"""
Basic class for building forms
"""
import tkinter as tk
#import sys
#sys.path.append("C:\\Users\\stepa\\Documents\\Repositories\\LAPyS")
from Logging.LAPyS_Logging import Logs
from Utils.Profile import Profile
from JSON_Classes.Marshaling import JSON
import os

class FormBuilder:
    __EntryFieldsTextVariablesDict = dict()
    __Name = None

    def __init__(self, Name):
        __Name = Name
        Logs.WriteToLog("Form {0} created".format(Name))
        print("Form {0} created".format(Name))


    def CustomEvent(self, Event):
        """
        Add your event here.
        """
        pass

    def AddWindowParams(self, WindowGeometry, WindowResizable, WindowTitle):
        """
        Setting up window params (geometry).
        """
        self.__AddIpWindow.geometry(WindowGeometry)
        self.__AddIpWindow.resizable(WindowResizable, WindowResizable)
        self.__AddIpWindow.title(WindowTitle)

    def AddWindowLabels(self, Master, LabelText, lx, ly, Width, Height):
        """
        Add lebel to window.
        """
        self.Label = tk.Label(Master, text = LabelText)
        self.Label.place(x = lx, y = ly, width = Width, height = Height)
    
    def AddWindowEntry(self, Master, lx, ly, Width, Height, TextVariableName):
        """
        Add entry field to window.
        """
        self.__EntryFieldsTextVariablesDict[TextVariableName] = tk.StringVar()
        self.EntryBox = tk.Entry(Master, textvariable  = self.__EntryFieldsTextVariablesDict[TextVariableName])
        self.EntryBox.place(x = lx, y = ly, width = Width, height = Height)

    def AddButton(self, Master, Text, ButtonWidth, ButtonHeight, BindFunc, lx, ly, Width, Height):
        """
        Add button to window.
        """
        self.Button = tk.Button(Master, text = Text, width = ButtonWidth, height = ButtonHeight, bg="white", fg="black")
        self.Button.bind("<Button-1>", BindFunc)
        self.Button.place(x = lx, y = ly, width = Width, height = Height)

    def __GetEntryText(self, TextVariable):
        """
        Return entry TextVariable from dict.
        """
        return self.__EntryFieldsTextVariablesDict[TextVariable].get()
    
    def __ClearEntry(self, TextVariable):
        """
        Clear value/text in TextVariable.
        """
        self.__EntryFieldsTextVariablesDict[TextVariable].set("")    

    def Initialize(self):
        """
        Build new window.
        You may sets your params, and add fields that you want.
        """
        self.__AddIpWindow = tk.Tk()

        ###!Example!###
        #self.AddWindowParams("160x115", False, "Server addition")
        #self.AddWindowLabels(self.__AddIpWindow, "Server name:", 10, 5, 130, 20)
        #self.AddWindowLabels(self.__AddIpWindow, "IPv4 Address:", 10, 44, 130, 20)
        #self.AddWindowEntry(self.__AddIpWindow, 10, 25, 130, 20, "ServerName")
        #self.AddWindowEntry(self.__AddIpWindow, 10, 65, 130, 20, "ServerIP")
        #self.AddButton(self.__AddIpWindow, "Add", 10, 2, self.AddServer, 10, 90, 130, 20)

        self.__AddIpWindow.mainloop()