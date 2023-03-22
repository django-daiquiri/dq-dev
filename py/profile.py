from os.path import isdir, isfile
from os.path import join as pj
from shutil import copyfile
from sys import exit as x

from py.colours import Colours
from py.util import (
    find,
    listdirs_only,
    mkdir,
    path_up_to_last_slash,
    ptable,
    read_toml,
    rxsearch,
    write_toml,
)


class Profile:
    def __init__(self, conf):
        self.conf = conf
        self.c = Colours()

    def create(self, profname):
        if self.profile_exists(profname) is True:
            print(
                "Please check "
                + self.c.yel(self.conf["prof"]["basedir"])
                + "\nDid nothing. Profile "
                + self.c.yel(profname)
                + " seems to exist"
            )
        else:
            mkdir(self.get_profile_folder_by_name(profname))
            conf_yaml = pj(self.get_profile_folder_by_name(profname), "conf.toml")
            secrets_yaml = pj(self.get_profile_folder_by_name(profname), "secrets.toml")
            print(
                "Fresh profile "
                + self.c.yel(profname)
                + " created inside folder "
                + self.c.yel(self.get_profile_folder_by_name(profname))
                + "\nPlease add your local settings to "
                + self.c.yel(conf_yaml)
                + "\nAnd don't forget your secrets."
            )
            copyfile(self.conf["files"]["base_conf"], conf_yaml)
            copyfile(self.conf["files"]["base_secrets"], secrets_yaml)

    def set(self, profname):
        if self.profile_exists(profname) is False:
            print(
                "Unable to set. Profile "
                + self.c.yel(profname)
                + " does not seem to exist"
            )
        else:
            print("Set active profile " + self.c.yel(profname))
            p = {}
            p["active_profile_name"] = profname
            write_toml(p, self.conf["files"]["active_conf"])

    def read_profile_config(self, profname=None):
        if profname is None or profname is True:
            profname = self.conf["prof"]["name"]
        if profname is None:
            print(
                "Unable to detect active profile. Either set one or use "
                + "the command line arg."
            )
            x(1)
        r = {}
        f = find(self.conf["prof"]["basedir"], profname + r"$", "d")
        if len(f) < 1:
            print(
                "Please check "
                + self.c.yel(self.conf["prof"]["basedir"])
                + "\nProfile "
                + self.c.yel(profname)
                + " does not seem to exist. "
            )
            x(1)
        if len(f) > 1:
            print(
                "Please check "
                + self.c.yel(self.conf["prof"]["basedir"])
                + "\nMultiple profiles matched: "
            )
            for el in f:
                print("\t" + el)
            x(1)
        r["name"] = profname
        r["yaml"] = pj(f[0], "conf.toml")
        r["folder"] = path_up_to_last_slash(f[0])
        r["dc_yaml"] = pj(r["folder"], "docker-compose.yaml")
        if isfile(r["yaml"]) is True:
            r["conf"] = read_toml(r["yaml"])
        return r

    def boolstr(self, bool):
        if bool is True:
            return "*"
        else:
            return ""

    def list(self):
        print(self.c.yel("\nThe following profiles are available\n"))
        arr = find(self.conf["prof"]["basedir"], r".*/profiles/[a-zA-Z0-9-_]+$", "d")
        head = ["profile", "has conf", "active", "volumes"]
        tabledata = []
        for el in arr:
            shortname = rxsearch(r"[^/]+/[^/]+$", el)
            profname = rxsearch(r"[^/]+$", shortname)
            ap = self.conf["prof"]["name"]
            has_conf = self.boolstr(isfile(pj(el, "conf.toml")))
            active = self.boolstr(profname == ap)
            listdirs_only(self.get_profile_folder_by_name(el))
            volumes = " ".join(listdirs_only(self.get_profile_folder_by_name(el)))
            tabledata.append([profname, has_conf, active, volumes])
        ptable(head, tabledata)
        print()

    def get_profile_folder_by_name(self, profname=None):
        if profname is None:
            profname = self.conf["prof"]["name"]
        return pj(self.conf["prof"]["basedir"], profname)

    def profile_exists(self, profname):
        return isdir(self.get_profile_folder_by_name(profname))
