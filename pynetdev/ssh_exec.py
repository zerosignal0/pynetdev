#!/usr/bin/env python
"""
Execution classes for ssh based connections, using
fabric configuration.
"""
from fabric.api import env, run, parallel, serial, execute

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
    def parallel_run_cmd(self):
        env = self.env_settings
        for command in self.env.commands:
            results = run (command)
            if results:
                self.logger.warning(
                    'command executed successfully, {}'.format(results))

    @serial
    def serial_run_cmd(self):
        env = self.env_settings
        for command in self.env.commands:
            results = run (command)
            if results:
                self.logger.warning(
                    'command executed successfully, {}'.format(results))

    def run_tests(self):
        env = self.env_settings

        if self.env.parallel:
            execute(self.parallel_run_cmd())
        else:
            execute(self.serial_run_cmd())
