import os
import pprint as ppr
import re
from os.path import sep as sep
from pathlib import Path
from shutil import copy, rmtree
from subprocess import PIPE, Popen
from sys import exit as x
from typing import Any

import pytomlpp as toml
import yaml
from tabulate import tabulate


def colgre(s: str) -> str:
    return "\033[92m" + str(s) + "\033[0m"


def colmag(s: str) -> str:
    return "\033[95m" + str(s) + "\033[0m"


def find(root, filter: str = ".*", filter_type: str = "f") -> list[Path]:
    detected = []
    for path, dirs, files in os.walk(root):
        if files and filter_type == "f":
            for filename in files:
                rfn = Path(path) / filename
                if bool(re.search(filter, str(rfn))) is True:
                    detected.append(rfn)
        elif dirs and filter_type == "d":
            for dirname in dirs:
                rdir = Path(path) / dirname
                if bool(re.search(filter, str(rdir))) is True:
                    detected.append(rdir)

    return sorted(detected)


def listdirs_only(root: Path) -> list[Path]:
    p = os.listdir(root)
    r = []
    for i in p:
        fil = root / i
        if fil.is_dir():
            r.append(fil)

    return sorted(r)


def listfiles_only(root: Path) -> list[Path]:
    p = os.listdir(root)
    r = []
    for i in p:
        fil = root / i
        if fil.is_file():
            r.append(fil)

    return sorted(r)


def run_cmd(cmd: list[str], silent: bool = True, debug: bool = False) -> str:
    o = ""
    if debug is False:
        proc = Popen(cmd, stdout=PIPE, stderr=PIPE, close_fds=True)
        (out, err) = proc.communicate()
        exitcode = proc.wait()
        if exitcode != 0:
            print(err.decode("utf-8"))
            return (False, None)
            x()
        o = out.decode("utf-8")
        if silent is False:
            print(o)
    else:
        print(" ".join(cmd))

    return o


def is_git(folder: Path | str) -> tuple[bool, str | None]:
    proc = Popen(
        ["git", "-C", folder, "remote", "-v"], stdout=PIPE, stderr=PIPE, close_fds=True
    )
    (out, err) = proc.communicate()
    exitcode = proc.wait()
    if exitcode != 0:
        return (False, None)
    out = out.splitlines()[0].decode("utf-8")
    try:
        out = re.search(r"git.*?\s", out).group(0)
    except (NameError, AttributeError):
        return (False, None)

    return (True, out)


def copy_file(src: Path, trg: Path):
    trg.mkdir(exist_ok=True, parents=True)
    sn = shortname(src)
    trg = trg / sn
    print(f"Copy file {colmag(src)} to {colgre(trg)}")
    copy(src, trg)


def empty_dir(dir: Path | str):
    for f in os.listdir(dir):
        os.remove(Path(dir) / f)


def exists(dir: Path | str) -> bool:
    return os.path.exists(dir)


def remove_dir(dir: Path):
    if dir.is_dir():
        rmtree(dir)


def read_toml(filename: Path | str) -> dict | None:
    filename = Path(filename)
    if not filename.is_file():
        print(f"yaml file does not exist: {filename}")
    else:
        with open(filename) as filedata:
            try:
                data = filedata.read()
                d = toml.loads(data)
                return d
            except Exception as e:
                print(f"toml decode error: {filename}")
                raise (e)
    return None


def write_toml(data, filename: Path | str):
    with open(filename, "w") as toml_file:
        toml.dump(data, toml_file)


def write_yaml(data, filename: Path | str):
    with open(filename, "w") as outfile:
        yaml.dump(data, outfile, default_flow_style=False, indent=2)


def write_array_to_file(data: list[str], filename: Path | str, mode: str = "w"):
    with open(filename, mode) as fp:
        for line in data:
            fp.write(line + "\n")


def is_port_no(s: int) -> bool:
    try:
        i = int(s)
    except (TypeError, ValueError):
        return False
    else:
        if 0 < i <= 65535:
            return True

    return False


def lookup_env_value(env, rx):
    r = None
    for el in env:
        if rxbool(rx, el):
            r = env[el]
    return r


def shortname(p: str) -> str:
    return re.search(r"[^/]+$", p).group(0)


def rxsearch(rx: str, s: str, gr: int = 0) -> str | None:
    r = None
    m = re.search(rx, s, flags=re.IGNORECASE)
    if bool(m) is True:
        r = m.group(gr)

    return r


def rxbool(rx: str, s: str) -> bool:
    return bool(re.search(rx, s))


def uncomment_line(line: str) -> str:
    rx = r"(#\s*)(.*)"
    if rxbool(rx, line) is True:
        line = rxsearch(rx, line, 2)
    return line


def pprint(obj: Any):
    pp = ppr.PrettyPrinter(indent=4)
    pp.pprint(obj)


def ptable(head, tab):
    print(tabulate(tab, headers=head))


def get_lastmod(filename):
    stat = os.stat(filename)
    return os.path.getmtime(filename)
