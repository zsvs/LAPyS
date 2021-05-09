import socket
from ping3 import ping, verbose_ping
from Logging.LAPyS_Logging import Logs
import UI.Network_Error as UI_NetError
from JSON_Classes.Marshaling import JSON
from Utils.Profile import Profile
"""
Module provides work with network.
Such as:
1) pinging;
2) create sockets;
And allow to find optimal in delay time server.
"""

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
                    Logs.WriteToLog("No ICMP answer from servers")
                    Logs.WriteToLog("Function return default server {0}".format(DefServerAddr))
                    return DefServerAddr
                else:
                    Logs.WriteToLog("Pinging server pool. Get {0} as main DC".format(OptimalServerName))
                    return OptimalServerAddr
        
def CheckNetwork():
    try:
        SRV = JSON.Deserialize(Profile.GetProfilePath() +  "\\SERVERS_POOL.json")
        Logs.WriteToLog("Network test started")
        hostname, domain = socket.gethostbyaddr(SRV["DC-KV-01"])[0].partition('.')[::2]
    except socket.herror:   
        Logs.WriteToLog("No connection to domain network")
        UI_NetError.NetError()  
        return socket.herror
    else:
        Logs.WriteToLog("Successfully connected to {0}".format(hostname + "." + domain))