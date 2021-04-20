"""
Module provides simple class that store 
data which must be posted to web-server
"""
from datetime import datetime as dt

class DataForm:
    __DataTemplate = None

    def __init__(self, UserName, Password, RequestedName):
        self.__DataTemplate = { 
                                    "UserName" :  UserName,
                                    "Password" : Password,
                                    "RequestedName" : RequestedName,
                                    "Date" :  str(dt.now())
                                }

    def GetDataToExchange(self):
        return self.__DataTemplate


