import re
import subprocess

from py.colours import Colours
from py.util import run_cmd


class Runner():
    def __init__(self, dcyaml, debug):
        self.c = Colours()
        self.dcyaml = dcyaml
        self.debug = debug
        self.need_sudo = self.need_sudo()

    def run_cmd_fg(self, cmd):
        print(self.c.mag(' '.join(cmd)))
        if self.debug is False:
            subprocess.run(cmd)

    def need_sudo(self):
        g = run_cmd(['groups'])
        if bool(re.search('docker', g)) is True:
            return False
        else:
            return True

    def file_arg_compose(self):
        return ['-f', self.dcyaml]

    def run_compose(self, args):
        cmd_arr = []
        if self.need_sudo is True:
            cmd_arr.append('sudo')
        cmd_arr.append('docker-compose')
        cmd_arr.extend(self.file_arg_compose())
        cmd_arr.extend(args)
        self.run_cmd_fg(cmd_arr)

    # docker compose commands
    def start(self):
        self.run_compose(['up', '--build', '-d'])
        self.tail_logs()

    def stop(self):
        self.run_compose(['stop'])

    def down(self, rmi):
        args = ['down', '--volumes', '--remove-orphans']
        if rmi is True:
            args.append('--rmi all')
        self.run_compose(args)

    def tail_logs(self):
        self.run_compose(['logs', '-f'])

    def remove_images(self):
        self.run_compose(['down', '--volume'])
