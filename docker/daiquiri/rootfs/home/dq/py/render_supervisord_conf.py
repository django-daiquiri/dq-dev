#!/usr/bin/python3
import os
import secrets
import string
import sys
from os.path import join as pj

sys.path.append(pj(os.environ["HOME"], "app"))

from django.conf import settings
from dotenv import load_dotenv


class SupervisordConfRenderer:
    def __init__(self):
        print("start to render supervisord conf")
        self.home = os.environ["HOME"]
        self.spv_tpl_path = pj(self.home, "tpl/supervisord.conf")
        self.spv_conf_path = pj(self.home, "conf/supervisord.conf")
        self.spv_conf = self.read_template()
        self.is_async = self.to_bool(os.environ["ASYNC"])
        if self.is_async:
            print("async is true, load django settings")
            load_dotenv()
            os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
            print(os.environ["DJANGO_SETTINGS_MODULE"])
            self.django_settings = settings

    def to_bool(self, s: str):
        if s.lower() == "true" or s == 1:
            return True
        return False

    def random_string(self, len):
        charset = string.ascii_letters + string.digits
        pwd = ""
        for i in range(len):
            pwd += "".join(secrets.choice(charset))
        return pwd

    def make_spv_entry(self, queue, idx):
        qu = "query_" + self.getval(queue, "key", idx)
        prio = self.getval(queue, "priority", 1)
        return [
            "",
            "[program:" + qu + "]",
            "run-rmq-worker.sh " + qu + " " + prio,
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


if __name__ == "__main__":
    scr = SupervisordConfRenderer()
    print(settings)
    # print(scr.django_settings.QUERY_QUEUES)
    if scr.is_async:
        try:
            scr.django_settings.QUERY_QUEUES
        except ModuleNotFoundError:
            print("hahaha")
        else:
            print("render supervisord.conf")
            for idx, queue in enumerate(scr.django_settings.QUERY_QUEUES):
                en = scr.make_spv_entry(queue, idx)
                print("add queue to spv conf: %s" % en[1:])
                scr.spv_conf.extend(en)
    scr.save_config()
