import re
import subprocess

from dq_dev.colours import Colours
from dq_dev.util import run_cmd


class Runner:
    def __init__(self, conf: dict):
        self.c = Colours()
        self.conf = conf
        self.need_sudo = self.need_sudo()

    def run_cmd_fg(self, cmd: list[str]):
        print(self.c.mag(' '.join(cmd)))
        if self.conf['dry_run'] is False:
            try:
                subprocess.run(cmd)
            except KeyboardInterrupt:
                pass

    def need_sudo(self):
        r = run_cmd(['whoami'])
        if bool(re.search('root', r)) is True:
            return False
        g = run_cmd(['groups'])
        if bool(re.search('docker', g)) is True:
            return False
        return True

    def file_arg_compose(self):
        return ['-f', str(self.conf['files']['dc_yaml'])]

    def run_docker(self, args: list[str]):
        cmd_arr = []
        if self.need_sudo is True:
            cmd_arr.append('sudo')
        cmd_arr.append('docker')
        cmd_arr.extend(args)
        self.run_cmd_fg(cmd_arr)

    def run_compose(self, args: list[str]):
        cmd_arr = []
        if self.need_sudo is True:
            cmd_arr.append('sudo')
        cmd_arr.extend(['docker', 'compose'])
        cmd_arr.extend(self.file_arg_compose())
        cmd_arr.extend(args)

        self.run_cmd_fg(cmd_arr)

    # docker compose commands
    def build(self):
        self.run_compose(['build'])

    def build_no_cache(self):
        self.run_compose(['build', '--no-cache'])

    def start(self):
        self.run_compose(['up', '--build', '-d'])
        self.tail_logs()

    def stop(self):
        self.run_compose(['stop'])

    def down(self):
        args = ['down', '--volumes', '--remove-orphans']
        if self.conf['args']['remove_images'] is True:
            args.append('--rmi all')
        self.run_compose(args)

    def tail_logs(self):
        self.run_compose(['logs', '-f'])

    def remove_images(self):
        self.run_compose(['down', '--volumes'])

    def remove_network(self):
        self.run_docker(['network', 'remove', self.conf['prof']['network_name']])
