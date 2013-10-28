import sys
import os
from xml.sax import make_parser
from xml.sax.handler import ContentHandler
from datetime import datetime

class Config(ContentHandler):
    def __init__(self):
        self.scripts = list()
        self.script = dict()
        self.date = datetime.now()
        self.debug = False
        self.isInOptions = False
        self.isInScript = False
        self.logdir = "/tmp"

    def str2bool(self, s):
        return s.lower() in ("yes", "true", "t", "1")

    def startElement(self, name, attrs):
        if self.isInOptions:
            if name == "directory":
                path = attrs.get("path", "")
                if len(path):
                    sys.path.append(os.path.realpath(path))
            elif name == "debug":
                self.debug = str2bool(attrs.get("value", ""))
            elif name == "logdir":
                self.logdir = attrs.get("path", "/tmp")
        elif self.isInScript:
            if name == "dependency":
                self.script["dependencies"].append(attrs.get("name", ""))
        else:
            if name == "options":
                self.isInOptions = True
            elif name == "script":
                if self.str2bool(attrs.get("disabled", "false")):
                    return
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
        if not os.path.isdir(self.logdir):
            os.mkdirs(self.logdir)
