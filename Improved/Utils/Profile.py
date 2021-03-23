import os
import LAPyS.Logging.LAPyS_Logging as Log

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
