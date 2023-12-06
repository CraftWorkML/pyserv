class Controller:
    def __init__(self):
        ...
    def getFile(self, parameter):
        print("in controller")
        return "file.png"

def getController(name):
    if name:
        return Controller()