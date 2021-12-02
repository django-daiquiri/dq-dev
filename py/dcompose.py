import os
import re
import sys
from os.path import join as pj
from sys import exit as x

from py.colours import Colours
from py.util import (find, is_git, mkdir, pprint, rxbool, rxsearch,
                     uncomment_line, write_array_to_file, write_yaml)


class DCompose():
    def __init__(self, conf, prof):
        self.col = Colours()
        self.conf = conf
        self.prof = prof
        self.dcyaml = {}
        self.profconf = {}
        self.names = {}
        self.volumes = []

    def expand_vars_arr(self, arr, container_name=None):
        for i, el in enumerate(arr):
            arr[i] = self.expand_vars(arr[i], container_name)
        return arr

    def expand_vars(self, string, container_name=None):
        if '<' not in string and '>' not in string:
            return string
        # expand variables set in config
        string = string\
            .replace('<HOME>', os.environ['HOME'])\
            .replace('<ACTIVE_APP>', self.conf['conf']['active_app'])\
            .replace(
                '<PGAPP_DB_USER>',
                self.conf['conf']['env']['pgapp']['postgres_user']
            )\
            .replace(
                '<PGAPP_DB_PASS>',
                self.conf['conf']['env']['pgapp']['postgres_password']
            )\
            .replace(
                '<PGDATA_DB_USER>',
                self.conf['conf']['env']['pgdata']['postgres_user']
            )\
            .replace(
                '<PGDATA_DB_PASS>',
                self.conf['conf']['env']['pgdata']['postgres_password']
            )\
            .replace(
                '<RABBITMQ_VHOST>',
                self.conf['conf']['env']['rabbitmq']['rabbitmq_vhost']
            )\
            .replace(
                '<RABBITMQ_USER>',
                self.conf['conf']['env']['rabbitmq']['rabbitmq_user']
            )\
            .replace(
                '<RABBITMQ_PASS>',
                self.conf['conf']['env']['rabbitmq']['rabbitmq_password']
            )\
            .replace('<CONTAINER_PGAPP>', self.nam_con('pgapp'))\
            .replace('<CONTAINER_PGDATA>', self.nam_con('pgdata'))\
            .replace('<CONTAINER_DOCS>', self.nam_con('docs'))\
            .replace('<CONTAINER_RABBITMQ>', self.nam_con('rabbitmq'))\
            .replace('<UID>', self.conf['user']['idstr'])\
            .replace('<GID>', self.conf['user']['groupstr'])
        # expand env var placeholders set in other env vars
        if container_name is not None:
            try:
                env_vars = self.conf['conf']['env'][container_name]
            except KeyError:
                pass
            else:
                for k in env_vars:
                    key = str(k)
                    val = str(env_vars[key])
                    if key != '' and val != '':
                        string = string.replace('<' + key.upper() + '>', val)
        # add additional packages
        if container_name is not None:
            try:
                p = ' '.join(
                    self.conf['conf']['additional_packages'][container_name]
                )
            except KeyError:
                pass
            except TypeError:
                print(
                    self.col.err() +
                    self.col.yel(
                        'Please check additional packages config entry for '
                    ) +
                    container_name +
                    self.col.yel(' and make sure it is a not empty list.')
                )
                print(
                    'If you do not wish to use additional packages remove ' +
                    ' or comment the whole list entry.'
                )
                sys.exit()
            else:
                var = '<ADDITIONAL_PACKAGES>'
                if var in string:
                    string = string.replace('<ADDITIONAL_PACKAGES>', p)
                    string = uncomment_line(string)
        return string

    def iter_services(self):
        return self.conf['conf']['env']

    # service and container names
    def make_names(self):
        for service in self.iter_services():
            self.names[service] = {}
            self.names[service]['con'] =\
                'dqdev' + '-' + service + '-' + self.conf['prof']['name']
            self.names[service]['img'] =\
                'dqdev' + '_' + service + '_' + self.conf['prof']['name']

    def nam_img(self, service):
        return self.names[service]['img']

    def nam_con(self, service):
        return self.names[service]['con']

    def nam_daiq(self):
        for service in self.names:
            img = self.nam_img(service)
            if 'daiquiri' in img:
                return img
        return None

    def container_enabled(self, container_name):
        try:
            return self.conf['conf']['enable_containers'][container_name]
        except KeyError:
            return False

    # template
    def make_template(self):
        self.dcyaml['version'] = '3.9'
        self.dcyaml['services'] = {}
        self.dcyaml['volumes'] = {}

        for service in self.iter_services():
            if self.container_enabled(service) is True:
                c = self.nam_img(service)
                self.dcyaml['services'][c] = {}
                self.dcyaml['services'][c]['build'] = {}
                self.dcyaml['services'][c]['build']['context'] =\
                    '../../../docker/' + service
                self.dcyaml['services'][c]['container_name'] =\
                    self.nam_con(service)
                self.dcyaml['services'][c]['restart'] = 'always'

    # depends on
    def add_depends_on(self):
        self.dcyaml['services'][self.nam_daiq()]['depends_on'] = []
        for service in self.dcyaml['services']:
            if 'daiquiri' not in service:
                self.dcyaml['services'][self.nam_daiq()]['depends_on']\
                    .append(service)

    # env
    def add_env(self):
        for service in self.iter_services():
            try:
                env_arr = []
                for k in self.conf['conf']['env'][service]:
                    key = str(k)
                    val = str(self.conf['conf']['env'][service][key])
                    env_arr.append(key.upper() + '=' + val)
                env = self.expand_vars_arr(
                    env_arr, service
                )
            except KeyError:
                pass
            else:
                try:
                    p = self.conf['conf']['portmap'][service]
                except KeyError:
                    pass
                else:
                    env.append('EXPOSED_PORT=' + str(p['exposed']))

                for mp in self.conf['conf']['docker_volume_mountpoints']:
                    key = ''.join(re.findall('[A-Z0-9]', mp.upper()))
                    val = self.conf['conf']['docker_volume_mountpoints'][mp]
                    env.append(key + '=' + val)
                # try because exception occurs when a container is disabled
                try:
                    self.dcyaml['services'][self.nam_img(service)]['environment'] = env
                except KeyError:
                    pass

    # network
    def add_networks(self):
        nn = self.prof.conf['prof']['network_name']
        self.dcyaml['networks'] = {}
        self.dcyaml['networks'][nn] = {}
        self.dcyaml['networks'][nn]['external'] = {}
        self.dcyaml['networks'][nn]['external']['name'] = nn
        for service in self.dcyaml['services']:
            self.dcyaml['services'][service]['networks'] = [nn]

    # ports
    def add_ports(self):
        for service in self.conf['conf']['portmap']:
            try:
                self.dcyaml['services'][self.nam_img(service)]['ports'] =\
                    [self.conf['conf']['portmap'][service]['envstr']]
            except KeyError:
                pass

    # volumes
    def add_volumes(self):
        for service in self.dcyaml['services']:
            self.dcyaml['services'][service]['volumes'] = []

            for vol in self.volumes:
                if rxbool(vol['mount_inside'], service) is True:
                    self.dcyaml['services'][service]['volumes'].append(
                        vol['driver_opts']['device'] + ':' +
                        self.expand_vars(vol['mp'])
                    )

    def make_volumes(self):
        vols = []
        for volname in self.conf['conf']['docker_volume_mountpoints']:
            try:
                fol = self.conf['conf']['folders_on_host'][volname]
            except KeyError:
                fol = self.conf['conf']['folders_on_host'][
                    self.conf['conf']['active_app']
                ]
            v = self.make_volume(
                volname + '_' + self.profconf['name'],
                self.conf['conf']['docker_volume_mountpoints'][volname],
                fol,
                volname.startswith('dq_'),
                'daiquiri'
            )
            if self.valid_volume(v) is True:
                vols.append(v)

        for volname in self.conf['conf']['enable_volumes']:
            # TODO: do not hard code folders, improve structure
            if self.conf['conf']['enable_volumes'][volname] is True:
                volfolder = pj(
                    self.prof.get_profile_folder_by_name(
                        self.profconf['name']
                    ),
                    volname
                )
                if volname == 'docs':
                    volfolder = self.expand_vars(
                        self.profconf['conf']['folders_on_host']['docs']
                    )
                mkdir(volfolder)
                mp = '/var/lib/mysql'
                if volname.startswith('pg'):
                    mp = '/var/lib/postgresql/data'
                if volname == 'docs':
                    mp = '/home/dq/docs'
                mount_inside = volname
                if volname == 'docs':
                    mount_inside = 'daiquiri'
                vols.append(
                    self.make_volume(
                        volname + '_' + self.profconf['name'],
                        mp,
                        volfolder,
                        mount_inside=mount_inside
                    )
                )
        self.volumes = vols

    def make_volume(
        self, volname, mp, folder_on_host,
        required_git=False, mount_inside='.*'
    ):
        vol = {}
        vol['name'] = volname
        vol['mp'] = mp
        vol['required_git'] = required_git
        vol['mount_inside'] = mount_inside
        vol['driver'] = 'local'
        vol['driver_opts'] = {}
        vol['driver_opts']['o'] = 'bind'
        vol['driver_opts']['type'] = 'none'
        vol['driver_opts']['device'] = self.expand_vars(folder_on_host)
        return vol

    def valid_volume(self, vol):
        r = False
        dev = vol['driver_opts']['device']
        is_dir = os.path.isdir(dev)

        if is_dir is False and vol['required_git'] is False:
            print(
                'Run without volume ' + self.col.yel(vol['name']) +
                '. Path does not exist on host ' + self.col.yel(dev)
            )

        if is_dir is True:
            r = True

        if vol['required_git'] is True:
            ig = is_git(dev)
            if ig[0] is False:
                print(
                    '\n' + self.col.err() + 'Folder ' + self.col.yel(dev) +
                    ' does not look like a git repo. ' +
                    '\nPlease make sure that it contains the source of ' +
                    self.col.yel(vol['name']) + '\n'
                )
                x(1)
            else:
                r = True
        return r

    def write_yaml(self):
        if self.conf['dry_run'] is True:
            print(self.col.yel('\nDry run, dc yaml would look like this:'))
            pprint(self.dcyaml)
        else:
            print(
                'Write dc yaml to    ' +
                self.col.yel(self.conf['files']['dc_yaml']) + '\n'
            )
            write_yaml(self.dcyaml, self.conf['files']['dc_yaml'])

    def render_dockerfile_templates(self):
        arr = find(self.conf['basedir'], '.*/dockerfile.tpl', 'f')
        for fn in arr:
            print('Render dockerfile template ' + self.col.yel(fn))
            self.render_template_file(fn)

    def render_template_file(self, filename):
        container_name = rxsearch(
            r'[a-z0-9A-Z-]+(?=/dockerfile.tpl$)', filename
        )
        new_filename = rxsearch(r'.*(?=\.)', filename)
        arr = []
        try:
            filecontent = open(filename, 'r')
        except Exception as e:
            raise(e)
        else:
            for line in filecontent.read().splitlines():
                arr.append(self.expand_vars(line, container_name))
        write_array_to_file(arr, new_filename)

    # main
    def render_dc_yaml(self, profname=None):
        self.profconf = self.prof.read_profile_config(profname)

        self.make_names()
        self.make_template()
        self.make_volumes()

        self.add_depends_on()
        self.add_env()
        self.add_ports()
        self.add_networks()
        self.add_volumes()

        self.write_yaml()
