import sys
import time
import zipfile
from pathlib import Path

from dq_dev.colours import Colours
from dq_dev.util import get_lastmod, listfiles_only, ptable, rxbool


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
        print(f'Done, file {current_snapshot} restored')

    def toZip(self, file: Path, filename: Path):
        zip_file = zipfile.ZipFile(filename, 'w')
        if file.is_file():
            zip_file.write(file)
        else:
            self.addFolderToZip(zip_file, file)
        zip_file.close()

    def addFolderToZip(self, zip_file: zipfile.ZipFile, folder: Path):
        for file in folder.iterdir():
            full_path = folder / file
            if full_path.is_file():
                print(f'Add file {str(full_path)}')
                zip_file.write(full_path)
            elif full_path.is_dir():
                self.addFolderToZip(zip_file, full_path)
