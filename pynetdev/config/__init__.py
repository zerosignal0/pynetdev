# -*- coding: utf-8 -*-
"""
This file contains configuration / supplemental functions
for pynetdev and the netautomaton wrapper script.
"""
import os, sys
from random import choice
import yaml

###
# Globals
GITHUB_URL = "https://github.com/zerosignal0/pynetdev"
INTRO_TEXT = """

Network automaton is a wrapper script for pynetdev and
enables users to perform automated tasks against one or more
network devices.

"""
COLOR_CODES = {

'default' : "\033[.0m",
'bold' : "\033[.1m",
'underline' : "\033[.4m",
'blink' : "\033[.5m",
'reverse' : "\033[.7m",

'red' : "\033[.31m",
'green' : "\033[.32m",
'yellow' : "\033[.33m",
'blue' : "\033[.34m",
'magenta' : "\033[.35m",
'cyan' : "\033[.36m",
'white' : "\033[.37m",


  }

def intro_banner():
    '''
    This function returns the intro banner for netautomaton
    by choosing a random banner from the files within pynetdev.config.
    '''

    banners = ['banner1', 'banner2', 'banner3',
               'banner4', 'banner5', 'banner6']

    banner_color = choice(COLOR_CODES.keys())
    banner_color = COLOR_CODES[banner_color]

    intro_banner_filename = choice(banners)

    banner_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
    abs_file_path = os.path.join(banner_dir, intro_banner_filename)

    with open(abs_file_path, 'r') as f:
        banner = f.read()

    return ("""{}
{}
                                                        GW 2014'
                                        {}
{}""".format(banner_color, banner, GITHUB_URL, COLOR_CODES['default']))

def yaml_conf_handler(logger):
    """
    This function will determine the executing user, and validate whether
    or not the ~/.pynetdev.yaml file exists.  If not, it will create
    a new copy, or load ~/.pynetdev.yaml.
    """
    home = os.path.expanduser("~")
    conf_file = home+'/.pynetdev.yaml'
    yaml_template_file = os.path.dirname(__file__)+'/default_conf_template.yaml'

    if not os.path.isfile(conf_file):
        # Create new ~/.pynetdev.yaml file in users homedir and load
        try:
            # Read the template yaml file, so that we can clone it out.
            with open(yaml_template_file) as f:
                config_template = yaml.safe_load(f)

            # Now write loaded template yaml to new file in conf_file
            with open(conf_file, 'w') as yaml_file:
                yaml_file.write( yaml.dump(config_template, default_flow_style=False))

            with open(conf_file, 'r') as yaml_file:
                return yaml_file['configuration']

        except Exception as e:
            logger.error(
                'Error during default configuration generation, {}. Unable to continue'.format(e))
            sys.exit(1)

    else:
        # Attempt to load ~/.pynetdev.yaml file in users homedir and return it
        logger.info(
            'Found existing {}, attempting load.'.format(
                conf_file))
        try:
            with open(conf_file) as f:
                config = yaml.safe_load(f)

            logger.info(
                '{} has been loaded successfully.'.format(conf_file))

            return config['configuration']
        except Exception as e:
            logger.error(
                'Unable to load {}, {}'.format(conf_file, e))
            logger.error(
                'Please fix bad entries in {}, or delete {} and run netautomaton.py again.'.format(
                    conf_file))
            sys.exit(1)
