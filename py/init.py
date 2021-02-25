import os
from os.path import isfile
from os.path import join as pj

from py.colours import Colours
from py.util import mkdir, read_yaml, x


def merge_dictionaries(dict1, dict2):
    for key, val in dict1.items():
        if isinstance(val, dict):
            dict2_node = dict2.setdefault(key, {})
            merge_dictionaries(val, dict2_node)
        else:
            if key not in dict2:
                dict2[key] = val
    return dict2


def init(args):
    col = Colours()
    conf = {}
    n = os.path.realpath(__file__)
    basedir = '/'.join(n.split('/')[:-2])
    conf['basedir'] = basedir

    conf['args'] = {}
    conf['files'] = {}
    conf['prof'] = {}
    conf['prof']['basedir'] = pj(conf['basedir'], 'usr', 'profiles')
    conf['files']['active_conf'] = pj(conf['prof']['basedir'], 'active.yaml')
    conf['files']['base_conf'] = pj(basedir, 'conf', 'baseconf.yaml')
    conf['files']['base_secrets'] = pj(basedir, 'conf', 'secrets.yaml')

    conf['args']['list'] = True
    conf['args']['down'] = parse_nargs(args.down)
    conf['args']['render'] = parse_nargs(args.render)
    conf['args']['run'] = parse_nargs(args.run)
    conf['args']['stop'] = parse_nargs(args.stop)
    conf['args']['display_profile'] = parse_nargs(args.display_profile)
    conf['args']['tail_logs'] = parse_nargs(args.tail_logs)
    conf['args']['set'] = args.set_profile
    conf['args']['create'] = args.create_profile

    apc = read_yaml(conf['files']['active_conf'])
    conf['prof']['name'] = ''
    if apc is not None:
        conf['prof']['name'] = apc['active_profile_name']

    for arg in conf['args']:
        if arg != 'list':
            val = conf['args'][arg]
            if val is not None:
                conf['args']['list'] = None
                if isinstance(val, str):
                    conf['prof']['name'] = val
                break

    # read base configurations
    print('Read base config  ' + col.yel(conf['files']['base_conf']))
    base_conf = read_yaml(conf['files']['base_conf'])
    print('Read base secrets ' + col.yel(conf['files']['base_secrets']))
    base_secrets = read_yaml(conf['files']['base_secrets'])
    base_conf['env'] = merge_dictionaries(base_conf['env'], base_secrets)
    conf['conf'] = base_conf

    # stop when no active profile was detected
    if conf['prof']['name'] == '':
        print(col.red(
            'No profile active. ' +
            'Please set one to be able to continue.'
        ))
        x()

    # read profile configurations
    conf['prof']['folder'] = pj(
        conf['prof']['basedir'], conf['prof']['name']
    )
    conf['files']['dc_yaml'] = pj(
        conf['prof']['folder'], 'docker-compose.yaml'
    )
    conf['files']['prof_conf'] = pj(conf['prof']['folder'], 'conf.yaml')
    conf['files']['prof_secrets'] = pj(conf['prof']['folder'], 'secrets.yaml')

    if conf['args']['set'] is None:
        print('\nUse profile       ' + col.gre(conf['prof']['name']))
    if isfile(conf['files']['prof_conf']) is True:
        if conf['args']['set'] is None:
            print('Read prof config  ' + col.yel(conf['files']['prof_conf']))
        prof_conf = read_yaml(conf['files']['prof_conf'])
        # merge the two
        conf['conf'] = merge_dictionaries(conf['conf'], prof_conf)
    else:
        if args.set_profile is None and args.create_profile is None:
            print(
                col.red('\nWarning') +
                '\n    Profile config does not exist: ' +
                col.yel(conf['files']['prof_conf']) +
                '\n    All base settings are going to be applied. ' +
                'It is highly likely your setup ' +
                'will turn out to be unusable.\n'
            )

    if isfile(conf['files']['prof_secrets']) is True:
        print('Read prof secrets ' + col.yel(conf['files']['prof_conf']))
        prof_secrets = read_yaml(conf['files']['prof_secrets'])
        conf['conf']['env'] = merge_dictionaries(conf['conf']['env'], prof_secrets)

    # user settings
    conf['user'] = {}
    conf['user']['id'] = os.getuid()
    conf['user']['idstr'] = str(conf['user']['id'])
    conf['user']['group'] = get_group(conf['user']['id'])
    conf['user']['groupstr'] = str(conf['user']['group'])
    conf['dry_run'] = args.dry_run
    mkdir(conf['prof']['basedir'])
    return conf


def parse_nargs(nargs):
    if isinstance(nargs, list):
        if len(nargs) < 1:
            return True
        else:
            return nargs[0]
    return None


def get_group(user_id):
    groups = sorted(os.getgroups())
    if user_id in groups:
        return user_id
    else:
        return groups[len(groups)-1]
