import os
import LAPyS.Logging.LAPyS_Logging as Log
"""
This module uses for create and check if profile is exist
CREDNTIALS_PATH contains the full path to credentials file
"""
__CREDNTIALS_PATH = os.getenv("USERPROFILE") + "\\LAPyS Log\\Credential.cred"

try:
    try:
        Log.WriteToLog("Start checking profile directory")
    except FileNotFoundError:
        os.mkdir(os.getenv("USERPROFILE") + "\\LAPyS Log")
        Log.WriteToLog("Profile directory created")
    else:
        Log.WriteToLog("Profile directory already exists")
except FileExistsError:
    Log.WriteToLog("Profile directory already exists")

try:
    Log.WriteToLog("Check if credential file is exist")
    f = open(__CREDNTIALS_PATH, "r")
    f.close
    Log.WriteToLog("Credential file is exist")
except FileNotFoundError:
    f = open(__CREDNTIALS_PATH, "w")
    Log.WriteToLog("Credential file created")
    f.close

