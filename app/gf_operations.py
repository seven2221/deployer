import subprocess
from app.config import Config
from flask import session


'''
 list-jbi-application-variables
 list-jbi-application-configurations
 list-jbi-service-assemblies
 update-jbi-application-variable
 create-jbi-application-variable
 
 asadmin create-jbi-application-variable --host ms-glass004 --port 4848 --user admin --passwordfile D:\Glassfish22\passfile123 --component sun-bpel-engine test_variable=testtest
 asadmin create-jbi-application-variable --host hostname --port 4848 --user admin --passwordfile D:\Glassfish22\passfile --component sun-bpel-engine SubscriberSMConfigFileDir=D:\\Glassfish22\\domains\\domain1\\config\\SubscriberManagementService\\
 asadmin shut-down-jbi-service-assembly --user admin --host ms-glass010 --port 4848 --passwordfile D:\GlassFish22\passfile SharedDataWeb
 '''


def choose_passfile():
    host = session.get('host')
    port = session.get('port')
    testhosts = ['ms-glass004', 'ms-glass006', 'ms-glass018', 'dr-glass016']
    if host == "ms-glass004" and port == "7000":
        passfile = Config.passfile_test2
    else:
        if host in testhosts:
            passfile = Config.passfile_test1
        else:
            passfile = Config.passfile
    return passfile


def check_SA(host, port):
    SAs = []
    passfile = choose_passfile()
    asadmin_command = subprocess.Popen\
        (
            [
                "asadmin", "list-jbi-service-assemblies",
                "--host", host,
                "--port", port,
                "--user", "admin",
                "--passwordfile", passfile
            ], stdout=subprocess.PIPE, shell=True
        )
    for line in asadmin_command.stdout:
        if "executed successfully." not in str(line):
            SA = str(line).replace("b\'", "").replace("\\r\\n\'", "")
            SAs.append(SA)
    return SAs


def undeploy_SA(host, port, SA):
    passfile = choose_passfile()
    asadmin_command = subprocess.Popen\
        (
            [
                "asadmin", "undeploy-jbi-service-assembly",
                "--host", host,
                "--port", port,
                "--user", "admin",
                "--passwordfile", passfile,
                "--target", SA
            ], stdout=subprocess.PIPE, shell=True
        )
    for line in asadmin_command.stdout:
        if "executed successfully" in str(line):
            return "Success"
        else:
            return str(line).replace("\\r\\n\'", "").replace("b\'", "")


def deploy_SA(host, port, zip):
    out = []


def get_all_variables(host, port):
    exists_variables = []
    passfile = choose_passfile()
    for component in Config.GFcomponents:
        asadmin_command = subprocess.Popen\
            (
                [
                    "asadmin", "list-jbi-application-variables",
                    "--host", host,
                    "--port", port,
                    "--user", "admin",
                    "--passwordfile", passfile,
                    "--component", component
                ], stdout=subprocess.PIPE, shell=True
            )
        for line in asadmin_command.stdout:
            if "executed successfully." not in str(line) and "Nothing to list" not in str(line):
                variable = str(line).split("=")[0].replace("b\'", "").replace("b\"", "").replace(" ", "")
                if variable not in exists_variables:
                    exists_variables.append(variable)
        return exists_variables


def update_variable(host, port, component, variable, value):
    passfile = choose_passfile()
    asadmin_command = subprocess.Popen\
        (
            [
                "asadmin", "update-jbi-application-variable",
                "--host", host,
                "--port", port,
                "--user", "admin",
                "--passwordfile", passfile,
                "--component", component,
                variable + "=" + value
            ], stdout=subprocess.PIPE, shell=True
        )
    for line in asadmin_command.stdout:
        if "executed successfully" in str(line):
            return "Success"
        else:
            return str(line).replace("\\r\\n\'", "").replace("b\'", "")


def create_variable(host, port, component, variable, value):
    passfile = choose_passfile()
    asadmin_command = subprocess.Popen\
        (
            [
                "asadmin", "create-jbi-application-variable",
                "--host", host,
                "--port", port,
                "--user", "admin",
                "--passwordfile", passfile,
                "--component", component,
                variable + "=" + value
            ], stdout=subprocess.PIPE, shell=True
        )
    for line in asadmin_command.stdout:
        if "executed successfully" in str(line):
            return "Success"
        else:
            return str(line).replace("\\r\\n\'", "").replace("b\'", "")


def get_all_configurations(cls):
    exists_configurations = []
    passfile = choose_passfile()


def update_configuration(cls):
    output = []
    passfile = choose_passfile()


def create_configuration(cls):
    output = []
    passfile = choose_passfile()

