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

        self.env = env_settings
        self.logger = logger


    @parallel
    def exec_task(self):
        for command in env.commands:
            results = run (str(command))
            if results:
                self.logger.warning('command executed successfully, {}'.format(results))

    def run_tests(self):
        execute(self.exec_task)
