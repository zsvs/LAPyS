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
        Pool[self.__GetEntryText("ServerName")] = self.__GetEntryText("ServerIP")
        with open(Profile.GetProfilePath() +  "\\SERVERS_POOL.json", "w") as ServerPoolFile:
            ServerPoolFile.write(JSON.Serialize(Pool))
            Logs.WriteToLog("Added " + self.__GetEntryText("ServerName") + " to servers pool")
        self.__ClearEntry("ServerName")
        self.__ClearEntry("ServerIP")
    
    @classmethod
    def GetInstance(cls, Name):
        if cls.__Instance == None:
            cls.__Instance = AddIpForm(Name)
        return cls.__Instance

    def AddWindowParams(self, WindowGeometry, WindowResizable, WindowTitle):
        self.__AddIpWindow.geometry(WindowGeometry)
        self.__AddIpWindow.resizable(WindowResizable, WindowResizable)
        self.__AddIpWindow.title(WindowTitle)

    def AddWindowLabels(self, Master, LabelText, lx, ly, Width, Height):
        self.Label = tk.Label(Master, text = LabelText)
        self.Label.place(x = lx, y = ly, width = Width, height = Height)
    
    def AddWindowEntry(self, Master, lx, ly, Width, Height, TextVariableName):
        self.__EntryFieldsTextVariablesDict[TextVariableName] = tk.StringVar()
        self.EntryBox = tk.Entry(Master, textvariable  = self.__EntryFieldsTextVariablesDict[TextVariableName])
        self.EntryBox.place(x = lx, y = ly, width = Width, height = Height)

    def AddButton(self, Master, Text, ButtonWidth, ButtonHeight, BindFunc, lx, ly, Width, Height):
        self.Button = tk.Button(Master, text = Text, width = ButtonWidth, height = ButtonHeight, bg="white", fg="black")
        self.Button.bind("<Button-1>", BindFunc)
        self.Button.place(x = lx, y = ly, width = Width, height = Height)

    def __GetEntryText(self, TextVariable):
        return self.__EntryFieldsTextVariablesDict[TextVariable].get()
    
    def __ClearEntry(self, TextVariable):
        self.__EntryFieldsTextVariablesDict[TextVariable].set("")    

    def Initialize(self):
        self.__AddIpWindow = tk.Tk()
        self.AddWindowParams("160x115", False, "Server addition")
        self.AddWindowLabels(self.__AddIpWindow, "Server name:", 10, 5, 130, 20)
        self.AddWindowLabels(self.__AddIpWindow, "IPv4 Address:", 10, 44, 130, 20)
        self.AddWindowEntry(self.__AddIpWindow, 10, 25, 130, 20, "ServerName")
        self.AddWindowEntry(self.__AddIpWindow, 10, 65, 130, 20, "ServerIP")
        self.AddButton(self.__AddIpWindow, "Add", 10, 2, self.AddServer, 10, 90, 130, 20)
        self.__AddIpWindow.mainloop()

#! print("Hello", AddIpForm.GetInstance().Initialize())