@echo off
REM
REM Copyright 2004-2005 Sun Microsystems, Inc. All rights reserved.
REM Use is subject to license terms.
REM

setlocal
call "D:\GlassFish22\config\asenv.bat"
set Path=%AS_INSTALL%\bin;%AS_ICU_LIB%;%PATH%

"%AS_JAVA%\bin\java" -Dcom.sun.aas.instanceName=server -Djava.library.path="%AS_INSTALL%\bin";"%AS_ICU_LIB%" -Dcom.sun.aas.configRoot="%AS_CONFIG%" -Djava.endorsed.dirs="%AS_INSTALL%\lib\endorsed" -Dcom.sun.aas.processLauncher="SE" -cp "%AS_DERBY_INSTALL%\lib\derby.jar";"%AS_INSTALL%\jbi\lib\jbi-admin-cli.jar";"%AS_INSTALL%\jbi\lib\jbi-admin-common.jar";"%AS_INSTALL%\lib\comms-appserv-rt.jar";"%AS_INSTALL%\lib\comms-appserv-api.jar";"%AS_INSTALL%\lib\appserv-rt.jar";"%AS_INSTALL%\lib\appserv-ext.jar";"%AS_INSTALL%\lib\javaee.jar";"%AS_INSTALL%\lib\appserv-se.jar";"%AS_INSTALL%\lib\comms-appserv-admin-cli.jar";"%AS_INSTALL%\lib\admin-cli.jar";"%AS_INSTALL%\lib\appserv-admin.jar";"%AS_INSTALL%\lib\commons-launcher.jar";"%AS_INSTALL%\lib\install\applications\jmsra\imqjmsra.jar" -Dcom.sun.appserv.admin.pluggable.features=com.sun.enterprise.ee.admin.pluggable.EEClientPluggableFeatureImpl com.sun.enterprise.cli.framework.CLIMain  %*
endlocal
