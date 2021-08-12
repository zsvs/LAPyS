"""
Module for create GUI by using tkinter libs.
Implements functions for block and clear for TextBoxes
"""

import tkinter as tk
import os
from LAPyS.Logging.LAPyS_Logging import Logs
from LAPyS.Utils.Profile import Profile
from LAPyS.UI.AddIP_Form import AddIpForm
from LAPyS.UI.Form_Class import FormBuilder
import LAPyS.Utils.UserClass as UserClass
import LAPyS.Utils.Factories.UserFactory as Factory
import LAPyS.Encryption.Encryption as Encr
import LAPyS.Network.Network_core as NetCore
from LAPyS.JSON_Classes.Marshaling import JSON
from LAPyS.UI.UserCreation_Error import Creation_Error
import LAPyS.Network.LDAP_Connect as ldap

MainUserFactory = Factory.UserFactory("UserFactory") # Factory for users creation
UsersHashArray = dict() # Associative array for users. 
DataToPost = None

class MainWindow(FormBuilder):
    isButtonPressed = False
    def __init__(self, Name):
        super().__init__(Name)
    
    def __del__(self):
        Logs.WriteToLog("Application killed!")

    def Load(self, Event):
        self.isButtonPressed = True
        self.ClearEntry("EntryUser")
        self.ClearEntry("EntryPassword")
        with open(Profile.GetCredentialPath(), "r") as Cred:
            UsersHashArray["OnFile"] = MainUserFactory.CreateInstance("onLoad", Encr.Coder.Decrypt((Cred.readlines(1))[0].split(",")), Encr.Coder.Decrypt((Cred.readlines(1))[0].split(",")))
            self.SetEntryText("EntryUser",  UsersHashArray["OnFile"].GetName())
            self.SetEntryText("EntryPassword", UsersHashArray["OnFile"].GetPassword())

    def Save(self, Event):
        if UserClass.User.NotNullOrEmpty(self.GetEntryText("EntryUser"), self.GetEntryText("EntryPassword")) and UserClass.User.isAdministrator(self.GetEntryText("EntryUser")):
            self.isButtonPressed = True
            UsersHashArray["OnFile"] = MainUserFactory.CreateInstance("onSave", self.GetEntryText("EntryUser"), self.GetEntryText("EntryPassword"))
            with open(Profile.GetCredentialPath(), "w") as Cred:
                Cred.write(str(Encr.Coder.Encrypt(UsersHashArray["OnFile"].GetName())) + "\n" + str(Encr.Coder.Encrypt(UsersHashArray["OnFile"].GetPassword())))
                Logs.WriteToLog("User saved -> {0}".format(self.isButtonPressed))
        else:
            Logs.WriteToLog("Operation Save failed. Empty user credential fields.")
            self.SetEntryText("EntryUser", "Please enter your login and password")
            
    def GetPassword(self, Event):
        if UserClass.User.NotNullOrEmpty(self.GetEntryText("EntryUser"), self.GetEntryText("EntryPassword")):
            Net = NetCore.CheckNetwork()
       
            if Net == NetCore.socket.herror:
                return None
            OptimalServer = NetCore.GetOptimalServer(JSON.Deserialize(Profile.GetProfilePath() +  "\\SERVERS_POOL.json"))

            if self.isButtonPressed:
                Logs.WriteToLog("Uses credential from file")
                UserContextLocal = UsersHashArray["OnFile"].GetName()
                PasswordContextLocal = UsersHashArray["OnFile"].GetPassword()
                RequestedNameLocal = self.GetEntryText("EntryDomainComputerName")
            else:
                Logs.WriteToLog("Uses entry fields credentials")
                try:
                    UsersHashArray["FromEntry"] = MainUserFactory.CreateInstance("FromEntry", self.GetEntryText("EntryUser"), self.GetEntryText("EntryPassword"))
                    UserContextLocal = UsersHashArray["FromEntry"].GetName()
                    PasswordContextLocal = UsersHashArray["FromEntry"].GetPassword()
                    RequestedNameLocal = self.GetEntryText("EntryDomainComputerName")
                except Exception:
                    Creation_Error(self.GetEntryText("EntryUser"))
                    return None
            
            self.SetEntryText("EntryDomainComputerRML", "")   
            #DataToPost = DataTemplate.DataForm(UserContextLocal, PasswordContextLocal, RequestedNameLocal) 
            if len(RequestedNameLocal) == 0:
                Logs.WriteToLog("Requested name is empty!")
            else:
                Logs.WriteToLog("Requested name -> {0}".format(RequestedNameLocal))

            AD = ldap.get_ldap_info(UserContextLocal, PasswordContextLocal, RequestedNameLocal, OptimalServer)
            AD_Computers = dict() 
            for obj in AD:
                AD_Computers[(str(obj.entry_attributes_as_dict["name"])[2:len(str(obj.entry_attributes_as_dict["name"]))-2])] = str(obj.entry_attributes_as_dict["ms-Mcs-AdmPwd"])[2:len(str(obj.entry_attributes_as_dict["ms-Mcs-AdmPwd"]))-2]

            try:
                self.SetEntryText("EntryDomainComputerRML", AD_Computers[RequestedNameLocal])
            except KeyError:
                self.SetEntryText("EntryDomainComputerRML", "No such name in OU")
                Logs.WriteToLog("No such name in OU")
                Logs.WriteToLog("Connection to LDAP server closed")
            else:
                Logs.WriteToLog("RML successfully returned")
                Logs.WriteToLog("Connection to LDAP server closed")
            #WebClient.SetPayload(DataToPost.GetDataToExchange()) # Sets payload for Post request
            #WebClient.PostRequest() # Sending POST to web-server
        else:
            self.SetEntryText("EntryUser", "Please enter your login and password")

    def Initialize(self):
        self.__MainWindow = tk.Tk()
        self.AddWindowParams(self.__MainWindow, "400x220", False, "LAPyS")

        self.AddWindowLabels(self.__MainWindow, "Enter your domain login:", 100, 25, 250, 15)
        self.AddWindowLabels(self.__MainWindow, "Enter your password:", 100, 65, 250, 20)
        self.AddWindowLabels(self.__MainWindow, "Enter name of computer:", 100, 105, 250, 20)

        self.AddWindowEntry(self.__MainWindow, 100, 45, 250, 20, "EntryUser", None)
        self.AddWindowEntry(self.__MainWindow, 100, 85, 250, 20, "EntryPassword", "*")
        self.AddWindowEntry(self.__MainWindow, 100, 125, 250, 20, "EntryDomainComputerName", None)
        self.AddWindowEntry(self.__MainWindow, 100, 165, 250, 20, "EntryDomainComputerRML", None)

        self.AddButton(self.__MainWindow, "Load", 10, 2, self.Load, 10, 45, 80, 20)
        self.AddButton(self.__MainWindow, "Save", 10, 2, self.Save, 10, 85, 80, 20)
        self.AddButton(self.__MainWindow, "Get Password", 10, 2, self.GetPassword, 10, 125, 80, 20)
        
        self.AddMenu(self.__MainWindow)
        self.AddSubMenu(self.mainMenu, "File")
        self.AddSubMenuCommand("Add IP to pool", lambda: AddIpForm.GetInstance("Add_IP").Initialize(), "File")
        self.AddSubMenuCommand("View server pool", lambda: os.system(Profile.GetProfilePath() +  "\\SERVERS_POOL.json"), "File")
        self.AddSubMenuCommand("Open logs", lambda: os.system(Logs.GetLogFilePath()), "File")
        self.mainMenu.add_cascade(label = "File", menu = self.GetSubMenu("File")) 
        self.__MainWindow.config(menu=self.mainMenu)
        self.__MainWindow.mainloop()
MainWindow("Main").Initialize()