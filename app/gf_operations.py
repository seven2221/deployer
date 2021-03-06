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
 asadmin list-jbi-application-configurations --host ms-glass004 --port 7000 --user admin --passwordfile D:\Glassfish22\passfile_test2 --component sun-jms-binding

 '''


def choose_passfile():
    host = session.get('host')
    port = session.get('port')
    testhosts = ['ms-glass004', 'ms-glass006', 'ms-glass018', 'dr-glass016', 'ms-glass017']
    if host == "ms-glass004" and port == "7000":
        passfile = Config.passfile_test2
    elif host == "ms-glass028":
        passfile = Config.passfile_test3
    else:
        if host in testhosts:
            passfile = Config.passfile_test1
        else:
            passfile = Config.passfile
    return passfile


def check_SA():
    statuses = ['started', 'stopped', 'shutdown']
    SAs = {}
    passfile = choose_passfile()
    for status in statuses:
        asadmin_command = subprocess.Popen\
            (
                [
                    "asadmin", "list-jbi-service-assemblies",
                    "--host", session.get('host'),
                    "--port", session.get('port'),
                    "--user", "admin",
                    "--passwordfile", passfile,
                    "--lifecyclestate", status
                ], stdout=subprocess.PIPE, shell=True
            )
        for line in asadmin_command.stdout:
            if "executed successfully." not in str(line) and "Nothing to list" not in str(line):
                SA = str(line).replace("b\'", "").replace("\\r\\n\'", "")
                SAs.update({SA: status})
    return SAs


def undeploy_SA(SA):
    result = ""
    passfile = choose_passfile()
    asadmin_command = subprocess.Popen\
        (
            [
                "asadmin", "undeploy-jbi-service-assembly",
                "--host", session.get('host'),
                "--port", session.get('port'),
                "--user", "admin",
                "--passwordfile", passfile,
                SA
            ], stdout=subprocess.PIPE, shell=True
        )
    for line in asadmin_command.stdout:
        if "Undeployed service assembly" in str(line):
            result = SA + " is successfully undeployed from " + session.get('host')
        else:
            result = result + str(line).replace("\\r\\n\'", "").replace("b\'", "").replace("\n", "")
    return result


def deploy_SA(zip):
    result = ""
    passfile = choose_passfile()
    asadmin_command = subprocess.Popen\
        (
            [
                "asadmin", "deploy-jbi-service-assembly",
                "--host", session.get('host'),
                "--port", session.get('port'),
                "--user", "admin",
                "--passwordfile", passfile,
                Config.zippath + zip
            ], stdout=subprocess.PIPE, shell=True
        )
    for line in asadmin_command.stdout:
        if "executed successfully" in str(line):
            result = zip + " is successfully deployed on " + session.get('host')
        else:
            result = result + str(line).replace("\\r\\n\'", "").replace("b\'", "").replace("\n", "")
    return result


def stop_SA(SA):
    result = ""
    passfile = choose_passfile()
    asadmin_command = subprocess.Popen\
        (
            [
                "asadmin", "stop-jbi-service-assembly",
                "--host", session.get('host'),
                "--port", session.get('port'),
                "--user", "admin",
                "--passwordfile", passfile,
                SA
            ], stdout=subprocess.PIPE, shell=True
        )
    for line in asadmin_command.stdout:
        if "Stopped service assembly" in str(line):
            result = SA + " is successfully stopped"
        else:
            result = result + str(line).replace("\\r\\n\'", "").replace("b\'", "").replace("\n", "")
    return result


def start_SA(SA):
    result = ""
    passfile = choose_passfile()
    asadmin_command = subprocess.Popen\
        (
            [
                "asadmin", "start-jbi-service-assembly",
                "--host", session.get('host'),
                "--port", session.get('port'),
                "--user", "admin",
                "--passwordfile", passfile,
                SA
            ], stdout=subprocess.PIPE, shell=True
        )
    for line in asadmin_command.stdout:
        if "Started service assembly" in str(line):
            result = SA + " is successfully started"
        else:
            result = result + str(line).replace("\\r\\n\'", "").replace("b\'", "").replace("\n", "")
    return result


def shutdown_SA(SA):
    result = ""
    passfile = choose_passfile()
    asadmin_command = subprocess.Popen\
        (
            [
                "asadmin", "shut-down-jbi-service-assembly",
                "--host", session.get('host'),
                "--port", session.get('port'),
                "--user", "admin",
                "--passwordfile", passfile,
                SA
            ], stdout=subprocess.PIPE, shell=True
        )
    for line in asadmin_command.stdout:
        if "Shut Down service assembly" in str(line):
            result = SA + " is successfully shutted down"
        else:
            result = result + str(line).replace("\\r\\n\'", "").replace("b\'", "").replace("\n", "")
    return result

def get_all_variables():
    exists_variables = []
    passfile = choose_passfile()
    for component in Config.GFcomponents:
        asadmin_command = subprocess.Popen\
            (
                [
                    "asadmin", "list-jbi-application-variables",
                    "--host", session.get('host'),
                    "--port", session.get('port'),
                    "--user", "admin",
                    "--passwordfile", passfile,
                    "--component", component
                ], stdout=subprocess.PIPE, shell=True
            )
        for line in asadmin_command.stdout:
            if "executed successfully." not in str(line) and "Nothing to list" not in str(line):
                variable = str(line).split("=")[0].replace("b\'", "").replace("b\"", "").replace(" ", "")#.replace("\\xd0", "").replace("\\xa1", "")
                if variable not in exists_variables:
                    exists_variables.append(variable)
    return exists_variables


def update_variable(component, variable, value):
    passfile = choose_passfile()
    result = ""
    asadmin_command = subprocess.Popen\
        (
            [
                "asadmin", "update-jbi-application-variable",
                "--host", session.get('host'),
                "--port", session.get('port'),
                "--user", "admin",
                "--passwordfile", passfile,
                "--component", component,
                variable + "=" + value
            ], stdout=subprocess.PIPE, shell=True
        )
    for line in asadmin_command.stdout:
        if "executed successfully" in str(line):
            result = "Success"
        else:
            result = result + str(line).replace("\\r\\n\'", "").replace("b\'", "").replace("\n", "")
    return result


def create_variable(component, variable, value):
    result = ""
    passfile = choose_passfile()
    asadmin_command = subprocess.Popen\
        (
            [
                "asadmin", "create-jbi-application-variable",
                "--host", session.get('host'),
                "--port", session.get('port'),
                "--user", "admin",
                "--passwordfile", passfile,
                "--component", component,
                variable + "=" + value
            ], stdout=subprocess.PIPE, shell=True
        )
    for line in asadmin_command.stdout:
        if "executed successfully" in str(line):
            result = "Success"
        else:
            result = result + str(line).replace("\\r\\n\'", "").replace("b\'", "").replace("\n", "")
    return result


def get_all_configurations():
    exists_configurations = []
    passfile = choose_passfile()
    for component in Config.GFcomponents:
        asadmin_command = subprocess.Popen\
            (
                [
                    "asadmin", "list-jbi-application-configurations",
                    "--host", session.get('host'),
                    "--port", session.get('port'),
                    "--user", "admin",
                    "--passwordfile", passfile,
                    "--component", component
                ], stdout=subprocess.PIPE, shell=True
            )
        for line in asadmin_command.stdout:
            if "executed successfully." not in str(line) and "Nothing to list" not in str(line):
                print(str(line))
                configuration = str(line).split("=")[0].replace("b\'", "").replace("b\"", "").replace(" ", "").replace("\\r\\n\'", "")
                print(configuration)
                if configuration not in exists_configurations:
                    exists_configurations.append(configuration)
    print(exists_configurations)
    return exists_configurations


def update_configuration(cls):
    output = []
    passfile = choose_passfile()


def create_configuration(cls):
    output = []
    passfile = choose_passfile()

