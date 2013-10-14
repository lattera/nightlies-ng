#!/usr/bin/env python

import os, sys
import subprocess
from xml.sax import make_parser

from Config import *

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.realpath(sys.argv[0])))
    configpath = "config.xml"
    if len(sys.argv) > 1:
        configpath = sys.argv[1]

    config = Config()
    parser = make_parser()
    parser.setContentHandler(config)
    parser.parse(open(configpath))

    if os.path.isdir("logs") == False:
        os.mkdir("logs")

    for script in config.scripts:
        path = config.date.strftime("logs/%F_%T-" + script["path"][0].replace("/", "_") + ".log")
        logfile = open(path, "w")
        status = subprocess.call(script["path"], stdout=logfile, stderr=subprocess.STDOUT)
        logfile.close()
        if status != 0 and script["stop_on_error"]:
            os._exit(1)
