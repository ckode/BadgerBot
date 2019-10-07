from __future__ import with_statement
import ConfigParser as configparser
from time import time
import sys
import random


VERSION = "0.1"
APPNAME = "BadgerBot - Version: " + VERSION

class BadgerBot:
    """
    Default BadgerBot application class.
    """
    def __init__(self, crt):
        """
        Initialize the application and load the configurations from disk.
        """
        self.crt = crt
        self.terminal = crt.Screen
        self.tab = crt.GetScriptTab()
        self.tab.Screen.IgnoreEscape = True
        self.tab.Screen.Synchronous = True
        self.terminal.Send("talk slow\n")
        global APPNAME
        global VERSION
        self.config = configparser.ConfigParser()
        self.config.read('BadgerBot.cfg')

        self.app_name = APPNAME
        self.version = VERSION
        self.player_name = None

        self.last_send = 0
        self.talk_delay = int(self.config.get('DEFAULTS', 'TalkDelay'))
        self.insults_enabled = bool(self.config.get('DEFAULTS', 'InsultsEnabled'))
        self.insults = self.get_list(self.config.get('DEFAULTS', 'InsultsConfig'))
        self.actions_enabled = bool(self.config.get('DEFAULTS', 'ActionsEnabled'))
        self.actions = self.get_list(self.config.get('DEFAULTS', 'ActionsConfig'))


    def get_list(self, config_file):
        # Load multi-line config files
        line_list = []
        try:
            with open(config_file) as fp:
                for line in fp:
                    if line.lstrip().startswith("#"):
                        continue
                    line_list.append(line)
        except EnvironmentError:
            print("An error occurred opening file %s for reading.\nExiting..." % (config_file))
            sys.exit()
        return line_list

    # strip the statline off the incoming text.
    def strip_statline(self, line):
        x = 0
        x = line.rfind("]:")
        if x == -1:
            return line
        while line[x] == "]" or line[x] == ":":
            x = x + 1
        return line[x:]

    # Get the next incoming line and send it to strip statline
    # then return it for processing.
    def get_next_line(self):
        return self.strip_statline(self.tab.Screen.ReadString("\n"))


    # Get the player running the bot's name
    def get_badger_player_name(self):
        self.terminal.Send("st\n")
        x = 0
        while True:
            x = x + 1
            if x == 5:
                self.player_name = "Unknown"
                return
            line = self.get_next_line()
            if "Name:" in line:
                words = line.split(" ")
                self.player_name = words[1].lstrip()
                return


    def process_line(self, line):
        talk_style = None
        word_list = []
        words = line.split(" ")
        for word in words:
            word_list.append(word.lstrip())
        victim = word_list[0].lstrip()
        if len(word_list) < 3 or word_list[0] == self.player_name:
            return
        if word_list[1] == "gossips:" and victim is not self.player_name:
            talk_style = "gos "
        elif word_list[1] == "auctions:" and victim is not self.player_name:
            talk_style = "auc "
        elif word_list[1] == "telepaths:":
            talk_style = "/%s " % victim
        elif word_list[1] == "says," and victim is not "You":
            talk_style = "."
        elif word_list[0] == "Broadcast" and word_list[2] is not self.player_name:
            talk_style = "br "
            victim = word_list[2]
        if talk_style != None:
            message = random.choice(self.insults) % (victim)
            self.send(talk_style + message)
    
    def send(self, message):
        if (int(time()) + self.talk_delay) >= self.last_send:
            self.terminal.Send(message)
            self.last_send = int(time())

def main():
    app = BadgerBot(crt)
    crt.Screen.Send("." + app.app_name + "\n")
    app.get_badger_player_name()
    while True:
        app.process_line(app.get_next_line())



main()




