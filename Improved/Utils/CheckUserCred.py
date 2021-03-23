

def NotNullOrEmpty(UserName, Password):
    """
    If string is empty return FALSE
    """
    if len(UserName) == 0 or len(Password) == 0 or UserName == None or Password == None:
        #WriteToLog("Entry fields are empty")
        return False
    else: 
        return True

def isAdministrator(UserName):
    """
    if UserName starts with <sa> return TRUE
    """
    if UserName.startswith("sa"):
        return True
    else:
        return False