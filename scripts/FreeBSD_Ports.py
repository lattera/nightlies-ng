import os
import sys
import subprocess

class FreeBSD_Ports:
    def __init__(self):
        self.portsdir = "/usr/ports"
        self.jobs = 7

    def Run(self, job, config):
        curdir = os.getcwd()
        os.chdir(self.portsdir)
        status = subprocess.call(["git", "fetch"])
        if status != 0:
            os.chdir(curdir)
            return False

        status = subprocess.call(["git", "merge", "origin/master"])
        if status != 0:
            os.chdir(curdir)
            return False

        if self.portsdir == "/usr/ports":
            status = subprocess.call(["make", "-j" + str(self.jobs), "index"])
            if status != 0:
                os.chdir(curdir)
                return False

        os.chdir(curdir)

        return True
