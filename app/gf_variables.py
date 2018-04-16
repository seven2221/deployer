import zipfile
from app.config import Config
from app import gf_operations
from app import file_operations


def find_variables_in_zip():
    for jarFiles in selectors.match_selection(tempdir, "*jar"):
        for jarFile in jarFiles:
            jar_with_variables = zipfile.ZipFile(jarFile, 'r')
            jar_with_variables_filelist = jar_with_variables.infolist()
            for file in jar_with_variables_filelist:
                filename = file.filename
                with zipfile.ZipFile(jarFile) as jar_to_open:
                    with jar_to_open.open(filename) as opened_file:

                        for line in opened_file:
                            if filename.endswith('.bpel'):
                                if "literal>" in str(line):
                                    variable = str(line).split("literal")[1].replace(">${", "").replace("}</", "")
                                    if variable not in new_variables.variables:
                                        new_variables.variables.append(variable)
                            else:
                                if "${" in str(line):
                                    variable = str(line).split("${")[1].split("}")[0]
                                    if variable not in new_variables.variables and variable != "HttpDefaultPort" and "\\" not in variable:  # len(variable) < 50:
                                        new_variables.variables.append(variable)
                                if "<application-config" in str(line):
                                    configuration = str(line).split("\"")[3]
                                    if configuration not in new_variables.configurations and configuration not in new_variables.variables:
                                        new_variables.configurations.append(configuration)


class check_variables_old:
    new_variables = []

    @classmethod
    def find_exists_variables(cls, host, port):
        exists_variables = []
        for line in gf_operations.get_all_variables(host, port):
            if "executed successfully." not in str(line) and "Nothing to list" not in str(line):
                variable = str(line).split("=")[0].replace("b\'", "").replace("b\"", "").replace(" ", "")
                if variable not in exists_variables:
                    # print(variable)
                    exists_variables.append(variable)
        return exists_variables

    @classmethod
    def find_zip_variables(cls):
        zip_variables = []
        for jarFile in file_operations.match_selection(Config.tempdir, "*jar"):
            jarfile = zipfile.ZipFile(Config.tempdir + jarFile, 'r')
            filelist = jarfile.infolist()
            for file in filelist:
                filename = file.filename
                opened_file = jarfile.open(filename)
                for line in opened_file:
                    if filename.endswith('.bpel'):
                        if "literal>" in str(line):
                            variable = str(line).split("literal")[1].replace(">${", "").replace("}</",
                                                                                                "")  # нет желания возиться с регулярками, временный костыль
                            if variable not in zip_variables:
                                zip_variables.append(variable)
                    else:
                        if "${" in str(line):
                            variable = str(line).split("${")[1].split("}")[0]
                            # print(variable)
                            if variable not in zip_variables and variable != "HttpDefaultPort" and "\\" not in variable:  # len(variable) < 50:
                                zip_variables.append(variable)
        return zip_variables


    @classmethod
    def find_new_variables(cls, host):
        new_variables = []
        for variable in check_variables.find_zip_variables():
            if variable in check_variables.find_exists_variables(host):
                new_variables.append(variable)
        return new_variables
