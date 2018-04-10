import subprocess
import zipfile
from app import file_operations
from app.config import Config


'''реквесты:
 list-jbi-application-variables
 list-jbi-application-configurations
 list-jbi-service-assemblies
 '''


def call_asadmin(param, request, host, port, passfile):
    if param == "with_comp":
        for component in Config.GFcomponents:
            callrequest = subprocess.Popen(["asadmin", request, "--component", component, "--host", host, "--port", port, "--user", "admin", "--passwordfile", passfile], stdout=subprocess.PIPE, shell=True)
            # print(str(callrequest.stdout))
    elif param == "without_comp":
        callrequest = subprocess.Popen(["asadmin ", request, "  --host  ", host, " --port ", port, " --user ", " admin ", " --passwordfile ", passfile], stdout=subprocess.PIPE, shell=True)
        # print("asadmin  list-jbi-service-assemblies --host" + host + "--port 4848 --user admin --passwordfile D:\\Glassfish22\\passfile")
        # print(str(callrequest.stdout))
    return callrequest.stdout


def check_SA(host):
    SAs = []
    for line in call_asadmin("without_comp",  "list-jbi-service-assemblies", host, "4848", Config.passfile):
        if "executed successfully." not in str(line):
            SA = str(line)
            SAs.append(SA)
    return SAs


class check_variables:
    new_variables = []

    @classmethod
    def find_exists_variables(cls, host):
        exists_variables = []
        for line in call_asadmin("with_comp", "list-jbi-application-variables", host, "4848", Config.passfile):
            if "executed successfully." not in str(line) and "Nothing to list" not in str(line):
                variable = str(line).split("=")[0].replace("b\'", "").replace("b\"", "").replace(" ", "")
                if variable not in exists_variables:
                    # print(variable)
                    exists_variables.append(variable)
        return exists_variables

    # @classmethod
    # def find_zip_variables(cls):
    #     zip_variables = []
    #     for jarFile in file_operations.match_selection(Config.tempdir, "*jar"):
    #         jarfile = zipfile.ZipFile(Config.tempdir + jarFile, 'r')
    #         filelist = jarfile.infolist()
    #         with jarfile.infolist() as filelist:
    #             for file in filelist:
    #                 filename = file.filename
    #                 with jarfile.open(filename) as opened_file:
    #                     for line in opened_file:
    #                         if filename.endswith('.bpel'):
    #                             if "literal>" in str(line):
    #                                 variable = str(line).split("literal")[1].replace(">${", "").replace("}</", "")  # нет желания возиться с регулярками, временный костыль
    #                                 if variable not in zip_variables:
    #                                     zip_variables.append(variable)
    #                         else:
    #                             if "${" in str(line):
    #                                 variable = str(line).split("${")[1].split("}")[0]
    #                                 if variable not in zip_variables and variable != "HttpDefaultPort" and "\\" not in variable:  # len(variable) < 50:
    #                                     zip_variables.append(variable)
    #     return zip_variables
                                    # if "<application-config" in str(line):
                                    #     configuration = str(line).split("\"")[3]
                                    #     if configuration not in configurations and configuration not in new_variables.variables:
                                    #         configurations.append(configuration)

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
                            variable = str(line).split("literal")[1].replace(">${", "").replace("}</", "")  # нет желания возиться с регулярками, временный костыль
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


class check_configurations:
    shit2 = []




