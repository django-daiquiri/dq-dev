import os
import re
from os.path import join as pj

from . import fixpath  # noqa
from util import find, rxsearch, uncomment_line  # noqa

scriptname = os.path.realpath(__file__)
scriptdir = '/'.join(scriptname.split('/')[:-1])


def test_find():
    assert_find('', 6, '1.txt', '3.yaml')
    assert_find('.*.yaml$', 3, '1.yaml', '3.yaml')


def assert_find(filter, alen, aelf, aell):
    tf = pj(scriptdir, 'testdata', 'find')
    res = find(tf, filter)
    assert len(res) == alen
    assert \
        re.search(r'[^' + os.path.sep + ']+$', res[0]).group(0) == aelf
    assert \
        re.search(r'[^' + os.path.sep + ']+$', res[alen - 1]).group(0) == aell
    print(res)


def test_rxsearch():
    assert rxsearch('999', 'hello world') is None
    assert rxsearch('.*', 'hello world') == 'hello world'
    assert rxsearch('.*?o', 'hello world') == 'hello'
    assert rxsearch('(?=.*?o).*(rld)', 'hello world', 1) == 'rld'


def test_uncomment_line():
    assert uncomment_line('hello world') == 'hello world'
    assert uncomment_line('#hello world') == 'hello world'
    assert uncomment_line('# hello world') == 'hello world'
    assert uncomment_line('#  hello world') == 'hello world'
    assert uncomment_line('#     hello world') == 'hello world'
