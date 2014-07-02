#!/usr/bin/env python
"""
Execution classes for ssh based connections, using
fabric configuration.
"""
from fabric.api import *

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

        print 'in ssh_execute __init__, setting up env'

        self.env = env_settings
        self.logger = logger

        #env.hosts = self.env.hosts
        #env.password = self.env.password
        #env.user = self.env.user
        #env.parallel = self.env.parallel
        #env.abort_on_prompts = self.env.abort_on_prompts

    @parallel
    def task_1(self):
        for command in env.commands:
            results = run (str(command))
            if results:
                logging.warning('command executed successfully, {}'.format(results))

    def run_tests(self):
        execute(self.task_1)
