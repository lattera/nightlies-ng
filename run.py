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

    config.applyConfig()
    jobs = Job.Job.InitializeJobs(config)
    for job in jobs:
        job.RunJob(config)
