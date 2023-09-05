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
        self.home = os.environ["HOME"]
        self.spv_tpl_path = pj(self.home, "tpl/supervisord.conf")
        self.spv_conf_path = pj(self.home, "conf/supervisord.conf")
        self.spv_conf = self.read_template()
        self.is_async = self.to_bool(os.environ["ASYNC"])
        if self.is_async:
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
        for i in range(len):
            pwd += "".join(secrets.choice(charset))
        return pwd

    def make_spv_entry(self, queue):
        qu = "query_" + queue["key"]
        prio = str(queue["priority"])
        return [
            "",
            "[program:" + qu + "]",
            "run-rmq-worker.sh " + qu + " " + prio,
            "exitcodes = 255",
        ]

    def read_template(self):
        data = []
        os.environ["SPV_USERNAME"] = self.random_string(32)
        os.environ["SPV_PASSWORD"] = self.random_string(32)
        with open(self.spv_tpl_path, "r") as file:
            temp = file.read().splitlines()
        for line in temp:
            data.append(os.path.expandvars(line))
        return data

    def save_config(self):
        with open(self.spv_conf_path, "w") as file:
            for el in self.spv_conf:
                file.write("%s\n" % el)


if __name__ == "__main__":
    scr = SupervisordConfRenderer()

    if scr.is_async:
        for queue in scr.django_settings.QUERY_QUEUES:
            en = self.make_spv_entry(queue)
            scr.spv_conf.extend(en)
    scr.save_config()
