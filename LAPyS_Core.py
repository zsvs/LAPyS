import os
import LAPyS.UI.MainForm as Form
import LAPyS.Network.Network_core as NetCore
import LAPyS.Network.LDAP_Connect as ldap
import LAPyS.Encryption.Encryption as Encr
from LAPyS.Utils.Profile import Profile
from LAPyS.Logging.LAPyS_Logging import Logs
from LAPyS.JSON_Classes.Marshaling import JSON
from LAPyS.UI.UserCreation_Error import Creation_Error
from LAPyS.Network.HTTP_core import WebClient
import LAPyS.JSON_Classes.DataTemplate as DataTemplate
import LAPyS.Utils.UserClass as UserClass

User_OnFile = None
User_FromEntry = None
DataToPost = None

STATE_FLAG = False

def Load(Event):
    global STATE_FLAG, User_OnFile
    STATE_FLAG = True
    Form.onLoad_ClearFields()
    with open(Profile.GetCredentialPath(), "r") as Cred:
        User_OnFile = UserClass.User(ObjectName = "onLoad", Name = Encr.Coder.Decrypt((Cred.readlines(1))[0].split(",")), Password = Encr.Coder.Decrypt((Cred.readlines(1))[0].split(",")) )
        Form.TextBoxUserContext.insert(0, User_OnFile.GetName())
        Form.TextBoxPasswordContext.insert(0, User_OnFile.GetPassword())
        Logs.WriteToLog("Profile loaded from file Credential.cred -> {0}".format(STATE_FLAG))

def Save(Event):
    global STATE_FLAG, User_OnFile
    if UserClass.User.NotNullOrEmpty(Form.TextBoxUserContext.get(), Form.TextBoxPasswordContext.get()) and UserClass.User.isAdministrator(Form.TextBoxUserContext.get()):
        STATE_FLAG = True
        User_OnFile = UserClass.User(ObjectName = "onSave", Name = Form.TextBoxUserContext.get(), Password = Form.TextBoxPasswordContext.get())
        with open(Profile.GetCredentialPath(), "w") as Cred:
            Cred.write(str(Encr.Coder.Encrypt(Form.TextBoxUserContext.get())) + "\n" + str(Encr.Coder.Encrypt(Form.TextBoxPasswordContext.get())))
            Logs.WriteToLog("Profile saved from entry fields -> {0}".format(STATE_FLAG))
    else: 
        Logs.WriteToLog("Operation Save failed. Empty user credential fields.")
        Form.TextBoxUserContext.insert(0,"Please enter your login and password")
        
def GetPassword(Event):
    if UserClass.User.NotNullOrEmpty(Form.TextBoxUserContext.get(), Form.TextBoxPasswordContext.get()):
        Net = NetCore.CheckNetwork()
       
        if Net == NetCore.socket.herror:
            return None
        OptimalServer = NetCore.GetOptimalServer(JSON.Deserialize(Profile.GetProfilePath() +  "\\SERVERS_POOL.json"))

        if STATE_FLAG:
            Logs.WriteToLog("Uses credential from file")
            UserContextLocal = User_OnFile.GetName()
            PasswordContextLocal = User_OnFile.GetPassword()
            RequestedNameLocal = Form.TextBoxDomainComputerName.get()
        else:
            Logs.WriteToLog("Uses entry fields credentials")
            try:
                User_FromEntry = UserClass.User(ObjectName = "FromEntryFields", Name = Form.TextBoxUserContext.get(), Password = Form.TextBoxPasswordContext.get())
                UserContextLocal = User_FromEntry.GetName()
                PasswordContextLocal = User_FromEntry.GetPassword()
                RequestedNameLocal = Form.TextBoxDomainComputerName.get()
            except Exception:
                Creation_Error(Form.TextBoxUserContext.get())
                return None

        Form.TextBoxDomainComputerRML.delete(0, "end")     
        DataToPost = DataTemplate.DataForm(UserContextLocal, PasswordContextLocal, RequestedNameLocal) 
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
        WebClient.SetPayload(DataToPost.GetDataToExchange()) # Sets payload for Post request
        WebClient.PostRequest() # Sending POST to web-server
    else:
        Form.TextBoxUserContext.insert(0,"Please enter your login and password")
        Form.TextBoxDomainComputerRML.insert(0,"Please enter your login and password")
