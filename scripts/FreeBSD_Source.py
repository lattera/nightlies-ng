import os
import sys
import subprocess

class FreeBSD_Source:
    def __init__(self):
        self.dataset = "tank/src/freebsd"
        self.upstream_remote = "upstream-github"
        self.upstream_branch = "master"
        self.local_branch = "soldierx/lattera/aslr"
        self.commit_msg = "[automated] Merge in " + self.upstream_remote + "/" + self.upstream_branch
        self.push_to = "origin"

    def Run(self, job, config):
        curdir = os.getcwd()
        newdir = subprocess.check_output(["zfs", "get", "-H", "-ovalue", "mountpoint", self.dataset]).strip()
        os.chdir(newdir)

        status = subprocess.call(["git", "fetch", self.upstream_remote])
        if status != 0:
            os.chdir(curdir)
            return False

        status = subprocess.call(["git", "merge", "-m", self.commit_msg, self.upstream_remote + "/" + self.upstream_branch])
        if status != 0:
            os.chdir(curdir)
            return False

        status = subprocess.call(["git", "push", self.push_to, self.local_branch])
        if status != 0:
            os.chdir(curdir)
            return False

        os.chdir(curdir)
        return True
