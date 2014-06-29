#!/usr/bin/env python
"""
Testing file
"""
import os
import sys
import cmd
import readline
import signal


# Imports for logging modules
from pynetdev.log import initialize_logger
from pynetdev.log import line_number
from pynetdev.log import logging_argparse

# Imports for configuration
import pynetdev.config
import pynetdev.netauto_common as common

# Imports auto-completion class
#import pynetdev.completer
#auto_comp = pynetdev.completer.Completer()
# we want to treat '/' as part of a word, so override the delimiters
#pynetdev.completer.readline.set_completer_delims(' \t\n;')
#pynetdev.completer.readline.parse_and_bind("tab: complete")
#pynetdev.completer.readline.set_completer(auto_comp.complete)


__author__ = "Gary Wright"
__author_email__ = "gwright@secureneo.com"
__app_name__ = os.path.basename(sys.argv[0])
__license__ = "GPL"
__version__ = "1.0.0"

###
# Globals
def signal_handler(signal, frame):
        logger.warning('User has requested to quit.')
        sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

arg_desc = """Network automaton is a wrapper script to expose common
functionality of the pynetdev network device connector library."""

# Setup logging mechanism
args = logging_argparse(description=arg_desc)
logger = initialize_logger(args, __app_name__)

# Launch yaml configuration method
yaml_conf = pynetdev.config.yaml_conf_handler(logger)

class NetAutomaton(cmd.Cmd):
    """Simple command processor example."""
    def __init__(self, device_file=None, command_file=None):

        '''
        This section of __init__ is used to wire up
        the cmd.Cmd instance to drive the CLI
        '''

        cmd.Cmd.__init__(self) # init cmd cli class
        self.prompt = '{}network-automaton> '.format(
            pynetdev.config.COLOR_CODES['default'])
        self.intro = pynetdev.config.intro_banner() + pynetdev.config.INTRO_TEXT
        self.doc_header = 'available commands'
        self.misc_header = 'misc_header'
        self.undoc_header = 'undoc_header'
        self.ruler = '='

        self.DEVICES = list()
        self.COMMANDS = list()
        self.SHOW = ['devices', 'commands', 'logfile_name']
        self.DEVICE = ['add', 'remove', 'clearout']
        self.COMMAND = ['add', 'remove', 'clearout']

        '''
        End of __init__ settings for cmd.Cmd CLI.
        '''

        '''
        If the user has specified a devicelist and/or commands list
        as arguments, pass them to common.parse_file(filename) to
        retrieve, parse and load the contents.
        '''
        if device_file:
            self.DEVICES = common.parse_device_file(device_file, logger)
            if self.DEVICES:
                logger.info('Devices auto-added from {}\n{}'.format(device_file,
                                                               self.DEVICES))
        if command_file:
            self.COMMANDS = common.parse_command_file(command_file, logger)
            if self.COMMANDS:
                logger.info('Commands auto-added from {}\n{}'.format(command_file,
                                                                self.COMMANDS))

    def do_quit(self, line):
        print "Exiting net automaton"
        logger.info('User has requested to quit.')
        sys.exit()
    def help_quit(self):
        "Used to quit netAutomaton"
    def help_help(self):
        "Used to display help for topics. 'help' <topic keyword>"
    def do_EOF(self, line): print 'CTRL+D not allowed.'
    def help_EOF(self): ""

###
# BEGIN device functions
    def do_devicelist(self, line):
        """
        This function allows the user to specify a /path/to/filename
        of a newline separated list of devicenames or IPs.
        """
        devicelist_filename = common.user_specified_file()
        readline.set_completer(self.complete)

        self.DEVICES = common.parse_file(devicelist_filename, logger)
        logger.info('Devices added from {}\n{}'.format(devicelist_filename,
                                                       self.DEVICES))

    def help_devicelist(self):
        print ("""
        Used to specify an existing newline separated /path/to/devicelist.txt.
        The contents can be either DNS devicenames or IP's
        """)


    def help_device(self):
        print """
        Use this command to add / remove devices that you wish to interact with.
          ie. device add bl2-n10-cps-1a

        Multiple device add / remove is also supported.
          ie. device add bl2-n10-cps-1a;bl2-n10-cps-1b

        Specifying "device clearout" will clear the queue of network devices.

        Commands available are:

          device {} $devicename
          """.format(self.DEVICE)

    def do_device(self, line):
        """This function evaluates the user input specified from the "device"
        command and attempts to determine if syntax matches accepted commands.
        (currently add/remove).  If not display the help function."""
        if 'add' in line:
            self.DEVICES = common.add_entries(line.replace('add', '').strip(),
                                              self.DEVICES,
                                              logger)
        elif 'remove' in line:
            self.DEVICES = common.remove_entries(line.replace('remove', '').strip(),
                                                 self.DEVICES,
                                                 logger)
        elif 'clearout' in line:
            self.DEVICES = list()
        else:
            logger.warning('Invalid device keyword specified.')
            self.help_device()

    def complete_device(self, text, line, begidx, endidx):
        if not text:
            completions = self.DEVICE[:]
        else:
            completions = [ f
                            for f in self.DEVICE
                            if f.startswith(text)
                            ]
        return completions
# END device functions
###
###
# BEGIN command functions
    def do_commandlist(self, line):
        """
        This function allows the user to specify a /path/to/filename
        of a newline separated list of commands.
        """
        commandlist_filename = common.user_specified_file()
        readline.set_completer(self.complete)

        self.COMMANDS = common.parse_file(commandlist_filename, logger)
        logger.info('Commands added from {}\n{}'.format(commandlist_filename,
                                                       self.COMMANDS))

    def help_commandlist(self):
        print ("""
        Used to specify an existing newline separated
        /path/to/commandlist.txt.
               """)

    def help_command(self):
        print """
        Use this command to add / remove device commands that you wish to
        execute against devices.
          ie. command add show version

        Multiple command add / remove is also supported.
          ie. command add conf term;interface gi1/0;shut

        Specifying "command clearout" will clear the queue of commands.

        Commands available are:

          command {} $command
          """.format(self.COMMAND)

    def do_command(self, line):
        """This function evaluates the user input specified from the "command"
        command and attempts to determine if syntax matches accepted commands.
        (currently add/remove).  If not display the help function."""
        if 'add' in line:
            self.COMMANDS = common.add_entries(line.replace('add', '').strip(),
                                              self.COMMANDS,
                                              logger)
        elif 'remove' in line:
            self.COMMANDS = common.remove_entries(line.replace('remove', '').strip(),
                                                 self.COMMANDS,
                                                 logger)
        elif 'clearout' in line:
            self.COMMANDS = list()
            logger.warning(
                'Command list has been successfully cleared.')
        else:
            logger.warning('Invalid command keyword specified.')
            self.help_command()

    def complete_command(self, text, line, begidx, endidx):
        if not text:
            completions = self.COMMAND[:]
        else:
            completions = [ f
                            for f in self.COMMAND
                            if f.startswith(text)
                            ]
        return completions
# END command functions
###
# BEGIN show functions
    def help_show(self):
        print """
        Displays current status of the topic you have specified to show.
        ie. show device

        Commands available are:

        show {}
          """.format(self.SHOW)

    def do_show(self, line):
        """This function is used to display current values for
        the specified keyword. IF the keyword does not exist then
        display help message."""
        if 'device' in line:
            print ('[network device list]: {}'.format(self.DEVICES))
        elif 'commands' in line:
            print ('[command list]: {}'.format(self.COMMANDS))
        elif 'logfile_name' in line:
            print ('[current logfile location]: {}'.format(logger.filename))
        else:
            self.help_show()

    def complete_show(self, text, line, begidx, endidx):
        """This function handles tab completion of
        show commands."""
        if not text:
            completions = self.SHOW[:]
        else:
            completions = [ f
                            for f in self.SHOW
                            if f.startswith(text)
                            ]
        return completions
# END show functions
###

def main():

    devicelist = args.devicelist   # Optional, gathered from argparse
    commandlist = args.commandlist # Optional, gathered from argparse

    NetAutomaton(device_file=devicelist,
                 command_file=commandlist).cmdloop()

if __name__ == '__main__':
    main()
