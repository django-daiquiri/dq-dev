import argparse
from pathlib import Path
from shutil import copyfile
from sys import exit as x

from dq_dev.colours import Colours
from dq_dev.init import init
from dq_dev.util import (
    find,
    listdirs_only,
    ptable,
    read_toml,
    rxsearch,
    write_toml,
)


class Profile:
    def __init__(self, args: argparse.Namespace):
        self.exists = False
        self.conf = init(args)
        if (
            self.profile_exists(self.conf['prof']['name'])
            and self.conf['prof']['name'] != ''
        ):
            self.exists = True
        self.c = Colours()

    def create(self, profname: str):
        if self.profile_exists(profname):
            print(
                'Please check '
                + self.c.yel(self.conf['prof']['basedir'])
                + '\nDid nothing. Profile '
                + self.c.yel(profname)
                + ' seems to exist'
            )
        else:
            profile_folder = self.get_profile_folder_by_name(profname)
            profile_folder.mkdir(parents=True, exist_ok=True)
            conf_yaml = profile_folder / 'conf.toml'
            secrets_yaml = profile_folder / 'secrets.toml'
            print(
                'Fresh profile '
                + self.c.yel(profname)
                + ' created inside folder '
                + self.c.yel(profile_folder)
                + '\nPlease add your local settings to '
                + self.c.yel(conf_yaml)
                + "\nAnd don't forget your secrets."
            )
            copyfile(self.conf['files']['conf_tpl'], conf_yaml)
            copyfile(self.conf['files']['secrets_tpl'], secrets_yaml)

    def set(self, profname: str):
        if not self.profile_exists(profname):
            print(
                'Unable to set. Profile '
                + self.c.yel(profname)
                + ' does not seem to exist'
            )
        else:
            print('Set active profile ' + self.c.yel(profname))
            p = {}
            p['active_profile_name'] = profname
            write_toml(p, self.conf['files']['active_conf'])

    def read_profile_config(self, profname: str | None = None) -> dict:
        if profname is None or profname is True:
            profname = self.conf['prof']['name']
        if profname is None:
            print(
                'Unable to detect active profile. Either set one or use the command line arg.'
            )
            x(1)
        r = {}
        profile_list = find(self.conf['prof']['basedir'], profname + r'$', 'd')

        if len(profile_list) < 1:
            print(
                'Please check '
                + self.c.yel(self.conf['prof']['basedir'])
                + '\nProfile '
                + self.c.yel(profname)
                + ' does not seem to exist. '
            )
            x(1)
        if len(profile_list) > 1:
            print(
                'Please check '
                + self.c.yel(self.conf['prof']['basedir'])
                + '\nMultiple profiles matched: '
            )
            for profile in profile_list:
                print('\t' + profile)
            x(1)

        r['name'] = profname
        r['yaml'] = profile_list[0] / 'conf.toml'
        r['folder'] = profile_list[0].parent
        r['dc_yaml'] = r['folder'] / 'docker-compose.yaml'
        if r['yaml'].is_file():
            r['conf'] = read_toml(r['yaml'])
        return r

    def bool_to_str(self, bool: bool) -> str:
        return '*' if bool else ''

    def list(self):
        print(self.c.yel('\nThe following profiles are available\n'))
        arr = find(self.conf['prof']['basedir'], r'.*/profiles/[a-zA-Z0-9-_]+$', 'd')
        head = ['profile', 'has conf', 'active', 'volumes']
        tabledata = []
        for path in arr:
            shortname = rxsearch(r'[^/]+/[^/]+$', str(path))
            profname = rxsearch(r'[^/]+$', shortname)
            ap = self.conf['prof']['name']
            has_conf = self.bool_to_str((path / 'conf.toml').is_file())
            active = self.bool_to_str(profname == ap)
            listdirs_only(self.get_profile_folder_by_name(path))
            volumes = ' '.join(listdirs_only(self.get_profile_folder_by_name(path)))
            tabledata.append([profname, has_conf, active, volumes])
        ptable(head, tabledata)
        print()

    def get_profile_folder_by_name(self, profname: str | Path | None = None) -> Path:
        if profname is None:
            profname = self.conf['prof']['name']

        return Path(self.conf['prof']['basedir']) / profname

    def profile_exists(self, profname: str) -> bool:
        return self.get_profile_folder_by_name(profname).is_dir()

    def is_active(self):
        if self.conf['prof']['name'] == '':
            return False
        return True
