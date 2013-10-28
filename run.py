#!/usr/bin/env python

import os, sys
import subprocess
from xml.sax import make_parser

from Config import *
import Job

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.realpath(sys.argv[0])))
    configpath = "config.xml"
    if len(sys.argv) > 1:
        configpath = sys.argv[1]

    config = Config()
    parser = make_parser()
    parser.setContentHandler(config)
    parser.parse(open(configpath))

    if not os.path.isdir("logs"):
        os.mkdir("logs")

    config.applyConfig()
    jobs = Job.Job.InitializeJobs(config)
    for job in jobs:
        job.RunJob(config)

    if True == False:
        for script in config.scripts:
            logdirpath = "logs/" + script["path"][0].replace("/", "_")
            if not os.path.isdir(logdirpath):
                os.mkdir(logdirpath)

            path = config.date.strftime(logdirpath + "/%F_%T.log")
            with open(path, "w") as logfile:
                status = subprocess.call(script["path"], stdout=logfile, stderr=subprocess.STDOUT)
                if status != 0 and script["stop_on_error"]:
                    os._exit(1)
