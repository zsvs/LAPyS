
from tkinter import messagebox as mb
"""
Show messagebox with error to user
"""
#mb.askyesno(title="Error", message=)
def LdapError():
    mb.showerror(title="Error", message="Invalid LDAP Credential")
