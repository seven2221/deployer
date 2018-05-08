import zipfile
import re
from app.config import Config
from app import gf_operations
from app import file_operations


def find_configurations_in_zip():
    zip_configurations = []
    for jarFile in file_operations.match_selection(Config.tempdir, "*jar"):
        for file in zipfile.ZipFile(Config.tempdir + jarFile, 'r').infolist():
            filename = file.filename
            with zipfile.ZipFile(Config.tempdir + jarFile).open(filename) as opened_file:
                for line in opened_file:
                    if "<application-config" in str(line):
                        configuration = str(line).split("\"")[3]
                        if configuration not in zip_configurations:
                            zip_configurations.append(configuration)
    return zip_configurations


def find_new_variables():
    new_configurations = []
    exists_variables = gf_operations.get_all_configurations()
    zip_variables = find_configurations_in_zip()
    for variable in zip_variables:
        if variable not in exists_variables:
            new_configurations.append(variable)
    return new_configurations
