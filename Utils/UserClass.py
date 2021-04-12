from LAPyS.Logging.LAPyS_Logging import Logs

"""
Module provides cheking user inputs
"""
class User:
    ObjectName = "Deffault"
    __Name = None
    __Password = None

    def __init__(self,**kwargs): # Default ctor
        """
        You can use keyword arguments 
        for setting <ObjectName>, <Name> and <Password>
        """
        self.ObjectName = kwargs.get("ObjectName")
        if not str(kwargs.get("Name")).startswith("sa"):
            Logs.WriteToLog("{0} is not administrator!".format(kwargs.get("Name")))
            raise Exception("User is not administrator")
        else:
            self.__Name = kwargs.get("Name")
        self.__Password = kwargs.get("Password")
    
    def SetName(self, Name):
        """
        Sets <Name> field
        """
        self.__Name = Name

    def SetObjectName(self, ObjectName):
        """
        Setting up <ObjectName> field
        """
        self.ObjectName = ObjectName
    
    def GetObjectName(self):
        """
        Returns <ObjectName> field
        """       
        return self.ObjectName

    def SetPassword(self, Password):
        """
        Sets <Password> field
        """
        self.__Password = Password

    def GetName(self):
        """
        Returns user name
        """
        return self.__Name

    def GetPassword(self):
        """
        Returns user password
        """
        return self.__Password       
    
    @staticmethod
    def NotNullOrEmpty(UserName, Password):
        """
        If credentials is empty return <True>
        """
        if len(UserName) == 0 or len(Password) == 0 or UserName == None or Password == None:
            return False
        else: 
            return True

    @staticmethod
    def isAdministrator(UserName):
        """
        if UserName starts with <sa> return <True>
        """
        if UserName.startswith("sa"):
            return True
        else:
            return False
