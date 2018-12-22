import os

class Browser:
    def __init__(self):
        self.imdir = "images/"

    def setDir(self, imdir):
        self.imdir = os.path.normpath(imdir)

    def getDir(self):
        return self.imdir