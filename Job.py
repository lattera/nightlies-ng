import os
import Config
import sys
import datetime

class Job:
    def __init__(self):
        self.module = None
        self.name = ""
        self.status = "init"
        self.dependencies = list()
        self.instance = None

    @staticmethod
    def GetJob(jobs, name):
        for job in jobs:
            if job.name == name:
                return job

        return None

    @staticmethod
    def InitializeJobs(config):
        #sys.path.append(os.path.realpath(config.scriptpath))
        jobs = list()
        for script in config.scripts:
            job = Job()
            job.name = script["name"]
            job.module = __import__(job.name, globals(), locals(), job.name, -1)
            exec("job.instance = job.module." + job.name + "()")
            jobs.append(job)

        for script in config.scripts:
            if len(script["dependencies"]):
                job = Job.GetJob(jobs, script["name"])
                for dep in script["dependencies"]:
                    jobdep = Job.GetJob(jobs, dep)
                    if jobdep != None:
                        job.dependencies.append(jobdep)

        return jobs

    def RunJob(self, config):
        if len(self.dependencies):
            for job in self.dependencies:
                if job.status == "init":
                    if job.RunJob(config) == False:
                        return False
                elif job.status == "false":
                    if config.debug:
                        print "Job[" + self.name + "]: Dependency[" + job.name + "] failed. Skipping."
                    return False

        if self.instance.Run(self, config):
            self.status = "true"
        else:
            self.status = "false"

    def GetLogfile(self, config):
        now = datetime.datetime.now()
        logdir = "{}/{}".format(config.logdir, self.name)
        if not os.path.isdir(logdir):
            os.mkdirs(logdir)
        filename = "{}/{}_{}_{}_{}:{}:{}".format(logdir, now.year, now.month, now.day, now.hour, now.minute, now.second);
        return open(filename, "w")
