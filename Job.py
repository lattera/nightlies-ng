import os
import Config
import sys

class Job:
    def __init__(self):
        self.module = None
        self.name = ""
        self.status = "init"
        self.dependencies = list()
        self.instance = None

    @staticmethod
    def InitializeJobs(config):
        sys.path.append(os.path.realpath(config.scriptpath))
        jobs = list()
        for script in config.scripts:
            job = Job()
            job.name = script["name"]
            job.module = __import__(job.name, globals(), locals(), job.name, -1)
            exec("job.instance = job.module." + job.name + "()")

        return jobs
