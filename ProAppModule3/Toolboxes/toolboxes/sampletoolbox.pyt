"""
This is a sample toolbox
"""
import arcpy

class Toolbox(object):
    def __init__(self):
        self.label = "Sample Toolbox"
        self.alias = "SampleToolbox"
        self.tools = [Hello_Tool]

class Hello_Tool(object):

    def __init__(self):
        self.label = "Hello World"
        self.description = "Sends a sample message."
        self.canRunInBackground = False
        return

    def getParameterInfo(self):
        # I have no parameters!
        return []

    def isLicensed(self):
        return True
    
    def updateParameters(self, parameters):
        return

    def updateMessages(self, parameters):
        return
    
    def execute(self, parameters, messages):
        messages.addMessage("Hello, ArcGIS!")
        return
