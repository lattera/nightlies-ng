#!/usr/bin/env python

import os, sys, signal
import subprocess
from xml.sax import make_parser

from Config import *
import Job

config = Config()

def sig_handler(signum, frame):
    if os.path.exists(config.lockfile):
        os.remove(config.lockfile)
    os._exit(0)

def main():
    signal.signal(signal.SIGINT, sig_handler)
    os.chdir(os.path.dirname(os.path.realpath(sys.argv[0])))
    configpath = "config.xml"
    if len(sys.argv) > 1:
        configpath = sys.argv[1]

    parser = make_parser()
    parser.setContentHandler(config)
    parser.parse(open(configpath))

    if os.path.exists(config.lockfile):
        return

    open(config.lockfile, "w").close()

    config.applyConfig()
    jobs = Job.Job.InitializeJobs(config)
    for job in jobs:
        job.RunJob(config)

    os.remove(config.lockfile)

if __name__ == "__main__":
    main()
