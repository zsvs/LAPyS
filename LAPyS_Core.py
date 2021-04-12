import os
import LAPyS.UI.MainForm as Form
import LAPyS.Network.Network_core as NetCore
import LAPyS.Network.LDAP_Connect as ldap
import LAPyS.Encryption.Encryption as Encr
from LAPyS.Utils.Profile import Profile
from LAPyS.Logging.LAPyS_Logging import Logs
from LAPyS.JSON_Classes.Marshaling import JSON
from LAPyS.UI.UserCreation_Error import Creation_Error
import LAPyS.Utils.UserClass as UserClass

User_OnLoad = None
User_OnSave = None
User_FromEntry = None

STATE_FLAG = False

def Load(Event):
    global STATE_FLAG, User_OnLoad
    STATE_FLAG = True
    Form.onLoad_ClearFields()
    with open(Profile.GetCredentialPath(), "r") as Cred:
        User_OnLoad = UserClass.User(ObjectName = "onLoad", Name = Encr.Decrypt((Cred.readlines(1))[0].split(",")), Password = Encr.Decrypt((Cred.readlines(1))[0].split(",")) )
        Form.TextBoxUserContext.insert(0, User_OnLoad.GetName())
        Form.TextBoxPasswordContext.insert(0, User_OnLoad.GetPassword())
        Logs.WriteToLog("Profile loaded from file Credential.cred -> {0}".format(STATE_FLAG))

def Save(Event):
    global STATE_FLAG, User_OnSave
    if UserClass.User.NotNullOrEmpty(Form.TextBoxUserContext.get(), Form.TextBoxPasswordContext.get()) and UserClass.User.isAdministrator(Form.TextBoxUserContext.get()):
        STATE_FLAG = True
        with open(Profile.GetCredentialPath(), "w") as Cred:
            User_OnSave = UserClass.User(ObjectName = "onSave", Name = Form.TextBoxUserContext.get(), Password = Form.TextBoxPasswordContext.get())
            Cred.write(str(Encr.Encrypt(Form.TextBoxUserContext.get())) + "\n" + str(Encr.Encrypt(Form.TextBoxPasswordContext.get())))
            Logs.WriteToLog("Profile saved from entry fields -> {0}".format(STATE_FLAG))
    else: 
        Logs.WriteToLog("Operation Save failed. Empty user credential fields.")
        Form.TextBoxUserContext.insert(0,"Please enter your login and password")

def GetPassword(Event):
    if UserClass.User.NotNullOrEmpty(Form.TextBoxUserContext.get(), Form.TextBoxPasswordContext.get()):
        Net = NetCore.CheckNetwork()
       
        if Net == NetCore.socket.herror:
            return None
        SRV = JSON.Deserialize(Profile.GetProfilePath() +  "\\SERVERS_POOL.json")
        OptimalServer = NetCore.GetOptimalServer(SRV)

        if STATE_FLAG:
            Logs.WriteToLog("Uses credential from file")
        else:
            Logs.WriteToLog("Uses entry fields credentials")
            try:
                User_FromEntry = UserClass.User(ObjectName = "FromEntryFields", Name = Form.TextBoxUserContext.get(), Password = Form.TextBoxPasswordContext.get())
            except Exception:
                Creation_Error(Form.TextBoxUserContext.get())
                return None

        Form.TextBoxDomainComputerRML.delete(0, "end")
        UserContextLocal = User_FromEntry.GetName()
        PasswordContextLocal = User_FromEntry.GetPassword() 

        RequestedNameLocal = Form.TextBoxDomainComputerName.get()

        if len(RequestedNameLocal) == 0:
            Logs.WriteToLog("Requested name is empty!")
        else:
            Logs.WriteToLog("Requested name -> {0}".format(RequestedNameLocal))

        AD = ldap.get_ldap_info(UserContextLocal, PasswordContextLocal, RequestedNameLocal, OptimalServer)
        AD_Computers = dict() #TODO Think about creates global dict to store all results for improving speed of searching.
        for obj in AD:
	        AD_Computers[(str(obj.entry_attributes_as_dict["name"])[2:len(str(obj.entry_attributes_as_dict["name"]))-2])] = str(obj.entry_attributes_as_dict["ms-Mcs-AdmPwd"])[2:len(str(obj.entry_attributes_as_dict["ms-Mcs-AdmPwd"]))-2]

        try:
            Form.TextBoxDomainComputerRML.insert(0, AD_Computers[RequestedNameLocal])
        except KeyError:
            Form.TextBoxDomainComputerRML.insert(0, "No such name in OU")
            Logs.WriteToLog("No such name in OU")
            Logs.WriteToLog("Connection to LDAP server closed")
        else:
            Logs.WriteToLog("RML successfully returned")
            Logs.WriteToLog("Connection to LDAP server closed")
    else:
        Form.TextBoxUserContext.insert(0,"Please enter your login and password")
        Form.TextBoxDomainComputerRML.insert(0,"Please enter your login and password")
