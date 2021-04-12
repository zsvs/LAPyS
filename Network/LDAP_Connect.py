from ldap3 import Server, Connection, AUTO_BIND_NO_TLS, SUBTREE
from ldap3.core.exceptions import LDAPBindError
from LAPyS.Logging.LAPyS_Logging import Logs
import LAPyS.Utils.UserClass as UserClass
import LAPyS.UI.UI_LDAP_Error as ldap_error_message
"""
Module used for provide work with LDAP.
Using ldap3 lib.
"""
LDAP_SEACRCH_BASE_DIR = "OU=Кластер Західний,OU=Агропідприємства,OU=Компютери,OU=Kernel Holding,DC=kernel,DC=local"

def get_ldap_info(UserName, PasswordLocal, ComName, OptServer): 
    """
        This function gets domain admins credential, computer name
        and address of optimal LDAP server.
        It will connect to Doman Controller by using domain admin credential.
        When it successfully, then search requsted computer using LDAP request syntax.
        If it can't connect check log file.
        Returns list of LDAP attributes which contains ms-Msc-AdmPwd(local admin password)
    """
    if not UserClass.User.isAdministrator(UserName):
        Logs.WriteToLog("Not administrator entered!")
        return None
    try:
        with Connection(Server(OptServer, port=389, use_ssl=False), auto_bind=AUTO_BIND_NO_TLS, user="Kernel\\{0}".format(UserName), password=PasswordLocal) as c:
            c.search(search_base=LDAP_SEACRCH_BASE_DIR, search_filter="(&(objectCategory=computer)(objectClass=computer)(cn={0}))".format(ComName), search_scope=SUBTREE, attributes=["name", "ms-Mcs-AdmPwd"], get_operational_attributes=True)
            Logs.WriteToLog("LDAP credential successfully accepted")
        return c.entries
    except LDAPBindError:
        Logs.WriteToLog("Invalid LDAP credentials")
        ldap_error_message.LdapError()
