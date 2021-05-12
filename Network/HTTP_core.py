"""
Class to work with web-server
"""

import requests
from LAPyS.JSON_Classes.Marshaling import JSON # Get instance of Marshaling class
from LAPyS.Logging.LAPyS_Logging import Logs # Get instance of Logger class

class HTTPClient:
    __Payload = None
    __Headers = None
    __URL ="http://10.6.0.229:65065/some/post"
    __Answer = None

    def __init__(self):
        self.__Headers = {  
                            "Content-type": "application/json",
                            "Accept": "*/*",
                            "User-Agent" : "Python_Client",
                            "Content-Encoding": "utf-8" 
                        }
    
    def SetPayload(self, Data):
        """
        Setting up HTTP payload.
        Mandatory attribute <Data>, preferred to be a dict()
        """
        self.__Payload = JSON.Serialize(Data)

    def GetPayload(self):
        """
        Getting active request payload
        """
        return self.__Payload

    def PostRequest(self):
        """
        Sending POST request to web-server
        """
        if self.__Payload: 
            self.__Answer = requests.post(self.__URL, data = self.__Payload, headers = self.__Headers)
            Logs.WriteToLog("Data transited to web server")
        else:
            Logs.WriteToLog("No payload in HTTP request")
            raise Exception("Payload must be setted")
    
    def GetAnswer(self):
        """
        Returns HTTP code of response
        """
        return self.__Answer

WebClient = HTTPClient()
