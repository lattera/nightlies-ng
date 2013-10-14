from xml.sax import make_parser
from xml.sax.handler import ContentHandler
from datetime import datetime

class Config(ContentHandler):
    def __init__(self):
        self.scripts = list()
        self.date = datetime.now()
        self.debug = False

    def str2bool(self, s):
        return s.lower() in ("yes", "true", "t", "1")

    def startElement(self, name, attrs):
        if name == "script":
            script = dict()
            script["path"] = [attrs.get("path", "")]
            script["stop_on_error"] = Config.str2bool(self, attrs.get("stop_on_error", "false"))
            for attr in attrs.get("args", "").split():
                script["path"].append(attr)
            self.scripts.append(script)

    def endElement(self, name):
        pass
