import os
import LAPyS.UI.MainForm as Form
from LAPyS.Utils.Profile import Profile
import LAPyS.Logging.LAPyS_Logging as Log
import LAPyS.Network.Network_core as NetCore
import LAPyS.Network.LDAP_Connect as ldap
import LAPyS.Utils.CheckUserCred as UserCred
import LAPyS.Encryption.Encryption as Encr
import LAPyS.JSON_Classes.Marshaling as Marsh

STATE_FLAG = False
Logs = Log.Logger().GetInstance()

def Load(Event):
    global STATE_FLAG
    STATE_FLAG = True
    with open(Profile.GetCredentialPath(), "r") as Cred:
        DECODED_NAME = Cred.readlines(1)
        DECODED_PASSW = Cred.readlines(1)
        Form.TextBoxUserContext.insert(0, Encr.Decrypt(DECODED_NAME[0].split(",")))
        Form.TextBoxPasswordContext.insert(0, Encr.Decrypt(DECODED_PASSW[0].split(",")))
        Logs.WriteToLog("Profile loaded from file Credential.cred -> {0}".format(STATE_FLAG))
    Form.OnLoadPressed()

def Save(Event):
    global STATE_FLAG
    if UserCred.NotNullOrEmpty(Form.TextBoxUserContext.get(), Form.TextBoxPasswordContext.get()) and UserCred.isAdministrator(Form.TextBoxUserContext.get()):
        STATE_FLAG = True
        with open(Profile.GetCredentialPath(), "w") as Cred:
            ENCODED_NAME = Encr.Encrypt(Form.TextBoxUserContext.get())
            ENCODED_PASSW = Encr.Encrypt(Form.TextBoxPasswordContext.get())
            Cred.write(str(ENCODED_NAME)[1:len(str(ENCODED_NAME))-1] + "\n" + str(ENCODED_PASSW)[1:len(str(ENCODED_PASSW))-1])
            Logs.WriteToLog("Profile saved from entry fields -> {0}".format(STATE_FLAG))
        Form.OnSavePressed()
    else: 
        Logs.WriteToLog("Operation Save failed. Empty user credential fields.")
        Form.TextBoxUserContext.insert(0,"Please enter your login and password")

def GetPassword(Event):
    if UserCred.NotNullOrEmpty(Form.TextBoxUserContext.get(), Form.TextBoxPasswordContext.get()):
        Net = NetCore.CheckNetwork()
       
        if Net == NetCore.socket.herror:
            return None
        JSON = Marsh.Marshaling().GetInstance()
        SRV = JSON.Deserialize(Profile.GetProfilePath() +  "\\SERVERS_POOL.json")
        OptimalServer = NetCore.GetOptimalServer(SRV)

        if STATE_FLAG:
            Logs.WriteToLog("Uses credential from file")
        else:
            Logs.WriteToLog("Uses entry fields credentials")

        Form.TextBoxDomainComputerRML.delete(0, "end")
        UserContextLocal = Form.TextBoxUserContext.get()
        PasswordContextLocal = Form.TextBoxPasswordContext.get()
        
        if not UserContextLocal.startswith("sa"):
            Form.TextBoxUserContext.delete(0, "end")
            Form.TextBoxPasswordContext.delete(0, "end")
            Form.TextBoxUserContext.insert(0, "{0} is not administrator!".format(UserContextLocal))
            Logs.WriteToLog("{0} is not administrator!".format(UserContextLocal))
            return None

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
