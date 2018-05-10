import zipfile
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


def find_new_configurations():
    new_configurations = []
    exists_configurations = gf_operations.get_all_configurations()
    zip_configurations = find_configurations_in_zip()
    for variable in zip_configurations:
        print(variable)
        if variable not in exists_configurations:
            new_configurations.append(variable)
    return new_configurations
