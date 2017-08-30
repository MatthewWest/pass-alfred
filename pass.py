#!/usr/bin/python
# encoding: utf-8

import sys
import os
if sys.version_info < (3,0):
    import pipes
else:
    import shlex


from workflow import Workflow


def search_key_for_pw(relpath):
    """Generate a string search key for a full path of a password file"""
    elements = []
    elements.append(os.path.splitext(relpath)[0])
    return u' '.join(elements)

def extract_pw_keys(path):
    """Allow recursive directory checking"""
    children = os.listdir(path)
    children = filter(lambda x: not (x[0] == '.'), children)
    full_paths = []

    for child in children:
        full_path = os.path.join(path, child)
        if os.path.isfile(full_path):
            full_paths.append(full_path)
        else:
            full_paths.extend(extract_pw_keys(full_path))

    return full_paths


def main(wflow):
    # The Workflow instance will be passed to the function
    # you call from `Workflow.run`
    # Your imports here if you want to catch import errors
    # or if the modules/packages are in a directory added via `Workflow(libraries=...)`

    args = wflow.args[0].split()
    # Get args from Workflow, already in normalised Unicode
    if len(args) == 0:
        query = None

    if args[0] == u'add' or args[0] == u'insert':
        if len(args) == 1:
            wflow.add_item('Add password to pass')
        elif len(args) == 2:
            wflow.add_item(u'pass ' + args[0] + u' ' + args[1],
                           arg=(u'pass ' + args[0] + u' ' + args[1]), valid=True)
        elif len(args) > 2:
            wflow.add_item(u'Do not include spaces in pass names', valid=False)

        wflow.send_feedback()
        exit()
    elif args[0] == u'edit':
        if len(args) == 1:
            wflow.add_item(u'Edit an existing password in pass')
            wf.send_feedback()
            exit()
        elif len(args) == 2:
            query = args[1]
        elif len(args) > 2:
            wflow.add_item(u'Do not include spaces in pass names', valid=False)
            wflow.send_feedback()
            exit()
        edit = True
        display = False
        rm = False
    elif args[0] == u'rm' or args[0] == u'remove' or args[0] == u'delete':
        if len(args) ==1:
            wflow.add_item(u'Remove a password from pass')
            wflow.send_feedback()
            exit()
        elif len(args) == 2:
            query = args[1]
        elif len(args) > 2:
            wflow.add_item(u'Do not include spaces in pass names', valid=False)
            wflow.send_feedback()
            exit()
        edit = False
        display = False
        rm = True
    elif len(args) == 1:
        if args[0] == u'grep':
            wflow.add_item(u'Grep for a string in the decrypted password files')
            wflow.send_feedback()
            exit()
        elif args[0] == u'init':
            wflow.add_item(u'Initialize the password store')
            wflow.send_feedback()
            exit()
        elif args[0] == u'ls':
            wflow.add_item(u'List names of passwords inside the tree')
            wflow.send_feedback()
            exit()
        elif args[0] == u'find' or args[0] == u'search':
            wflow.add_item(u'List names of passwords that match the argument')
            wflow.send_feedback()
            exit()
        elif args[0] == u'generate':
            wflow.add_item(u'Generate a password: generate pass-name pass-length')
            wflow.send_feedback()
            exit()
        elif args[0] == u'cp': # should be split out to its own command
            wflow.add_item(u'Copy a password from old-path to new-path')
            wflow.send_feedback()
            exit()
        elif args[0] == u'git':
            wflow.add_item(u'Execute git for the password store')
            wflow.send_feedback()
            exit()
        elif args[0] == u'show':
            query = args[1]
        else:
            query = args[0]
        display = True
        edit = False
        rm = False

    else:
        command = u'pass '
        for arg in args:
            command += arg + u' '
        wflow.add_item(command, arg=command, valid=True)
        wflow.send_feedback()
        exit()





    password_dir = os.path.expanduser('~/.password-store')

    if not os.path.exists(password_dir):
        wflow.add_item(u'Password directory not found', u'Specify with pdir')
    else:
        full_paths = extract_pw_keys(password_dir)
        rel_paths = [os.path.relpath(full_path, password_dir) for full_path in full_paths]
        results = wflow.filter(query, rel_paths, key=search_key_for_pw, min_score=20)

        for r in results:
            r = os.path.splitext(r)[0]
            if sys.version_info >= (3,0):
                r = shlex.quote(r)
            else:
                r = pipes.quote(r)

            if edit:
                wflow.add_item(r, arg=(u'pass edit ' + r), valid=True, autocomplete=(u'pass edit ' + r))
            if display:
                wflow.add_item(r, u'', arg= u'pass -c ' + r, valid=True, autocomplete=r)
            if rm:
                wflow.add_item(r, u'', arg=(u'pass rm ' + r), valid=True, autocomplete=(u'pass rm ' + r))

    # Add an item to Alfred feedback


    # Send output to Alfred
    wflow.send_feedback()


if __name__ == '__main__':
    wf = Workflow()
    sys.exit(wf.run(main))
