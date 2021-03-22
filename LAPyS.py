import tkinter as tk
import os
import datetime
import socket
import re # Regex
from ldap3 import Server, Connection, AUTO_BIND_NO_TLS, SUBTREE
from ldap3.core.exceptions import LDAPBindError
from ping3 import ping, verbose_ping

LDAP_SEACRCH_BASE_DIR = "OU=Кластер Західний,OU=Агропідприємства,OU=Компютери,OU=Kernel Holding,DC=kernel,DC=local"
STATE_FLAG = False
#!AD_Computers = dict()

SERVERS_POOL = {
        "DC-KV-01" : "10.1.249.116",
        "DC-KV-02" : "10.1.249.117",
        "DC-HPI-01" : "10.1.249.118"
        }

def GetOptimalServer(ServersPool):
    """
        Get servers from dictionary(Server Name -> IPv4 Address). 
        It will check delay time of all servers and return address of best one 
    """
    ServerDelayDict = dict()
    DefServerAddr = "10.1.249.118"
    PivotTime = 1.0
    OptimalServerAddr = ""
    for key in ServersPool.keys():
        ServerDelayDict[key] = ping(ServersPool[key])
        #! Add for debug info print(key," - ",ping(ServersPool[key]))
        for DelayTime in ServerDelayDict.values():
                try:
                    if DelayTime <= PivotTime:
                            PivotTime = DelayTime
                            OptimalServerAddr = ServersPool[key]
                            OptimalServerName = key
                except TypeError:
                    WriteToLog("No ICMP answer from servers")
                    WriteToLog("Function return default server {0}".format(DefServerAddr))
                    return DefServerAddr
                else:
                    WriteToLog("Pinging server pool. Get {0} as main DC".format(OptimalServerName))
                    return OptimalServerAddr
        
def CheckNetwork():
    try:
        WriteToLog("Network test started")
        hostname, domain = socket.gethostbyaddr(SERVERS_POOL["DC-KV-01"])[0].partition('.')[::2]
    except socket.herror:     
        WriteToLog("No connection to domain network")
        TextBoxDomainComputerRML.insert(0, "No connection to domain network")
        print(socket.herror)
        return socket.herror
    else:
        WriteToLog("Successfully connected to {0}".format(hostname + "." + domain))

def WriteToLog(Text):
    TIME = datetime.datetime.now()
    FILE_PATH = os.getenv("USERPROFILE") + "\\LAPyS Log\\Log.log"
    with open(FILE_PATH, "a") as LogFile:
        LogFile.write(str(TIME) + ": " + Text + "\n")

def Encrypt(String):
    lst = list()
    for symbol in String:
        lst.append(ord(symbol))
    return lst

def Decrypt(ByteList):
    st = str()
    for ASCII_Code in ByteList:
        st += chr(int(ASCII_Code))
    return st

def CheckUserCred_NotNullOrEmpty(UserName, Password):
    if len(UserName) == 0 or len(Password) == 0 or UserName == None or Password == None:
        WriteToLog("Entry fields are empty")
        return False
    else: 
        return True
    

def get_ldap_info(UserName, PasswordLocal, ComName, OptServer): 
    """
        This function gets domain admins credential, computer name
        and address of optimal LDAP server.
        It will connect to Doman Controller by using domain admin credential.
        When it successfully, then search requsted computer using LDAP request syntax.
        If it can't connect check log file.
        Returns list of LDAP attributes which contains ms-Msc-AdmPwd(local admin password)
    """
    if not UserName.startswith("sa"):
        WriteToLog("Not administrator entered!")
        return None
    try:
        with Connection(Server(OptServer, port=389, use_ssl=False), auto_bind=AUTO_BIND_NO_TLS, user="Kernel\\{0}".format(UserName), password=PasswordLocal) as c:
            c.search(search_base=LDAP_SEACRCH_BASE_DIR, search_filter="(&(objectCategory=computer)(objectClass=computer)(cn={0}))".format(ComName), search_scope=SUBTREE, attributes=["name", "ms-Mcs-AdmPwd"], get_operational_attributes=True)
            WriteToLog("LDAP credential successfully accepted")
        return c.entries
    except LDAPBindError:
        WriteToLog("Invalid LDAP credentials")
        TextBoxUserContext.delete(0, "end")
        TextBoxPasswordContext.delete(0, "end")
        TextBoxUserContext.insert(0, "Invalid LDAP credentials")
        TextBoxPasswordContext.insert(0, "Invalid LDAP credentials")
        
window = tk.Tk()

try:
    os.mkdir(os.getenv("USERPROFILE") + "\\LAPyS Log")
    WriteToLog("Profile directory created")
except FileExistsError:
    WriteToLog("Profile directory already exists")
    #print("File already exists")

def Load(Event):
    global STATE_FLAG
    STATE_FLAG = True
    TextBoxUserContext.delete(0, "end")
    TextBoxPasswordContext.delete(0, "end")
    BtnSave.configure(state="disabled")
    BtnLoad.configure(state="disabled")
    FILE_PATH = os.getenv("USERPROFILE") + "\\LAPyS Log\\Credential.cred"
    with open(FILE_PATH, "r") as Cred:
        DECODED_NAME = Cred.readlines(1)
        DECODED_PASSW = Cred.readlines(1)
        TextBoxUserContext.insert(0, Decrypt(DECODED_NAME[0].split(",")))
        TextBoxPasswordContext.insert(0, Decrypt(DECODED_PASSW[0].split(",")))
        WriteToLog("Profile loaded from file Credential.cred -> {0}".format(STATE_FLAG))
    TextBoxUserContext.configure(state="disabled")
    TextBoxPasswordContext.configure(state="disabled")

def Save(Event):
    global STATE_FLAG
    if CheckUserCred_NotNullOrEmpty(TextBoxUserContext.get(), TextBoxPasswordContext.get()):
        STATE_FLAG = True
        BtnLoad.configure(state="disabled")
        FILE_PATH = os.getenv("USERPROFILE") + "\\LAPyS Log\\Credential.cred"
        with open(FILE_PATH, "w") as Cred:
            ENCODED_NAME = Encrypt(TextBoxUserContext.get())
            ENCODED_PASSW = Encrypt(TextBoxPasswordContext.get())
            Cred.write(str(ENCODED_NAME)[1:len(str(ENCODED_NAME))-1] + "\n" + str(ENCODED_PASSW)[1:len(str(ENCODED_PASSW))-1])
            WriteToLog("Profile saved from entry fields -> {0}".format(STATE_FLAG))
        TextBoxUserContext.configure(state="disabled")
        TextBoxPasswordContext.configure(state="disabled")
    else: 
        WriteToLog("Operation Save failed. Empty user credential fields.")
        TextBoxUserContext.insert(0,"Please enter your login and password")

def GetPassword(Event):
    global SERVERS_POOL
    if CheckUserCred_NotNullOrEmpty(TextBoxUserContext.get(), TextBoxPasswordContext.get()):
        Net = CheckNetwork()
       
        if Net == socket.herror:
            return None

        OptimalServer = GetOptimalServer(SERVERS_POOL)



        if STATE_FLAG:
            WriteToLog("Uses credential from file")
        else:
            WriteToLog("Uses entry fields credentials")
            

        TextBoxDomainComputerRML.delete(0, "end")
        UserContextLocal = TextBoxUserContext.get()
        PasswordContextLocal = TextBoxPasswordContext.get()
        
        if not UserContextLocal.startswith("sa"):
            TextBoxUserContext.delete(0, "end")
            TextBoxPasswordContext.delete(0, "end")
            TextBoxUserContext.insert(0, "{0} is not administrator!".format(UserContextLocal))
            WriteToLog("{0} is not administrator!".format(UserContextLocal))
            return None

        RequestedNameLocal = TextBoxDomainComputerName.get()
    
        if len(RequestedNameLocal) == 0:
            WriteToLog("Requested name is empty!")
        else:
            WriteToLog("Requested name -> {0}".format(RequestedNameLocal))

        AD = get_ldap_info(UserContextLocal, PasswordContextLocal, RequestedNameLocal, OptimalServer)
        AD_Computers = dict() #TODO Think about creates global dict to store all results for improving speed of searching.
        for obj in AD:
	        AD_Computers[(str(obj.entry_attributes_as_dict["name"])[2:len(str(obj.entry_attributes_as_dict["name"]))-2])] = str(obj.entry_attributes_as_dict["ms-Mcs-AdmPwd"])[2:len(str(obj.entry_attributes_as_dict["ms-Mcs-AdmPwd"]))-2]

        try:
            TextBoxDomainComputerRML.insert(0, AD_Computers[RequestedNameLocal])
        except KeyError:
            TextBoxDomainComputerRML.insert(0, "No such name in OU")
            WriteToLog("No such name in OU")
            WriteToLog("Connection to LDAP server closed")
        else:
            WriteToLog("RML successfully returned")
            WriteToLog("Connection to LDAP server closed")
    else:
        TextBoxUserContext.insert(0,"Please enter your login and password")
        TextBoxDomainComputerRML.insert(0,"Please enter your login and password")

window.geometry('400x180')
window.resizable(False, False)
window.title("LAPyS")

labelUserLogin = tk.Label(text="Enter your domain login:")
labelUserLogin.place(x = 100, y = 5, width = 250, height = 15)

TextBoxUserContext = tk.Entry()
TextBoxUserContext.place(x = 100, y = 25, width = 250, height = 20)

labelUserPassword = tk.Label(text="Enter your password:")
labelUserPassword.place(x = 100, y = 45, width = 250, height = 20)

TextBoxPasswordContext = tk.Entry()
TextBoxPasswordContext["show"] = "*"
TextBoxPasswordContext.place(x = 100, y = 65, width = 250, height = 20)

labelRequestedName = tk.Label(text="Enter name of computer:")
labelRequestedName.place(x = 100, y = 85, width = 250, height = 20)

TextBoxDomainComputerName = tk.Entry()
TextBoxDomainComputerName.place(x = 100, y = 105, width = 250, height = 20)

TextBoxDomainComputerRML = tk.Entry()
TextBoxDomainComputerRML.place(x = 100, y = 145, width = 250, height = 20)

BtnLoad = tk.Button(window, text="Load", width=10, height=2, bg="white", fg="black")
BtnLoad.bind("<Button-1>", Load)
BtnLoad.place(x = 10, y = 25, width = 80, height = 20)

BtnSave = tk.Button(window, text="Save", width=10, height=2, bg="white", fg="black")
BtnSave.bind("<Button-1>", Save)
BtnSave.place(x = 10, y = 65, width = 80, height = 20)

BtnPassw = tk.Button(window, text="Get password", width=10, height=2, bg="white", fg="black")
BtnPassw.bind("<Button-1>", GetPassword)
BtnPassw.place(x = 10, y = 105, width = 80, height = 20)

window.mainloop()
if window.mainloop() == None:
    WriteToLog("Application killed!")
