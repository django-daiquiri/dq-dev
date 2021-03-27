import os
import re
import sys
from os.path import join as pj

scriptname = os.path.realpath(__file__)
scriptdir = '/'.join(scriptname.split('/')[:-1])
basedir = re.search(r'.*(?=\/)', scriptdir).group(0)

sys.path.append(pj(basedir, 'py'))
