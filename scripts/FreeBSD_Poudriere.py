import subprocess

class FreeBSD_Poudriere:
    def __init__(self):
        self.jails = list()
        self.poudriere_dir = "/tank/poudriere/jails"
        self.config_dir = "/tank/poudriere/configs"

        jail = dict()
        jail["name"] = "11-current_amd64"
        jail["ports"] = "local"
        jail["configfile"] = "11-current_amd64.ports.txt"
        jail["syncdir"] = "/tank/poudriere/packages/11-current_amd64"
        self.jails.append(jail)

    def Run(self, job, config):
        for jail in self.jails:
            status = subprocess.call([
                "sudo",
                "poudriere",
                "bulk",
                "-f", self.config_dir + "/" + jail["configfile"],
                "-j", jail["name"],
                "-p", jail["ports"]
            ])
            if status != 0:
                return False

            status = subprocess.call([
                "sudo",
                "rsync"
                "-a",
                self.poudriere_dir + "/data/packages" + jail["name"] + "-" + jail["ports"] + "/",
                jail["syncdir"]
            ])
            if status != 0:
                return False

        return True
