import subprocess
import zipfile
from app.config import Config


'''
реквесты:
 list-jbi-application-variables
 list-jbi-application-configurations
 list-jbi-service-assemblies
 update-jbi-application-variable
 create-jbi-application-variable
 '''
# asadmin create-jbi-application-variable --host ms-glass004 --port 4848 --user admin --passwordfile D:\Glassfish22\passfile123 --component sun-bpel-engine test_variable=testtest
# asadmin create-jbi-application-variable --host hostname --port 4848 --user admin --passwordfile D:\Glassfish22\passfile --component sun-bpel-engine SubscriberSMConfigFileDir=D:\\Glassfish22\\domains\\domain1\\config\\SubscriberManagementService\\


def check_SA(host, port):
    SAs = []
    passfile = Config.passfile
    asadmin_command = subprocess.Popen(["asadmin", "list-jbi-service-assemblies", "--host", host, "--port", port, "--user", "admin", "--passwordfile", passfile], stdout=subprocess.PIPE, shell=True)
    for line in asadmin_command.stdout:
        if "executed successfully." not in str(line):
            SA = str(line).replace("b\'", "").replace("\\r\\n\'", "")
            SAs.append(SA)
    return SAs


def get_all_variables(host, port):
    exists_variables = []
    passfile = Config.passfile
    for component in Config.GFcomponents:
        asadmin_command = subprocess.Popen(["asadmin", "list-jbi-application-variables", "--host", host, "--port", port, "--user", "admin", "--passwordfile", passfile, "--component", component], stdout=subprocess.PIPE, shell=True)
        for line in asadmin_command.stdout:
            if "executed successfully." not in str(line) and "Nothing to list" not in str(line):
                variable = str(line).split("=")[0].replace("b\'", "").replace("b\"", "").replace(" ", "")
                if variable not in exists_variables:
                    exists_variables.append(variable)
        return exists_variables


def update_variable(host, port, component, variable, value):
    passfile = Config.passfile
    asadmin_command = subprocess.Popen(["asadmin", "update-jbi-application-variable", "--host", host, "--port", port, "--user", "admin", "--passwordfile", passfile, "--component", component, variable, "=", value], stdout=subprocess.PIPE, shell=True)
    for line in asadmin_command.stdout:
        if "executed successfully" in str(line):
            return "Success"
        else:
            return "Failure"


def create_variable(host, port, component, variable, value):
    passfile = Config.passfile
    asadmin_command = subprocess.Popen(["asadmin", "create-jbi-application-variable", "--host", host, "--port", port, "--user", "admin", "--passwordfile", passfile, "--component", component, variable + "=" + value], stdout=subprocess.PIPE, shell=True)
    for line in asadmin_command.stdout:
        if "executed successfully" in str(line):
            return "Success"
        else:
            return "Failure"


def get_all_configurations(cls):
    exists_configurations = []
    passfile = Config.passfile


def update_configuration(cls):
    output = []
    passfile = Config.passfile


def create_configuration(cls):
    output = []
    passfile = Config.passfile

