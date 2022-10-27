class CleverDict(dict):
    def __init__(self, dc):
        self.update(dc)

    def __getattr__(self, name):
        if(isinstance(self[name], dict)):
            return CleverDict(self[name])
        elif(name == "__str__"):
            return self.__str__()
        else:
            return self[name]