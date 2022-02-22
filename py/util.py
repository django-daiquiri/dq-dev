import os
import pprint as ppr
import re
from os.path import isdir, isfile
from os.path import join as pj
from os.path import sep as sep
from shutil import copyfile, rmtree
from subprocess import PIPE, Popen
from sys import exit as x

import yaml
from tabulate import tabulate

# import toml
import pytomlpp as toml


def colgre(s):
    return '\033[92m' + str(s) + '\033[0m'


def colmag(s):
    return '\033[95m' + str(s) + '\033[0m'


def find(root, filter='.*', filter_type='f'):
    detected = []
    for (path, dirs, files) in os.walk(root):
        if files and filter_type == 'f':
            for filename in files:
                rfn = pj(path, filename)
                if bool(re.search(filter, rfn)) is True:
                    detected.append(rfn)
        elif dirs and filter_type == 'd':
            for dirname in dirs:
                rdir = pj(path, dirname)
                if bool(re.search(filter, rdir)) is True:
                    detected.append(rdir)
    return(sorted(detected))


def listdirs_only(root):
    p = os.listdir(root)
    r = []
    for i in p:
        fil = pj(root, i)
        if isdir(fil):
            r.append(fil)
    return sorted(r)


def listfiles_only(root):
    p = os.listdir(root)
    r = []
    for i in p:
        fil = pj(root, i)
        if isfile(fil):
            r.append(fil)
    return sorted(r)


def run_cmd(cmd, silent=True, debug=False):
    o = ''
    if debug is False:
        proc = Popen(cmd, stdout=PIPE, stderr=PIPE, close_fds=True)
        (out, err) = proc.communicate()
        exitcode = proc.wait()
        if exitcode != 0:
            print(err.decode('utf-8'))
            return (False, None)
            x()
        o = out.decode('utf-8')
        if silent is False:
            print(o)
    else:
        print(' '.join(cmd))
    return o


def is_git(folder):
    proc = Popen(
        ['git', '-C', folder, 'remote', '-v'],
        stdout=PIPE, stderr=PIPE, close_fds=True
    )
    (out, err) = proc.communicate()
    exitcode = proc.wait()
    if exitcode != 0:
        return (False, None)
    out = out.splitlines()[0].decode('utf-8')
    out = re.search(r'git.*?\s', out).group(0)
    return (True, out)


def copy_file(src,  trg):
    if exists(trg) is False:
        mkdir(trg)
    if isdir(trg) is True:
        sn = shortname(src)
        trg = pj(trg, sn)
    print('Copy file ' + colmag(src) + ' to ' + colgre(trg))
    copyfile(src, trg)


def empty_dir(dir):
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))


def exists(dir):
    return os.path.exists(dir)


def mkdir(dir):
    if exists(dir) is False:
        os.makedirs(dir)


def remove_dir(dir):
    if exists(dir) is True:
        rmtree(dir)


def read_toml(filename):
    if os.path.isfile(filename) is False:
        print('yaml file does not exist: ' + filename)
    else:
        with open(filename) as filedata:
            try:
                data = filedata.read()
                d = toml.loads(data)
                return(d)
            except Exception as e:
                print('toml decode error: ' + str(filename))
                raise(e)
    return None


def write_toml(data, filename):
    with open(filename, 'w') as toml_file:
        toml.dump(data, toml_file)


def write_yaml(data, filename):
    with open(filename, 'w') as outfile:
        yaml.dump(data, outfile, default_flow_style=False, indent=4)


def write_array_to_file(data, filename, mode='w'):
    with open(filename, mode) as fp:
        for line in data:
            fp.write(line + '\n')


def is_port_no(s):
    try:
        i = int(s)
    except (TypeError, ValueError):
        return False
    else:
        if i <= 65535:
            return True
    return False


def lookup_env_value(env, rx):
    r = None
    for el in env:
        if rxbool(rx, el):
            r = env[el]
    return r


def shortname(p):
    return re.search(r'[^/]+$', p).group(0)


def rxsearch(rx, s, gr=0):
    r = None
    m = re.search(rx, s, flags=re.IGNORECASE)
    if bool(m) is True:
        r = m.group(gr)
    return r


def rxbool(rx, s):
    return bool(re.search(rx, s))


def uncomment_line(line):
    rx = r'(#\s*)(.*)'
    if rxbool(rx, line) is True:
        line = rxsearch(rx, line, 2)
    return line


def path_after_last_slash(s):
    return rxsearch('[^' + sep + ']+$', s)


def path_up_to_last_slash(s):
    return rxsearch('.*(?=\\' + sep + ')', s)


def pprint(obj):
    pp = ppr.PrettyPrinter(indent=4)
    pp.pprint(obj)


def ptable(head, tab):
    print(tabulate(tab, headers=head))
