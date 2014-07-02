#!/usr/bin/env python
"""
Execution classes for ssh based connections, using
fabric configuration.
"""
from fabric.api import *

env = env

env.hosts=["myark.cloudapp.net", "gnsase-cr.cloudapp.net"]
env.user="azureuser"
env.password=None
#env.port = 22
#env.timeout = 0 # Main timeout of ssh connect
env.parallel=True
#env.pool_size = 0 # Controls number of parallel process
env.abort_exception = None
env.abort_on_prompts = True
#env.command_timeout = 1
#env.key_filename = '/path/to/keyfiles'
#env.no_agent = True
#env.no_keys = True
#env.reject_unknown_hosts = True

###
# Custom exception
class CMDExecError(Exception):
    "Custom exception raised on error during cmd execution"
    pass

class ssh_execute(object):
    """
    Used to drive execution of commands list against
    the list of devices, using fabric.
    """
    def __init__(self, env_settings, logger):
        self.env = env
        self.env = env_settings
        self.env.hosts = env_settings.hosts
        self.logger = logger

    def init_hosts(self):
        self.env.hosts = self.env.hosts

    @parallel
    def parallel_run_cmd(self):
        env = self.env
        for command in self.env.commands:
            results = run (command)
            if results:
                self.logger.warning(
                    'command executed successfully, {}'.format(results))

    @serial
    def serial_run_cmd(self):
        env = self.env
        for command in self.env.commands:
            results = run (command)
            if results:
                self.logger.warning(
                    'command executed successfully, {}'.format(results))

    def run_tests(self):
        env = self.env
        print env
        print env.hosts

        if self.env.parallel:
            execute(self.parallel_run_cmd())
        else:
            execute(self.serial_run_cmd())
