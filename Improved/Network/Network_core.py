import socket
from ping3 import ping, verbose_ping
import LAPyS.Logging.LAPyS_Logging as Log
import LAPyS.Network.Servers_pool as SRV_POOL
import LAPyS.UI.Network_Error as UI_NetError

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
                    Log.WriteToLog("No ICMP answer from servers")
                    Log.WriteToLog("Function return default server {0}".format(DefServerAddr))
                    return DefServerAddr
                else:
                    Log.WriteToLog("Pinging server pool. Get {0} as main DC".format(OptimalServerName))
                    return OptimalServerAddr
        
def CheckNetwork():
    try:
        Log.WriteToLog("Network test started")
        hostname, domain = socket.gethostbyaddr(SRV_POOL.SERVERS_POOL["DC-KV-01"])[0].partition('.')[::2]
    except socket.herror:   
        Log.WriteToLog("No connection to domain network")
        UI_NetError.NetError()  
        return socket.herror
    else:
        Log.WriteToLog("Successfully connected to {0}".format(hostname + "." + domain))