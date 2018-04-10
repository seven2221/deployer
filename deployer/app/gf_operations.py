import subprocess
import zipfile
from deployer.app import file_operations
from deployer.app.config import Config


'''реквесты:
 list-jbi-application-variables
 list-jbi-application-configurations
 list-jbi-service-assemblies
 '''


def call_asadmin(request, component, host, port, passfile):
    #print("asadmin list-jbi-application-variables --component" + component + "--host" + host + "--port 4848 --user admin --passwordfile D:\\Glassfish22\\passfile")
    callrequest = subprocess.Popen(["asadmin", request, "--component", component, "--host", host, "--port", port, "--user", "admin", "--passwordfile", passfile], stdout=subprocess.PIPE, shell=True)
    return callrequest.stdout


class check_variables:

    new_variables = []

    @classmethod
    def find_variables(cls, host):
        exists_variables = []
        for component in Config.GFcomponents:
            for line in call_asadmin("list-jbi-application-variables", component, host, "4848", Config.passfile):
                if "executed successfully." not in str(line) and "Nothing to list" not in str(line):
                    variable = str(line).split("=")[0].replace("b\'", "").replace("b\"", "").replace(" ", "")
                    if variable not in exists_variables:
                        exists_variables.append(variable)
        return exists_variables

    @classmethod
    def findvariables(cls):
        zip_variables = []
        for jarFile in file_operations.match_selection(Config.tempdir, "*jar"):
            jarfile = zipfile.ZipFile(jarFile, 'r')
            with jarfile as target_jar:
                with jarfile.infolist() as filelist:
                    for file in filelist:
                        filename = file.filename
                        with target_jar.open(filename) as opened_file:
                            for line in opened_file:
                                if filename.endswith('.bpel'):
                                    if "literal>" in str(line):
                                        variable = str(line).split("literal")[1].replace(">${", "").replace("}</", "")  # нет желания возиться с регулярками, временный костыль
                                        if variable not in zip_variables:
                                            zip_variables.append(variable)
                                else:
                                    if "${" in str(line):
                                        variable = str(line).split("${")[1].split("}")[0]
                                        if variable not in zip_variables and variable != "HttpDefaultPort" and "\\" not in variable:  # len(variable) < 50:
                                            zip_variables.append(variable)
        return zip_variables
                                    # if "<application-config" in str(line):
                                    #     configuration = str(line).split("\"")[3]
                                    #     if configuration not in configurations and configuration not in new_variables.variables:
                                    #         configurations.append(configuration)


class check_configurations:
    shit2 = []





