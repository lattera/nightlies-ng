import os
import Config
import sys
import datetime

class Job:
    def __init__(self):
        self.module = None
        self.name = ""
        self.classname = ""
        self.modulename = ""
        self.status = "init"
        self.dependencies = list()
        self.instance = None
        self.forcerun = False
        self.options = dict()

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
            job.classname = script["class"]
            job.modulename = script["module"]
            if "options" in script:
                job.options = script["options"]

            job.module = __import__(job.modulename, globals(), locals(), job.classname, -1)
            exec("job.instance = job.module." + job.classname + "()")

            if script["skip"]:
                if config.debug:
                    print "[*] Skipping job " + job.name + ". Setting status to skipped."
                job.status = "skipped"
            if "forcerun" in script:
                job.forcerun = script["forcerun"]
            jobs.append(job)

        for script in config.scripts:
            if "dependencies" in script:
                job = Job.GetJob(jobs, script["name"])
                for dep in script["dependencies"]:
                    jobdep = Job.GetJob(jobs, dep)
                    if jobdep != None:
                        job.dependencies.append(jobdep)

        return jobs

    def RunJob(self, config):
        if not self.status == "init":
            if self.status == "skipped":
                config.irc.broadcast_message("[" + self.name + "]: Skpped");
            return

        if len(self.dependencies):
            for job in self.dependencies:
                if job.status == "init":
                    if job.RunJob(config) == False:
                        config.irc.broadcast_message("Job[" + self.name + "]: Dependency[" + job.name + "] failed. Skipping myself.")
                        self.status = "skipped"
                        break
                elif job.status == "false" and not self.forcerun:
                    if config.debug:
                        print "Job[" + self.name + "]: Dependency[" + job.name + "] failed. Skipping myself."
                    self.status = "skipped"
                    config.irc.broadcast_message("Job[" + self.name + "]: Dependency[" + job.name + "] failed. Skipping myself.")
                    break

        if self.status == "skipped":
            return False

        if config.debug:
            print "[+] Running " + self.name

        config.irc.broadcast_message("Job[" + self.name + "]: Starting.");

        if self.instance.Run(self, config):
            self.status = "true"
        else:
            self.status = "false"

        if config.debug:
            print "[+] " + self.name + " finished with status: " + self.status

        config.irc.broadcast_message("Job[" + self.name + "]: Finished: " + self.status)

        return self.status == "true"

    def GetLogfile(self, config):
        now = datetime.datetime.now()
        logdir = "{}/{}".format(config.logdir, self.name)
        if not os.path.isdir(logdir):
            os.mkdir(logdir)
        filename = "{}/{}_{:02}_{:02}_{:02}:{:02}:{:02}".format(logdir, now.year, now.month, now.day, now.hour, now.minute, now.second);
        return open(filename, "w")
