from __future__ import with_statement
import ConfigParser as configparser
from time import time
import sys


VERSION = "0.01"
APPNAME = "BadgerBot - Version: " + VERSION

class BadgerBot:
    """
    Default BadgerBot application class.
    """
    def __init__(self, crt.Screen):
        """
        Initialize the application and load the configurations from disk.
        """

        terminal = crt.Screen
        terminal.Send("talk slow\n")
        global APPNAME
        global VERSION
        self.config = configparser.ConfigParser()
        self.config.read('BadgerBot.cfg')

        self.app_name = APPNAME
        self.version = VERSION
        self.last_send = 0
        self.talk_queue = []
        self.talk_queue_size = self.config.get('DEFAULTS', 'TalkQueueSize')
        self.talk_delay = self.config.get('DEFAULTS', 'TalkDelay')
        self.insults_enabled = self.config.get('DEFAULTS', 'InsultsEnabled')
        self.insults = self.get_list(self.config.get('DEFAULTS', 'InsultsConfig'))
        self.actions_enabled = self.config.get('DEFAULTS', 'ActionsEnabled')
        self.actions = self.get_list(self.config.get('DEFAULTS', 'ActionsConfig'))


    def get_list(self, config_file):
        # Load multi-line config files
        line_list = []
        try:
            with open(config_file) as fp:
                for line in fp:
                    line_list.append(line)
        except EnvironmentError:
            print("An error occurred opening file %s for reading.\nExiting..." % (config_file))
            sys.exit()
        return line_list


    def send(self, message):
        # Send message to terminal
        if len(self.talk_queue) >= 10:
            crt.Screen.Send("Slow down! Action not queued.")
        else:
            self.talk_queue.insert(0, message)

    def process_queue(self):
        if int(time.time()) > self.last_send and len(self.talk_queue) > 0:
            crt.Screen.Send(self.talk_queue.pop())


def main():
    app = BadgerBot(crt)
    crt.Screen.Send("." + app.app_name + "\n")
    



main()
    



