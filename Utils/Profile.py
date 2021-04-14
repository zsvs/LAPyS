"""
This module uses for work with application profile 
"""
import os
from LAPyS.Logging.LAPyS_Logging import Logs

class AplicationProfile: 
    __CREDNTIALS_PATH = os.getenv("USERPROFILE") + "\\LAPyS\\Credential.cred"
    __APP_PATH = os.getenv("USERPROFILE") + "\\LAPyS"
    __Instance = None
    
    def __init__(self):
        """
        ctor. Check if exist profile dir 
        and credentials file. If not then create them.
        """
        if AplicationProfile.__Instance:
            print("Profile instance already existsH", self.GetInstance())

        if not self.CheckProfileDirectoryExist():
            self.__CreateProfileDirectory()
        else:
            Logs.WriteToLog("Profile directory already exists")

        if not self.CheckCredentialFileExist():
            self.__CreateCredentialFile()
        else:
            Logs.WriteToLog("Credential file is exist")
    
    @classmethod
    def GetInstance(cls):
        """
        Creates an unique instance of AplicationProfile class
        """
        if cls.__Instance == None:
            cls.__Instance = AplicationProfile()
        return cls.__Instance 

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

Profile = AplicationProfile().GetInstance() # Create an instance of ApplicationProfile

