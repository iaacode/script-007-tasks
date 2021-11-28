import logging
import os
import os.path
import shutil

import pytest

from server import FileService


@pytest.fixture()
def filefordel():
    filedict = FileService.create_file('qwe.txt')
    return os.path.join(os.getcwd(), filedict['name'])


@pytest.fixture()
def examplefile():
    return os.path.abspath(FileService.create_file('qwe.txt')['name'])


def test_create_file(filefordel):
    assert os.path.exists(filefordel)


def test_get_file_data(examplefile):
    assert type(FileService.get_file_data(examplefile)) is dict


def test_delete_file(filefordel):
    FileService.delete_file(filefordel)
    assert not os.path.exists(filefordel)


def test_change_dir():
    curr_dir = os.getcwd()
    assert FileService.change_dir(os.getcwd(), '../') != curr_dir
    FileService.change_dir(curr_dir)

def test_get_data():
    assert type(FileService.get_files()) is list
