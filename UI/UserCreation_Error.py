from tkinter import messagebox as mb
"""
Show messagebox with error to user
"""
#mb.askyesno(title="Error", message=)
def Creation_Error(UserName):
    mb.showerror(title="Name error", message="{0} is not administrator!".format(UserName))