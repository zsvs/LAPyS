import os
import datetime
"""
Provides logging for LAPyS project.
"""
__LOG_DIR_PATH = os.getenv("USERPROFILE") + "\\LAPyS Log" #Save path to Logs directory

def WriteToLog(Text):
    """
    Write <Text> params to file that
    lying at path of __LOG_DIR_PATH
    """
    TIME = datetime.datetime.now()
    FILE_PATH = __LOG_DIR_PATH + "\\Log.log"
    with open(FILE_PATH, "a") as LogFile:
        LogFile.write(str(TIME) + ": " + Text + "\n")