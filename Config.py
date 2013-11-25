import sys
import os
from xml.sax import make_parser
from xml.sax.handler import ContentHandler
from datetime import datetime

import IRC

class Config(ContentHandler):
    def __init__(self, jsonobj):
        self.scripts = list()
        self.script = dict()
        self.date = datetime.now()
        self.debug = False
        self.logdir = "/tmp"
        self.lockfile = "/tmp/nightly.lock"
        self.irc = IRC.IRC(jsonobj)

        if "options" in jsonobj:
            if "logdir" in jsonobj["options"]:
                self.logdir = jsonobj["options"]["logdir"]
            if "debug" in jsonobj["options"]:
                self.debug = jsonobj["options"]["debug"]
            if "directory" in jsonobj["options"]:
                for directory in jsonobj["options"]["directory"]:
                    sys.path.append(directory)

        for job in jsonobj["jobs"]:
            if "disabled" in job and job["disabled"]:
                if not "forcerun" in job or not job["forcerun"]:
                    continue

            script = dict()
            # Defaults
            script["skip"] = False
            script["forcerun"] = False

            script["name"] = job["name"]
            script["module"] = job["module"]
            if "class" in job:
                script["class"] = job["class"]
            else:
                script["class"] = job["module"]

            if "options" in job:
                script["options"] = job["options"]
            if "dependencies" in job:
                script["dependencies"] = job["dependencies"]
            if "skip" in job:
                script["skip"] = job["skip"]
            if "forcerun" in job:
                script["forcerun"] = job["forcerun"]

            self.scripts.append(script)

    def applyConfig(self):
        if not os.path.isdir(self.logdir):
            os.mkdir(self.logdir)
