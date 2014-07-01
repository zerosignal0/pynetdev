#!/usr/bin/env python
"""
This file contains helper functions for use by the
net automaton wrapper script.
"""
import sys
import os.path
import glob
import readline

def query_yes_no(question, default="no"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
    It must be "yes" (the default), "no" or None (meaning
    an answer is required of the user).

    The "answer" return value is one of "yes" or "no".
    """
    valid = {"yes":True,   "y":True,  "ye":True,
             "no":False,     "n":False}
    if default == None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: {}".format(default))

    while True:
        sys.stdout.write(question + prompt)
        choice = raw_input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "\
                             "(or 'y' or 'n').\n")

def query_user(question, valid, default=None):
    """Ask a question using raw_input, evaluating the users answer
    against a list that contains the possible accepted inputs.
    """
    if default:
        sys.stdout.write('{} [default: {}]'.format(question,
                                                   default))
    else:
        sys.stdout.write(
            '{} [enter one of the following: {}]'.format(question,
                                                         valid))

    while True:
        choice = raw_input().lower()
        if default is not None and choice == '' and default in valid:
            return default
        elif choice in valid:
            return choice
        else:
            sys.stdout.write(
                '{} [enter one of the following: {}]'.format(question,
                                                             valid))

def tab_complete(text, state):
    return (glob.glob(text+'*')+[None])[state]

def user_specified_file():
    """
    This function prompts the user to enter the full
    filepath / filename for devicelist and commandlists.
    The usage of readline allows for tab completion access
    from the OS.
    """

    readline.set_completer_delims(' \t\n;')
    readline.parse_and_bind("tab: complete")
    readline.set_completer(tab_complete)

    while True:
        user_input = raw_input(
            'Specify /Path/To/File (tab-completion enabled): ')

        if os.path.isfile(user_input):
            return user_input

def parse_device_file(filename, logger):
    """
    This function will attempt to open the provided file
    and convert the contents within the file into a
    newline separated list object and return.
    """
    if not os.path.isfile(filename):
        logger.warning(
            '{} not found, skipping auto-load.'.format(filename))
        return list()
    else:
        with open(filename, 'r') as f:
            result = [line.strip('\n') for line in f if line]
            result = set([x for x in result if x])
            return list(result)

def parse_command_file(filename, logger):
    """
    This function will attempt to open the provided file
    and convert the contents within the file into a
    newline separated list object and return.
    """
    if not os.path.isfile(filename):
        logger.warning(
            '{} not found, skipping auto-load.'.format(filename))
        return list()
    else:
        with open(filename, 'r') as f:
            result = [line.strip('\n') for line in f if line]
            result = [x for x in result if x]
            return result

def add_entries(candidates, existing_entries, logger):
    """
    This function handles the addition of single/
    multiple entries to the set list "existing_entries"
    if candidates consists of intersecting entries.
    Returns existing_entries.
    """
    if ';' in candidates:
        candidates = candidates.split(';')
        candidates = set(candidates)
        candidates = list(candidates)

    if type(candidates) == list:
        for entry in candidates:
            if entry not in existing_entries:
                existing_entries.append(
                    entry.lstrip().rstrip())
                logger.info('[{}] added entry.'.format(
                    entry.lstrip().rstrip()))

    else:
        if candidates not in existing_entries:
            existing_entries.append(
                candidates.lstrip().rstrip())
            logger.info('[{}] added entry.'.format(
                candidates.lstrip().rstrip()))

    return existing_entries

def remove_entries(candidates, existing_entries, logger):
    """
    This function handles the removal of single/
    multipleentries specified within
    candidates, and validated against the
    existing_devices list.  Returns existing_devices
    with any successfully removed devices popped.
    """
    if ';' in candidates:
        candidates = candidates.split(';')
        for entry in candidates:
            for x in existing_entries:
                if entry == x:

                    existing_entries.remove(entry)
                    logger.info(
                        '[{}] removed entry'.format(entry))

    else:
        for x in existing_entries:
            if candidates == x:
                existing_entries.remove(candidates)
                logger.info(
                    '[{}] removed entry.'.format(candidates))

    return existing_entries
