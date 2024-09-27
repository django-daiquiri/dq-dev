import os
from os.path import isdir, isfile
from os.path import join as pj
import sys

from py.colours import Colours
from py.util import (
    copy_file,
    exists,
    is_port_no,
    listdirs_only,
    listfiles_only,
    mkdir,
    read_toml,
    remove_dir,
    shortname,
)


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
    basedir = "/".join(n.split("/")[:-2])
    conf["basedir"] = basedir
    conf["args"] = get_parsed_args(args)
    conf["prof"] = {}
    conf["prof"]["basedir"] = pj(conf["basedir"], "usr", "profiles")
    conf["files"] = {}
    conf["files"]["active_conf"] = pj(conf["prof"]["basedir"], "active.toml")
    conf["files"]["conf_tpl"] = pj(conf["basedir"], "conf_tpl", "conf.toml")
    conf["files"]["secrets_tpl"] = pj(conf["basedir"], "conf_tpl", "secrets.toml")
    conf["snapshots_dir"] = pj(conf["basedir"], "usr", "snapshots")

    apc = read_toml(conf["files"]["active_conf"]) or {}
    conf["prof"]["name"] = apc.get("active_profile_name", "")
    # stop init when no active profile was detected
    if conf["prof"]["name"] == "":
        return conf

    # read profile configurations
    conf["prof"]["folder"] = pj(conf["prof"]["basedir"], conf["prof"]["name"])
    conf["prof"]["network_name"] = "dqdevnet_" + conf["prof"]["name"]
    conf["files"]["dc_yaml"] = pj(conf["prof"]["folder"], "docker-compose.yaml")
    conf["files"]["prof_conf"] = pj(conf["prof"]["folder"], "conf.toml")
    conf["files"]["prof_secrets"] = pj(conf["prof"]["folder"], "secrets.toml")

    mkdir(conf["snapshots_dir"])
    if conf["args"]["set"] is None and args.save_snapshot and args.restore_snapshot:
        print("\nUse profile         " + col.gre(conf["prof"]["name"]))

    conf["conf"] = {}
    if isfile(conf["files"]["prof_conf"]) is True:
        if conf["args"]["set"] is None:
            print("Read prof config    " + col.yel(conf["files"]["prof_conf"]))
        conf["conf"] = read_toml(conf["files"]["prof_conf"])
    else:
        print(
            col.red("\nWarning") + "\n  Profile config does not exist!")

    if isfile(conf["files"]["prof_secrets"]) is True:
        print("Read prof secrets   " + col.yel(conf["files"]["prof_secrets"]))
        prof_secrets = read_toml(conf["files"]["prof_secrets"])
        conf["conf"]["env"] = merge_dictionaries(conf["conf"]["env"], prof_secrets)

    # user settings
    conf["user"] = {}
    conf["user"]["id"] = os.getuid()
    conf["user"]["idstr"] = str(conf["user"]["id"])
    conf["user"]["group"] = get_group(conf["user"]["id"])
    conf["user"]["groupstr"] = str(conf["user"]["group"])
    conf["dry_run"] = args.dry_run
    mkdir(conf["prof"]["basedir"])

    clean_temp_files(conf["basedir"], conf["conf"]["enable_containers"])

    copy_custom_scripts(
        conf["conf"]["custom_scripts"], conf["basedir"], conf["conf"]["active_app"]
    )

    create_rootfs_folders(conf["basedir"])

    conf["conf"]["portmap"] = parse_ports(conf)
    del conf["conf"]["exposed_ports"]

    return conf


def get_parsed_args(args):
    parsed_args = {}
    parsed_args["down"] = parse_nargs(args.down)
    parsed_args["remove_network"] = parse_bool(args.remove_network)
    parsed_args["remove_images"] = parse_bool(args.remove_images)
    parsed_args["render"] = parse_nargs(args.render)
    parsed_args["build"] = parse_nargs(args.build)
    parsed_args["run"] = parse_nargs(args.run)
    parsed_args["stop"] = parse_nargs(args.stop)
    parsed_args["display_profile"] = parse_nargs(args.display_profile)
    parsed_args["tail_logs"] = parse_nargs(args.tail_logs)
    parsed_args["set"] = args.set_profile
    parsed_args["create"] = args.create_profile
    parsed_args["list_snapshots"] = args.list_snapshots
    parsed_args["save_snapshot"] = parse_nargs(args.save_snapshot)
    parsed_args["restore_snapshot"] = parse_nargs(args.restore_snapshot)
    return parsed_args



def parse_bool(boolval):
    if boolval is True:
        return boolval
    else:
        return None


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
        try:
            return groups[len(groups) - 1]
        except:
            return ""


def create_rootfs_folders(basedir):
    dockerdir = pj(basedir, "docker")
    for dir in listdirs_only(dockerdir):
        mkdir(pj(dir, "rootfs"))


def clean_temp_files(basedir, container_names):
    for con in container_names:
        fol = pj(basedir, "docker", con, "rootfs", "tmp")
        remove_dir(fol)


def copy_custom_scripts(cs_conf, basedir, active_app):
    col = Colours()
    for typ in cs_conf:
        for con in cs_conf[typ]:
            dockdir = pj(basedir, "docker", con)
            if exists(dockdir) is True:
                target_folder = pj(dockdir, "rootfs", "tmp", "custom_scripts", typ)
                source_folder = expand(cs_conf[typ][con], active_app)
                if isdir(source_folder) is True:
                    files = listfiles_only(source_folder)
                    if len(files) > 0:
                        print(
                            "\nAdd custom scripts to container "
                            + col.gre(shortname(dockdir))
                        )
                    for fil in files:
                        copy_file(fil, target_folder)
    print("")


def expand(s, active_app):
    return s.replace("<HOME>", os.environ["HOME"]).replace("<ACTIVE_APP>", active_app)


def parse_ports(conf):
    portmap = {}
    for service_name in conf["conf"]["enable_containers"]:
        r = None
        try:
            exp = conf["conf"]["exposed_ports"][service_name]
        except KeyError:
            pass
        else:
            if is_port_no(exp) is True:
                r = {}
                r["exposed"] = str(exp)
                r["envstr"] = r["exposed"] + ":"
            inp = "0"
            if service_name == "daiquiri":
                inp = r["exposed"]
            if service_name == "pgapp" or service_name == "pgdata":
                inp = str(5432)
            if service_name == "rabbitmq":
                inp = str(5672)
            if inp == "0":
                print(
                    "\n[error] can not construct port map, "
                    + "unable to determine internally used port for service '"
                    + service_name
                    + "'\n"
                )
                sys.exit(1)
            r["internal"] = str(inp)
            r["envstr"] += r["internal"]
        if r is not None:
            portmap[service_name] = r
    return portmap
