import os
from LAPyS.Logging.LAPyS_Logging import Logs
"""
This module uses for create and check if profile is exist
CREDNTIALS_PATH contains the full path to credentials file
"""

class AplicationProfile:
    __CREDNTIALS_PATH = os.getenv("USERPROFILE") + "\\LAPyS\\Credential.cred"
    __APP_PATH = os.getenv("USERPROFILE") + "\\LAPyS"

    def __init__(self):
        """
        ctor check if exist profile dir 
        and credentials file. If not then create them.
        """
        if not self.CheckProfileDirectoryExist():
            self.__CreateProfileDirectory()
        else:
            Logs.WriteToLog("Profile directory already exists")

        if not self.CheckCredentialFileExist():
            self.__CreateCredentialFile()
        else:
            Logs.WriteToLog("Credential file is exist")

    def __CreateProfileDirectory(self):
        """
        Creates profile directory
        """
        os.mkdir(self.__APP_PATH)
        Logs.WriteToLog("Profile directory created")
        
    def CheckProfileDirectoryExist(self):
        """
        Return <True> if profile dir exist
        """
        return os.path.exists(self.__APP_PATH)

    def __CreateCredentialFile(self):
        """
        Creates credentials file
        """
        f = open(self.__CREDNTIALS_PATH, "w")
        f.close
        Logs.WriteToLog("Credential file created")
    
    def CheckCredentialFileExist(self):
        """
        Return <True> if credentials file exist
        """
        return os.path.exists(self.__CREDNTIALS_PATH)
        
    def GetCredentialPath(self):
        """
        Return full path to credentials file
        """
        return self.__CREDNTIALS_PATH

    def GetProfilePath(self):
        """
        Return full path to profile dir
        """
        return self.__APP_PATH

Profile = AplicationProfile()

