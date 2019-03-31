import json

class Config():
    """Config file class for Caroline"""
    def __init__(self, filename):
        self.filename = filename
        self.config = {}
        self.loadConfig()
        

    def saveConfig(self):
        with open(self.filename, 'w') as file:
            json.dump(self.config, file, indent=4, sort_keys=True)


    def loadConfig(self, filename=None):
        if filename != None:
            self.filename = filename

        with open(self.filename, 'r') as file:
            self.config = json.load(file)


    def get(self, prop):
        try:
            return self.config[prop]
        except KeyError:
            raise KeyError("'{0}' was not found in the config file '{1}'".format(prop, self.filename))


    def set(self, prop, content):
        self.config[prop] = content
        self.saveConfig()



        