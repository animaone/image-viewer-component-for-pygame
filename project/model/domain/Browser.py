import os

class Browser:
    def __init__(self, basedir):
        self.imdir = basedir

    def setDir(self, imdir):
        self.imdir = os.path.normpath(imdir)

    def getDir(self):
        return self.imdir