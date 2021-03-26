import requests
from datetime import datetime as dt
import LAPyS.JSON_Classes.Serializator as Serializer

JSONdata ={ #! Just simple example
        "UserName" : "sa.stepanets",
        "Password" : "SOME_UGLY_BASTARD_PASSWORD",
        "RequestedName" : "SOME_NAME",
        "Date" :  str(dt.now())
    }


Headers = {"Content-type":  "application/json",  # Определение типа данных
           "Accept": "*/*",
           "User-Agent" : "Python_Client",
           "Content-Encoding": "utf-8"}

URL = "http://192.168.1.41:65065/some/post"

Data = Serializer.Serializator()
Data.GetInstance()
Answer = requests.post(URL, data = Data.Serialize(JSONdata) , headers = Headers)

print(Answer)
print(Answer.headers)
print(Answer.text)
