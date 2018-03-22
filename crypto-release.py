import argparse

from git import Repo


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-mi', '--minor', action='store_true')
    parser.add_argument('-ma', '--major', action='store_true')
    parser.add_argument('-p', '--patch', action='store_true')
    parser.add_argument('-a', '--message', type=str)
    parser.add_argument('-t', '--tag', type=str)
    args = parser.parse_args()

    if not (args.minor and args.major and args.patch):
        args.minor = True

    if args.message:
        repo = Repo()
        git = repo.git
        git.add('-A')
        git.commit('-m {}'.format(args.message))
        git.push()
