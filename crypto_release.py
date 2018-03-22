#!/usr/bin/env python

import argparse
from subprocess import check_output

from git import Repo
import semantic_version


def get_version_from_git():
    print('right here')
    label = check_output(
        ['git', 'describe', 'version-test', '--tags']
    )
    git_version_string = label.strip().decode('UTF-8')
    git_version = semantic_version.Version(git_version_string)
    git_version = '.'.join(str(item) for item in list(git_version)[:3])
    return git_version if semantic_version.validate(git_version) else False


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-mi', '--minor', action='store_true')
    parser.add_argument('-ma', '--major', action='store_true')
    parser.add_argument('-p', '--patch', action='store_true')
    parser.add_argument('-a', '--message', type=str)
    args = vars(parser.parse_args())
    git_version = get_version_from_git()
    git_version = semantic_version.Version(git_version)
    #print("git: ", type(git_version))
    #git_version = semantic_version.Version(git_version)
    #git_version = '.'.join(str(item) for item in list(git_version)[:3])
    #git_version = semantic_version.Version(temp_version_string)
    #new_version = git_version.next_patch()
    #print("git: ", git_version)
    #print("new: ",new_version)

    increment = {k: args[k] for k in args if args[k] is True}
    print(increment)
    # No version arguments supplied. Defaulting to "patch" 0.0.x
    if not len(increment):
        #git_version = semantic_version.Version(git_version)
        new_version = git_version.next_patch()
        print(new_version)
        increment_type = 'minor'

    # One version argument supplied. Either "major": x.0.0 or "minor": 0.x.0
    elif len(increment) == 1:
        #git_version = semantic_version.Version(git_version)
        increment_type = list(increment.keys())[0]
        new_version = getattr(git_version, 'next_' + increment_type)()
        print(new_version)

    # Multiple version arguments supplied. Unsupported
    else:
        raise Exception("Multiple version arguments detected." +
                        " Please supply one or none to default to patch")

    repo = Repo()
    git = repo.git
    if args['message']:
        git.add('-A')
        git.commit('-m {}'.format(args['message']))
        git.push()

    git.tag(new_version, '-a', '-m', 'applied {}'.format(increment_type))
    git.push('origin', new_version)
