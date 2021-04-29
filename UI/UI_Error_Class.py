"""
Class for creates error windows
"""
from tkinter import messagebox as mb

class UIError:
    """
    Static class that contains methods for creates various error window
    """
    @staticmethod
    def UserCreationError(UserName):
        """
        Creates error window
        for User creation errors
        """
        mb.showerror(title="Name error", message="{0} is not administrator!".format(UserName))

    @staticmethod
    def NetError(self):
        """
        Creates error window
        for Network errors
        """
        mb.showerror(title="Error", message="No connection to domain network")

    @staticmethod
    def LdapError():
        """
        Creates error window 
        for LDAP errors
        """
        mb.showerror(title="Error", message="Invalid LDAP Credential")
    
    @staticmethod
    def CustomError(**kwargs):
        """
        Creates custom error window.
        Gets kwargs "Title" and "Message"
        for setting up it in window text
        """
        mb.showerror(title=kwargs.get("Title"), message=kwargs.get("Message"))
