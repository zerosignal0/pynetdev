#!/usr/bin/env python
"""
This module is used to create a credential object, used
by pynetdev to feed fabric.
"""

class credential(object):
    """
    Intake username, auth type and return back a class
    object instance.
    """
    def __init__(self, username, password,
                 ssh_key=None, ssh_agent=None):

        self.username = username
        self.password = password
        self.ssh_key = ssh_key
        self.ssh_agent = ssh_agent

    @property
    def username(self):
        return self.username

    @property
    def password(self):
        return self.password

    @property
    def ssh_key(self):
        return self.ssh_key

    @property
    def ssh_agent(self):
        return self.ssh_agent
