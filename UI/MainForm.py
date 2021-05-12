"""
Module for create GUI by using tkinter libs.
Implements functions for block and clear for TextBoxes
"""

import tkinter as tk
import os
from LAPyS.LAPyS_Core import Save, Load, GetPassword
from LAPyS.Logging.LAPyS_Logging import Logs
from LAPyS.Utils.Profile import Profile
from LAPyS.UI.AddIP_Form import AddIpForm

window = tk.Tk()

window.geometry("400x220")
window.resizable(False, False)
window.title("LAPyS")

mainMenu = tk.Menu(window)

fileMenu = tk.Menu(mainMenu, tearoff=0)
fileMenu.add_command(label = "Add ip to pool", command = lambda: AddIpForm.GetInstance("Add_IP").Initialize())
fileMenu.add_command(label = "View server pool", command = lambda: os.system(Profile.GetProfilePath() +  "\\SERVERS_POOL.json"))
fileMenu.add_command(label = "Open logs", command = lambda: os.system(Logs.GetLogFilePath()))

aboutMenu = tk.Menu(mainMenu, tearoff=0)
aboutMenu.add_command(label = "About")

labelUserLogin = tk.Label(window, text="Enter your domain login:")
labelUserLogin.place(x = 100, y = 25, width = 250, height = 15)

TextBoxUserContext = tk.Entry(window)
TextBoxUserContext.place(x = 100, y = 45, width = 250, height = 20)

labelUserPassword = tk.Label(window, text="Enter your password:")
labelUserPassword.place(x = 100, y = 65, width = 250, height = 20)

TextBoxPasswordContext = tk.Entry(window)
TextBoxPasswordContext["show"] = "*"
TextBoxPasswordContext.place(x = 100, y = 85, width = 250, height = 20)

labelRequestedName = tk.Label(window, text="Enter name of computer:")
labelRequestedName.place(x = 100, y = 105, width = 250, height = 20)

TextBoxDomainComputerName = tk.Entry(window)
TextBoxDomainComputerName.place(x = 100, y = 125, width = 250, height = 20)

TextBoxDomainComputerRML = tk.Entry(window)
TextBoxDomainComputerRML.place(x = 100, y = 165, width = 250, height = 20)

BtnLoad = tk.Button(window, text="Load", width=10, height=2, bg="white", fg="black")
BtnLoad.bind("<Button-1>", Load)
BtnLoad.place(x = 10, y = 45, width = 80, height = 20)

BtnSave = tk.Button(window, text="Save", width=10, height=2, bg="white", fg="black")
BtnSave.bind("<Button-1>", Save)
BtnSave.place(x = 10, y = 85, width = 80, height = 20)

BtnPassw = tk.Button(window, text="Get password", width=10, height=2, bg="white", fg="black")
BtnPassw.bind("<Button-1>", GetPassword)
BtnPassw.place(x = 10, y = 125, width = 80, height = 20)

def onLoad_ClearFields():
    TextBoxUserContext.delete(0, "end")
    TextBoxPasswordContext.delete(0, "end")    

mainMenu.add_cascade(label = "File", menu=fileMenu)
mainMenu.add_cascade(label = "About", menu=aboutMenu)
window.config(menu=mainMenu)
window.mainloop()

if window.mainloop() == None:
    Logs.WriteToLog("Application killed!")


