#!/usr/bin/python3
import os
import re
import secrets
import string
import sys
from pathlib import Path

sys.path.append(str(Path(os.environ["HOME"])/ "app"))

from django.conf import settings
from dotenv import load_dotenv


class SupervisordConfRenderer:
    def __init__(self):
        print("start to render supervisord conf")
        self.home = Path(os.environ["HOME"])
        self.spv_tpl_path = self.home / "tpl/supervisord.conf"
        self.spv_conf_path = self.home / "conf/supervisord.conf"
        self.spv_conf = self.read_template()
        self.is_async = self.to_bool(os.environ["ASYNC"])
        if self.is_async:
            print("async is true, load django settings")
            load_dotenv()
            os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
            self.django_settings = settings

    def to_bool(self, s: str):
        if s.lower() == "true" or s == 1:
            return True
        return False

    def random_string(self, len):
        charset = string.ascii_letters + string.digits
        pwd = ""
        for _ in range(len):
            pwd += "".join(secrets.choice(charset))
        return pwd

    def make_spv_entry(self, queue, idx):
        qu = "query_" + self.getval(queue, "key", idx)
        prio = self.getval(queue, "priority", 1)
        return [
            "",
            "[program:" + qu + "]",
            "command = run-rmq-worker.sh " + qu + " " + prio,
            "exitcodes = 255",
        ]

    def getval(self, dic, val, default=""):
        try:
            return str(dic[val])
        except KeyError:
            return str(default)

    def open_file(self, filepath, mode):
        try:
            fil = open(filepath, mode)
        except OSError:
            print("could not open file %s" % filepath)
            return None
        else:
            return fil

    def read_template(self):
        print("read conf template %s" % self.spv_tpl_path)
        data = []
        os.environ["SPV_USERNAME"] = self.random_string(32)
        os.environ["SPV_PASSWORD"] = self.random_string(32)
        fil = self.open_file(self.spv_tpl_path, "r")
        if fil is not None:
            with fil:
                temp = fil.read().splitlines()
            for line in temp:
                data.append(os.path.expandvars(line))
        return data

    def save_config(self):
        fil = self.open_file(self.spv_conf_path, "w")
        if fil is not None:
            with fil:
                print("save rendered conf %s" % self.spv_conf_path)
                for el in self.spv_conf:
                    fil.write("%s\n" % el)


    def add_to_supervisord_conf_from_env_var(self):
        entries = os.getenv("ADD_TO_SUPERVISORD_CONF")
        if entries is not None:
            self.spv_conf.append("")
            self.spv_conf.append(
                "# from add_to_supervisord_conf env var set in conf.toml"
            )
            arr = entries.split(",")
            for el in arr:
                substr = self.rxfind("(?<=').*(?=')", el)
                if substr is not None:
                    print("add to spv conf from env: %s" % substr)
                    if substr[0] == "[":
                        self.spv_conf.append("")
                    self.spv_conf.append(substr)
            self.spv_conf.append("")

    def rxfind(self, rx, string, group=0, ignoreCase=False):
        r = None
        if ignoreCase is True:
            m = re.search(rx, string, flags=re.IGNORECASE)
        else:
            try:
                m = re.search(rx, string)
            except TypeError:
                pass
            else:
                if bool(m) is True:
                    if group is None:
                        r = m
                    else:
                        r = m.group(group)
        return r


if __name__ == "__main__":
    scr = SupervisordConfRenderer()
    if scr.is_async:
        try:
            scr.django_settings.QUERY_QUEUES
        except (ModuleNotFoundError, KeyError):
            print(
                "can not open django_settings.QUERY_QUEUES, skip query queue renderer"
            )
        else:
            print("render supervisord.conf")
            for idx, queue in enumerate(scr.django_settings.QUERY_QUEUES):
                en = scr.make_spv_entry(queue, idx)
                print("add queue to spv conf: %s" % en[1:])
                scr.spv_conf.extend(en)
    scr.add_to_supervisord_conf_from_env_var()
    scr.save_config()
    print("done")
