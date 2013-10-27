import sys
from xml.sax import make_parser
from xml.sax.handler import ContentHandler
from datetime import datetime

class Config(ContentHandler):
    def __init__(self):
        self.scripts = list()
        self.script = dict()
        self.date = datetime.now()
        self.debug = False
        self.scriptpath = ""
        self.isInOptions = False
        self.isInScript = False

    def str2bool(self, s):
        return s.lower() in ("yes", "true", "t", "1")

    def startElement(self, name, attrs):
        if self.isInOptions:
            if name == "directory":
                self.scriptpath = attrs.get("path", "")
            elif name == "debug":
                self.debug = str2bool(attrs.get("value", ""))
        elif self.isInScript:
            if name == "dependency":
                self.script["dependencies"].append(attrs.get("name", ""))
        else:
            if name == "options":
                self.isInOptions = True
            elif name == "script":
                self.isInScript = True
                self.script = dict()
                self.script["dependencies"] = list()
                self.script["name"] = attrs.get("name", "")

    def endElement(self, name):
        if name == "options":
            self.isInOptions = False
        elif name == "script":
            self.isInScript = False
            self.scripts.append(self.script)

    def applyConfig(self):
        if len(self.scriptpath):
            sys.path.append(self.scriptpath)
