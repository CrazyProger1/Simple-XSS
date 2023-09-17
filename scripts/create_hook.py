import os
import sys
import toml

from settings import HOOKS_DIR, HOOK_PACKAGE_FILE, HOOK_MAIN_FILE
from app.utils import cli
from app.hook import HookMetadata
from sanitize_filename import sanitize


def validate_dirname(dirname: str):
    return dirname is not None


def create_hook(metadata: HookMetadata, dirname):
    abspath = os.path.abspath(os.path.join(HOOKS_DIR, dirname))
    main_file_path = os.path.join(abspath, HOOK_MAIN_FILE)
    os.makedirs(abspath)

    with open(os.path.join(abspath, HOOK_PACKAGE_FILE), 'w') as pf:
        toml.dump(metadata.__dict__, pf)

    open(main_file_path, 'w').close()

    cli.print_pos(f'Hook succesefully created: {abspath}')
    cli.print_pos(f'Main file: {main_file_path}')


def main():
    basedir = os.path.split(sys.argv[0])[0]

    if not os.path.isdir(os.path.join(basedir, HOOKS_DIR)):
        os.chdir('../')

    if not os.path.isdir(HOOKS_DIR):
        os.makedirs(HOOKS_DIR)

    metadata = HookMetadata()
    metadata.name = cli.ask('Enter name:')
    metadata.version = cli.ask('Enter version:')
    metadata.description = cli.ask('Enter description:')
    metadata.author = cli.ask('Enter your nickname/organization:')

    if not metadata.name:
        dirname = sanitize(cli.ask_validated('Hook directory name:', validate_dirname))
    else:
        dirname = sanitize(metadata.name)

    create_hook(metadata, dirname)


main()
