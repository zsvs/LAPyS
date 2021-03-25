
from tkinter import messagebox as mb

#mb.askyesno(title="Error", message=)
def LdapError():
    mb.showerror(title="Error", message="Invalid LDAP Credential")
