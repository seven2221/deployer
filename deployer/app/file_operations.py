import os
import fnmatch
import zipfile
import shutil
from deployer.app.config import Config


def match_selection(dir, match):
    filelist = os.listdir(dir)
    results = []
    for name in filelist:
        if fnmatch.fnmatch(name, match):
            results.append(name)
    return results


def unpack_zip(zip):
    with zipfile.ZipFile(Config.path + zip) as archive:
        archive.extractall(Config.tempdir)
        archive.close()


def deleter(dir):
    shutil.rmtree(dir, ignore_errors=True)


