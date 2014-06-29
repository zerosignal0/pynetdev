#!/usr/bin/env python
"""
Logging library used by pynetdev to create logging stream handlers,
designate save location and specify logging attributes.
"""

import datetime
import logging
import os
import sys
import argparse
import inspect
import getpass

from rainbow_logging_handler import RainbowLoggingHandler

LOGGER = None #Setup default global
FORMATTER = None #Setup default global

def line_number():
    """Returns the current line number in our program. Used by debug mode."""
    return inspect.currentframe().f_back.f_lineno

def create_log_dir():
    """Determines users homedir and creates logging directory
       if it doesn't already exist."""
    logdir = os.path.join(os.path.expanduser('~'),'logs')

    if not os.path.exists(logdir):
        os.makedirs(logdir)

    return logdir

def logging_argparse(pre_parse=True, description=None):
    """Creates argparse for logging mechanism"""

    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-l',
                        '--log',
                        action="store",
                        default='info',
                        type=str,
                        nargs='?',
                        help="Specify the logging level you would like to display to STDOUT\
                         for this execution (Default is INFO).\
                         Choices are debug,info,warning,error.")
    parser.add_argument('-ld',
                        '--log_dir',
                        action="store",
                        default='',
                        type=str,
                        nargs='?',
                        help="Specify the logging directory to have logging files be stored. (Default is $HOMEDIR/logs/)")
    parser.add_argument('-dl',
                        '--devicelist',
                        action="store",
                        default='',
                        type=str,
                        nargs='?',
                        help="(Optional)Specify the filepath/filename.txt which contains\
                         new line separated network devicenames/IPs. ie.\
                         /path/to/devicelist.txt")
    parser.add_argument('-cl',
                        '--commandlist',
                        action="store",
                        default='',
                        type=str,
                        nargs='?',
                        help="(Optional)Specify the filepath/filename.txt which contains\
                         new line separated commands to execute on network devices. ie.\
                         /path/to/commandlist.txt")

    if pre_parse:
        return parser.parse_args()
    else:
        return parser

def contains(str, set):
    """Check whether 'str' contains ALL of the chars in 'set'"""
    return 0 not in [c in str for c in set]

def initialize_logger(args, script_name):
    LOGGER = logging.getLogger(script_name)

    FORMATTER = logging.Formatter(
        ""+script_name+" : "+str(getpass.getuser())+" : %(asctime)s : %(levelname)s : %(message)s",
                                  datefmt='%m/%d/%Y %I:%M:%S %p')

    # create console handler and set level to info
    logging.StreamHandler()

    # setup `RainbowLoggingHandler`
    handler   = RainbowLoggingHandler(
        sys.stderr,
        # Customizing each column's color
        color_pathname=('black', 'red'  , True), color_asctime=('white', None, False),
        color_funcName=('blue' , 'white', True), color_lineno=('yellow' , None, False),
    )

    handler.setFormatter(FORMATTER)
    LOGGER.addHandler(handler)

    # setup log level from arguments
    if args.log:
        if contains('DEBUG', args.log.upper()):
            handler.setLevel(logging.DEBUG)
            LOGGER.setLevel(logging.DEBUG)
        elif contains('WARNING', args.log.upper()):
            handler.setLevel(logging.WARNING)
            LOGGER.setLevel(logging.WARNING)
        elif contains('ERROR', args.log.upper()):
            handler.setLevel(logging.ERROR)
            LOGGER.setLevel(logging.ERROR)
        else:
            handler.setLevel(logging.INFO)
            LOGGER.setLevel(logging.INFO)
        LOGGER.info('Logging level has been set to {}'.format(args.log.upper()))

    # setup logging directory to store log files
    if args.log_dir:
        if os.path.isdir(args.log_dir):
            output_dir = args.log_dir
    else:
        output_dir = create_log_dir()
    LOGGER.info('Logging directory has been set to {}'.format(output_dir))


    # create individual execution file handler and set level to debug
    now = datetime.datetime.now()
    datetime_stamp = now.strftime("%Y-%m-%d_%H-%M-%S")
    datetime_stamp = ('{}_{}.log'.format(datetime_stamp, script_name.replace('.py','')))
    filename = os.path.join(output_dir, datetime_stamp)

    handler = logging.FileHandler(filename, "a")

    if contains('DEBUG', args.log.upper()):
        handler.setLevel(logging.DEBUG)
    elif contains('WARNING', args.log.upper()):
        handler.setLevel(logging.WARNING)
    elif contains('ERROR', args.log.upper()):
        handler.setLevel(logging.ERROR)
    else:
        handler.setLevel(logging.INFO)

    handler.setFormatter(FORMATTER)
    LOGGER.addHandler(handler)

    # display the exact file name / path to the user
    LOGGER.info('Logs for this session now being written to {}'.format(filename))

    # Attach filepath / filename string to logger
    LOGGER.filename = filename

    return LOGGER
