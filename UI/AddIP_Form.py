
import tkinter as tk
from LAPyS.Logging.LAPyS_Logging import Logs
from LAPyS.Utils.Profile import Profile
from LAPyS.JSON_Classes.Marshaling import JSON
import os

def Ip_Add_Form():
    Ip_Add_Form_window = tk.Tk()
    
    def AddServer(Event):
        Pool = JSON.Deserialize(Profile.GetProfilePath() +  "\\SERVERS_POOL.json")
        Pool[TextBoxServerName.get()] = TextBoxServerIP.get()
        with open(Profile.GetProfilePath() +  "\\SERVERS_POOL.json", "w") as ServerPoolFile:
            ServerPoolFile.write(JSON.Serialize(Pool))
            Logs.WriteToLog("Added " + TextBoxServerName.get() + " to servers pool")

    Ip_Add_Form_window.geometry("160x110")
    Ip_Add_Form_window.resizable(False, False)
    Ip_Add_Form_window.title("Server addition")

    labelServerName = tk.Label(Ip_Add_Form_window, text="Server name:")
    labelServerName.place(x = 10, y = 5, width = 130, height = 20)

    TextBoxServerName = tk.Entry(Ip_Add_Form_window)
    TextBoxServerName.place(x = 10, y = 25, width = 130, height = 20)

    labelServerIP = tk.Label(Ip_Add_Form_window, text="IPv4 Address:")
    labelServerIP.place(x = 10, y = 44, width = 130, height = 20)

    TextBoxServerIP = tk.Entry(Ip_Add_Form_window)
    TextBoxServerIP.place(x = 10, y = 65, width = 130, height = 20)

    BtnAdd = tk.Button(Ip_Add_Form_window, text="Load", width=10, height=2, bg="white", fg="black")
    BtnAdd.bind("<Button-1>", AddServer)
    BtnAdd.place(x = 10, y = 90, width = 130, height = 20)


    Ip_Add_Form_window.mainloop()
