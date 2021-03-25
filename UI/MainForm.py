import tkinter as tk
#import LAPyS.LAPyS_Core as Events
from LAPyS.LAPyS_Core import Save, Load, GetPassword
import LAPyS.Logging.LAPyS_Logging as Log
"""
Module for create GUI by using tkinter libs
"""
window = tk.Tk()

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
    Log.WriteToLog("Application killed!")