import os
import sys
import time
import zipfile
from os.path import isfile
from pathlib import Path

from dq_dev.colours import Colours
from dq_dev.util import exists, get_lastmod, listfiles_only, ptable, rxbool


class Snapshots:
    def __init__(self, conf: dict):
        self.conf = conf
        self.col = Colours()

    def check_name(self, name: str | None):
        if name is None or name is True:
            print(
                self.col.red('Error\n')
                + '  invalid snapshot name, please pass a valid string\n'
                + '  i.e. --save_snapshot hello, --restore_snapshot world\n'
            )
            sys.exit(1)

    def list_snapshots(self):
        snapshots_dir = self.conf['snapshots_dir']
        head = ['snapshot creation date', 'snapshot file', 'saved profile']
        snapshotslist = []
        for filename in listfiles_only(snapshots_dir):
            saved_profile = self.zipGetSavedProfile(filename)
            row = [get_lastmod(filename), filename, saved_profile]
            snapshotslist.append(row)
        snapshotslist.sort(key=lambda row: (row[0], row[1], row[2]), reverse=True)
        tabledata = []
        for snap in snapshotslist:
            tabledata.append([time.ctime(snap[0]), snap[1], snap[2]])
        ptable(head, tabledata)
        print('')

    def zipGetSavedProfile(self, filename: Path):
        s = ''
        if zipfile.is_zipfile(filename):
            zip = zipfile.ZipFile(filename)
            for fil in zip.namelist():
                if rxbool('conf\.toml$', fil) is True:
                    s = fil.replace('/conf.toml', '')
                    break
        return s

    def save_snapshot(self):
        name = self.conf['args']['save_snapshot']
        self.check_name(name)
        current_snapshot = (self.conf['snapshots_dir'] / name).with_suffix('.zip')
        if current_snapshot.is_file():
            print(
                f'snapshot already exists ("{current_snapshot}"), please choose a different name'
            )
            sys.exit(0)
        ('save snapshot ' + name)
        sources = [self.conf['prof']['folder']]
        for path in sources:
            self.toZip(path.relative_to(self.conf['basedir']), current_snapshot)
        print(f'Done, snapshot "{name}" saved to file "{current_snapshot}"')

    def restore_snapshot(self):
        name = self.conf['args']['restore_snapshot']
        self.check_name(name)
        current_snapshot = (self.conf['snapshots_dir'] / name).with_suffix('.zip')
        if not current_snapshot.is_file():
            print('snapshot does not exists, the following are available:\n')
            self.list_snapshots()
            sys.exit(0)
        print(f'Restore snapshot {name}')
        with zipfile.ZipFile(current_snapshot, 'r') as zip_ref:
            zip_ref.extractall(self.conf['basedir'])
        print('Done, file {} restored '.format(current_snapshot))

    def toZip(self, file, filename):
        zip_file = zipfile.ZipFile(filename, 'w')
        if isfile(file):
            zip_file.write(file)
        else:
            self.addFolderToZip(zip_file, file)
        zip_file.close()

    def addFolderToZip(self, zip_file, folder):
        for file in os.listdir(folder):
            full_path = os.path.join(folder, file)
            if isfile(full_path):
                print('Add file ' + str(full_path))
                zip_file.write(full_path)
            elif os.path.isdir(full_path):
                self.addFolderToZip(zip_file, full_path)
