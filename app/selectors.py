import os
import fnmatch


def match_selection(dir, match):
    filelist = os.listdir(dir)
    results = []
    for name in filelist:
        if fnmatch.fnmatch(name, match):
            results.append(name)
    return results
