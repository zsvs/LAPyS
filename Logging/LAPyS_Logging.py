import os
import datetime
"""
Provides logging for LAPyS project.
"""


class Logger:
    __Instance = None # Stores instance of class 
    __LOG_DIR_PATH = os.getenv("USERPROFILE") + "\\LAPyS" # Save path to Logs directory
    __FILE_PATH = __LOG_DIR_PATH + "\\Logs.log" # Save path to Log file

    def __init__(self):
        if Logger.__Instance:
            print("Instance already created", self.GetInstance())
    
    @classmethod
    def GetInstance(cls):
        """
        Creates an unique instance of Logger class
        """
        if cls.__Instance == None:
            cls.__Instance = Logger()
        return cls.__Instance

    def GetLogFilePath(self):
        """
        Returns path to log file
        """
        return self.__FILE_PATH

    def WriteToLog(self, Text):
        """
        Write <Text> params to file that
        lying at path of __LOG_DIR_PATH
        """
        TIME = datetime.datetime.now()
        with open(self.__FILE_PATH, "a") as LogFile:
            LogFile.write(str(TIME) + ": " + Text + "\n")

Logs = Logger().GetInstance() # Create an instance of logger

