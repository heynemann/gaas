#!/usr/bin/env python

### To use this file add lines in .ssh/authorized_keys like the following:
### command="/usr/bin/python /path/to/gaas/git_server.py --user=heynemann --conf /path/to/gaas/gaas.conf",no-port-forwarding,no-X11-forwarding,no-agent-forwarding,no-pty ssh-rsa <user ssh public key content>

import sys
import os
from os.path import abspath
import argparse

from gaas.config import Config


def parse_arguments(arguments):
    parser = argparse.ArgumentParser(description='git_server.py is a server for ssh git repos.')

    parser.add_argument('-u', '--user', help='User identified by the given ssh key.')
    parser.add_argument('-c', '--config', help='Configuration file path.')

    args = parser.parse_args(arguments)

    config_path = abspath(args.config)

    return {
        'user': args.user,
        'config_path': config_path
    }

def main(arguments):
    options = parse_arguments(arguments)
    user = options['user']
    config_path = options['config_path']

    config = Config.load(config_path)

    command = os.environ['SSH_ORIGINAL_COMMAND']

    userMap = {'username': ['reponame', 'reponame2'],
               'username2': ['reponame2', 'reponame3']}
    if user and command:
        command_parts = command.split()

        if command_parts[0] in ['git-receive-pack', 'git-upload-pack']:
            #if command.split()[1] in ["'/path/to/repositories/" + r + ".git'" for r in userMap[user]]:
            new_command = "%s '%s/%s'" % (command_parts[0], config.GIT_ROOT.rstrip('/'), command_parts[1].strip("'").lstrip('/'))
            os.system('exec git-shell -c "' + new_command + '"')
            #else:
                #sys.stderr.write("You can't access this repository.")

if __name__ == '__main__':
    main(sys.argv[1:])
