import requests
from datetime import datetime as dt
import LAPyS.JSON_Classes.Marshaling as Serializer

JSONdata ={ #! Just simple example
        "UserName" : "sa.stepanets",
        "Password" : "SOME_UGLY_BASTARD_PASSWORD",
        "RequestedName" : "SOME_NAME",
        "Date" :  str(dt.now())
    }

Data = Serializer.Marshaling().GetInstance() # Create an instance of Marshaling class
Payload = Data.Serialize(JSONdata)

Headers = {"Content-type": "application/json",
           "Accept": "*/*",
           "User-Agent" : "Python_Client",
           "Content-Encoding": "utf-8"}
           #"Content-Length" : str(len(Payload))}

URL = "http://93.76.47.112:65065/Kernel-LAPyS/index.php"
#URLTEST = "http://192.168.1.41:65065/some/post"
Answer = requests.post(URL, data = Payload , headers = Headers)

print(Answer)
print(Answer.headers)
print(Answer.text)
#print("Content-Length - ",len(Payload))
