import json
"""
Module provide mechanism to marshaling data to/from json
"""
class Marshaling: # Singleton class, that provide marhaling of information and storage of deserialization history 

    __Instance = None # Stores instance of class
    __History = set() # Saves paths to files that were used for deserialization

    def __init__(self):
        if Marshaling.__Instance:
            print("Instance already created", self.GetInstance())
    
    @classmethod
    def GetInstance(cls):
        if cls.__Instance == None:
            cls.__Instance = Marshaling()
        return cls.__Instance

    def GetHistory(self):
        return self.__History
    
    def Serialize(self, Dictionary):
        return json.dumps(Dictionary)

    def Deserialize(self, JSON_Path):
        self.__History.add(JSON_Path)
        with open(JSON_Path, "r") as JSON_File:
            return json.load(JSON_File)

#Data = Serializator().GetInstance()
#obj = Data.Deserialize("C:\\Users\\stepa\\Documents\\Repositories\\Python\\WindowBased\\Network\\SERVERS_POOL.json")
#print(obj["DC-KV-01"])