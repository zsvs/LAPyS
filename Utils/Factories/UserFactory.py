from LAPyS.Utils.Factories.BaseFactory import AbstractFactory
import LAPyS.Utils.UserClass as UserClass

class UserFactory(AbstractFactory):
    def __init__(self, Name):
        super().__init__(Name)

    def CreateInstance(self, InstanceObjectName, InstanceName, InstancePassword):
        return UserClass.User(ObjectName = InstanceObjectName, Name = InstanceName, Password = InstancePassword)

