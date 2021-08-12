"""
Basic class for building forms
"""
import tkinter as tk
from LAPyS.Logging.LAPyS_Logging import Logs
from LAPyS.Utils.Profile import Profile
from LAPyS.JSON_Classes.Marshaling import JSON
import os

class FormBuilder:
    __EntryFieldsTextVariablesDict = dict()
    __SubMenuNamesDict = dict()
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

    def AddWindowParams(self, Master, WindowGeometry, WindowResizable, WindowTitle):
        """
        Setting up window params (geometry).
        """
        Master.geometry(WindowGeometry)
        Master.resizable(WindowResizable, WindowResizable)
        Master.title(WindowTitle)

    def AddWindowLabels(self, Master, LabelText, lx, ly, Width, Height):
        """
        Add lebel to window.
        """
        self.Label = tk.Label(Master, text = LabelText)
        self.Label.place(x = lx, y = ly, width = Width, height = Height)
    
    def AddWindowEntry(self, Master, lx, ly, Width, Height, TextVariableName, ShowParams):
        """
        Add entry field to window.
        """
        self.__EntryFieldsTextVariablesDict[TextVariableName] = tk.StringVar()
        self.EntryBox = tk.Entry(Master, textvariable = self.__EntryFieldsTextVariablesDict[TextVariableName])
        self.EntryBox["show"] = ShowParams
        self.EntryBox.place(x = lx, y = ly, width = Width, height = Height)

    def AddButton(self, Master, Text, ButtonWidth, ButtonHeight, BindFunc, lx, ly, Width, Height):
        """
        Add button to window.
        """
        self.Button = tk.Button(Master, text = Text, width = ButtonWidth, height = ButtonHeight, bg="white", fg="black")
        self.Button.bind("<Button-1>", BindFunc)
        self.Button.place(x = lx, y = ly, width = Width, height = Height)

    def AddMenu(self, Master, **kwargs):
        """
        Add menu to Master window.
        You need to adds methods add_command and add_cascade
        """
        self.mainMenu = tk.Menu(Master)
        
    def AddSubMenu(self, MasterMenu, SubMenuName):
        """
        Creating sub menu.
        Store in __SubMenuNamesDict[SubMenuName] 
        """
        self.__SubMenuNamesDict[SubMenuName] = tk.Menu(MasterMenu, tearoff=0)
        
    def AddSubMenuCommand(self, SubMenuLabelText, SubMenuCommand, SubMenuName):
        """
        Add configs to sub menu
        """
        self.__SubMenuNamesDict[SubMenuName].add_command(label = SubMenuLabelText, command = SubMenuCommand)

    def GetSubMenu(self, SubMenuName):
        """
        Retrun SubMenu from from SubMenuDict
        """
        return self.__SubMenuNamesDict[SubMenuName]

    def GetEntryText(self, TextVariable):
        """
        Return entry TextVariable from dict.
        """
        return self.__EntryFieldsTextVariablesDict[TextVariable].get()
    
    def ClearEntry(self, TextVariable):
        """
        Clear value/text in TextVariable.
        """
        self.__EntryFieldsTextVariablesDict[TextVariable].set("")    

    def SetEntryText(self, TextVariable, Text):
        """
        Setting up text to entry with TextVariable
        """
        self.__EntryFieldsTextVariablesDict[TextVariable].set(Text)

    def Initialize(self):
        """
        Build new window.
        You may sets your params, and add fields that you want.
        Example:
        #self.<Your_window_name> = tk.Tk()
        #self.AddWindowParams(<Your_window_name>, "160x115", False, "Server addition")
        #self.AddWindowLabels(<Your_window_name>, "Server name:", 10, 5, 130, 20)
        #self.AddWindowLabels(<Your_window_name>, "IPv4 Address:", 10, 44, 130, 20)
        #self.AddWindowEntry(<Your_window_name>, 10, 25, 130, 20, "ServerName")
        #self.AddWindowEntry(<Your_window_name>, 10, 65, 130, 20, "ServerIP")
        #self.AddButton(<Your_window_name>, "Add", 10, 2, self.AddServer, 10, 90, 130, 20)
        #self.<Your_window_name>.mainloop()
        """
        pass
