class AbstractFactory:
    FactoryName = None
    def __init__(self, Name):
        self.FactoryName = Name
    
    def CreateInstance(self):
        return None