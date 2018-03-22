import argparse
from subprocess import check_output

from git import Repo
import semantic_version


def get_version_from_git():
    label = check_output(
        ['git', 'describe', 'version-test', '--tags']
    )
    label = label.strip().decode('UTF-8')
    return label if semantic_version.validate(label) else False


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-mi', '--minor', action='store_true')
    parser.add_argument('-ma', '--major', action='store_true')
    parser.add_argument('-p', '--patch', action='store_true')
    parser.add_argument('-a', '--message', type=str)
    args = vars(parser.parse_args())
    git_version = get_version_from_git()

    increment = {k: args[k] for k in args if args[k]}

    # No version arguments supplied. Defaulting to "patch" 0.0.x
    if not len(increment):
        git_version = semantic_version.Version(git_version)
        new_version = git_version.next_patch()

    # One version argument supplied. Either "major": x.0.0 or "minor": 0.x.0
    elif len(increment) == 1:
        git_version = semantic_version.Version(git_version)
        new_version = getattr(git_version, 'next_' + list(increment.keys())[0])()
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
        git.tag(new_version)
        git.push('origin tags')
    else:
        git.tag(new_version)
        git.push('origin --tags')
