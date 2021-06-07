"""
Additional form for user servers input
"""
import tkinter as tk
from LAPyS.Logging.LAPyS_Logging import Logs
from LAPyS.Utils.Profile import Profile
from LAPyS.JSON_Classes.Marshaling import JSON
from LAPyS.UI.Form_Class import FormBuilder
import os

class AddIpForm(FormBuilder):
    __Instance = None
    __EntryFieldsTextVariablesDict = dict()

    def __init__(self, Name):
        super().__init__(Name)
        if AddIpForm.__Instance:
            print("Instance already created", self.GetInstance(Name))

    def AddServer(self, Event):
        Pool = JSON.Deserialize(Profile.GetProfilePath() +  "\\SERVERS_POOL.json")
        Pool[self.GetEntryText("ServerName")] = self.GetEntryText("ServerIP")
        with open(Profile.GetProfilePath() +  "\\SERVERS_POOL.json", "w") as ServerPoolFile:
            ServerPoolFile.write(JSON.Serialize(Pool))
            Logs.WriteToLog("Added " + self.GetEntryText("ServerName") + " to servers pool")
        self.ClearEntry("ServerName")
        self.ClearEntry("ServerIP")
    
    @classmethod
    def GetInstance(cls, Name):
        if cls.__Instance == None:
            cls.__Instance = AddIpForm(Name)
        return cls.__Instance 

    def Initialize(self):
        self.__Window = tk.Tk()
        self.AddWindowParams(self.__Window, "160x115", False, "Server addition")
        self.AddWindowLabels(self.__Window, "Server name:", 10, 5, 130, 20)
        self.AddWindowLabels(self.__Window, "IPv4 Address:", 10, 44, 130, 20)
        self.AddWindowEntry(self.__Window, 10, 25, 130, 20, "ServerName", None)
        self.AddWindowEntry(self.__Window, 10, 65, 130, 20, "ServerIP", None)
        self.AddButton(self.__Window, "Add", 10, 2, self.AddServer, 10, 90, 130, 20)
        self.__Window.mainloop()

#! print("Hello", AddIpForm.GetInstance().Initialize())