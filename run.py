#!/usr/bin/env python

import os, sys, signal
import subprocess
import json

import Config
import Job

def sig_handler(signum, frame):
    if os.path.exists(config.lockfile):
        os.remove(config.lockfile)
    os._exit(0)

def main():
    jsonconfig = dict()

    signal.signal(signal.SIGINT, sig_handler)
    os.chdir(os.path.dirname(os.path.realpath(sys.argv[0])))

    configpath = "config.json"
    if len(sys.argv) > 1:
        configpath = sys.argv[1]

    with open(configpath, "r") as configfile:
        jsonconfig = json.loads(configfile.read())

    config = Config.Config(jsonconfig)

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
