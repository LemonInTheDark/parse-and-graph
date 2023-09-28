@ECHO OFF

SET CONFIGFOLDER=root\config\
SET TEMPLATEPATH=%CONFIGFOLDER%_template.json
SET CONFIGPATH=%CONFIGFOLDER%header_config.json

IF EXIST %CONFIGPATH% (
    ECHO Config already exists, skipping.
) ELSE (
    ECHO No config found, copying default...
    COPY %TEMPLATEPATH% %CONFIGPATH%
)

ECHO Installing pip dependencies...
py -3.6 -m pip install requests

PAUSE