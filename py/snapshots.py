import os
import sys
import time
import zipfile
from os.path import isfile
from os.path import join as pj

from py.colours import Colours
from py.util import exists, get_lastmod, listfiles_only, ptable, rxbool


class Snapshots:
    def __init__(self, conf):
        self.conf = conf
        self.col = Colours()

    def check_name(self, name):
        if name is None or name is True:
            print(
                self.col.red("Error\n")
                + "  invalid snapshot name, please pass a valid string\n"
                + "  i.e. --save_snapshot hello, --restore_snapshot world\n"
            )
            sys.exit(1)

    def list_snapshots(self):
        fol = self.conf["snapshots_dir"]
        head = ["snapshot creation date", "snapshot file", "saved profile"]
        snapshotslist = []
        for fil in listfiles_only(fol):
            saved_profile = self.zipGetSavedProfile(fil)
            row = [get_lastmod(fil), fil, saved_profile]
            snapshotslist.append(row)
        snapshotslist.sort(key=lambda row: (row[0], row[1], row[2]), reverse=True)
        tabledata = []
        for snap in snapshotslist:
            tabledata.append([time.ctime(snap[0]), snap[1], snap[2]])
        ptable(head, tabledata)
        print("")

    def zipGetSavedProfile(self, filename):
        s = ""
        if zipfile.is_zipfile(filename) is True:
            zip = zipfile.ZipFile(filename)
            for fil in zip.namelist():
                if rxbool("conf\.toml$", fil) is True:
                    s = fil.replace("/conf.toml", "")
                    break
        return s

    def save_snapshot(self):
        name = self.conf["args"]["save_snapshot"]
        self.check_name(name)
        current_snapshot = pj(self.conf["snapshots_dir"], name) + ".zip"
        if exists(current_snapshot) is True:
            print('snapshot already exists "{}"'.format(current_snapshot))
            print("please choose a different name\n")
            sys.exit(0)
        ("save snapshot " + name)
        sources = [self.conf["prof"]["folder"]]
        for el in sources:
            self.toZip(os.path.relpath(el, self.conf["basedir"]), current_snapshot)
        print('Done, snapshot "{}" saved to file "{}"'.format(name, current_snapshot))

    def restore_snapshot(self):
        name = self.conf["args"]["restore_snapshot"]
        self.check_name(name)
        current_snapshot = pj(self.conf["snapshots_dir"], name) + ".zip"
        if exists(current_snapshot) is False:
            print("snapshot does not exists, the following are available:\n")
            self.list_snapshots()
            sys.exit(0)
        print('Restore snapshot "{}"'.format(name))
        with zipfile.ZipFile(current_snapshot, "r") as zip_ref:
            zip_ref.extractall(self.conf["basedir"])
        print("Done, file {} restored ".format(current_snapshot))

    def toZip(self, file, filename):
        zip_file = zipfile.ZipFile(filename, "w")
        if isfile(file):
            zip_file.write(file)
        else:
            self.addFolderToZip(zip_file, file)
        zip_file.close()

    def addFolderToZip(self, zip_file, folder):
        for file in os.listdir(folder):
            full_path = os.path.join(folder, file)
            if isfile(full_path):
                print("Add file " + str(full_path))
                zip_file.write(full_path)
            elif os.path.isdir(full_path):
                self.addFolderToZip(zip_file, full_path)
