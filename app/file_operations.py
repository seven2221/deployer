import os
import fnmatch
import zipfile
import shutil
from app.config import Config


def match_selection(path, match):
    filelist = os.listdir(path)
    results = []
    for name in filelist:
        if fnmatch.fnmatch(name, match):
            results.append(name)
    return results


def unpack_zip(zip):
    with zipfile.ZipFile(Config.zippath + zip) as archive:
        archive.extractall(Config.tempdir)
        archive.close()


def deleter(dir):
    shutil.rmtree(dir, ignore_errors=True)


