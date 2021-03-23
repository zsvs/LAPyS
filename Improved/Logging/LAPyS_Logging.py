import os
import datetime

def WriteToLog(Text):
    TIME = datetime.datetime.now()
    FILE_PATH = os.getenv("USERPROFILE") + "\\LAPyS Log\\Log.log"
    with open(FILE_PATH, "a") as LogFile:
        LogFile.write(str(TIME) + ": " + Text + "\n")