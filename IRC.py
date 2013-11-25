import os, sys
import subprocess
import json

class IRC:
    def __init__(self, options=dict()):
        self.options = options;
        self.enabled = False
        if not "irc" in options:
            return True

        if not "path" in options["irc"]:
            return False

        if not "networks" in options["irc"]:
            return False

        for network in options["irc"]["networks"]:
            if not "name" in network:
                return False
            if not "channels" in network:
                return False

            if not self.is_network_connected(network["name"]):
                continue

            for channel in network["channels"]:
                if not self.is_in_chan(network["name"], channel):
                    if self.join_chan(network["name"], channel, False) == False:
                        return False

        self.enabled = True

    def is_network_connected(self, network):
        return os.path.isdir(self.options["irc"]["path"] + "/" + network)

    def is_in_chan(self, network, chan):
        val = os.path.exists(self.options["irc"]["path"] + "/" + network + "/" + chan + "/out")
        return val

    def join_chan(self, network, chan, checkEnabled=True):
        if checkEnabled and not self.enabled:
            return False

        with open(self.options["irc"]["path"] + "/" + network + "/in", "w") as fifo:
            val = subprocess.call(["/bin/echo", "/j", chan], stdout=fifo)
            return val == 0

    def broadcast_message(self, message):
        if not self.enabled:
            return False

        for network in self.options["irc"]["networks"]:
            for channel in network["channels"]:
                if not self.is_in_chan(network["name"], channel):
                    if self.join_chan(network["name"], channel) == False:
                        continue

                with open(self.options["irc"]["path"] + "/" + network["name"] + "/" + channel + "/in", "w") as fifo:
                    subprocess.call(["/bin/echo", message], stdout=fifo)
