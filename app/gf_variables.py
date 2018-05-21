import zipfile
import re
from app.config import Config
from app import gf_operations
from app import file_operations


def find_variables_in_zip():
    zip_variables = []
    for jarFile in file_operations.match_selection(Config.tempdir, "*jar"):
        for file in zipfile.ZipFile(Config.tempdir + jarFile, 'r').infolist():
            filename = file.filename
            with zipfile.ZipFile(Config.tempdir + jarFile).open(filename) as opened_file:
                for line in opened_file:
                    if "${" in str(line):
                        try:
                            variable = str(re.findall(r"\{([A-Za-z].*)\}", str(line))[0]).replace("[\'", "").replace("\']", "").split("}")[0]
                            if variable not in zip_variables and variable != "HttpDefaultPort" and variable != "[]" and "\\" not in variable:
                                zip_variables.append(variable)
                        except IndexError:
                            print(str(line))
                            print(str(re.findall(r"\{([A-Za-z].*)\}", str(line))))
    return zip_variables


def find_new_variables():
    new_variables = []
    exists_variables = gf_operations.get_all_variables()
    zip_variables = find_variables_in_zip()
    for variable in zip_variables:
        if variable not in exists_variables:
            new_variables.append(variable)
    return new_variables
