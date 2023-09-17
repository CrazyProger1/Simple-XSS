import os
import sys
import toml

from config import (
    PAYLOADS_DIR,
    PAYLOAD_MAIN_FILE,
    PAYLOAD_INIT_FILE,
    PAYLOAD_PACKAGE_FILE
)
from app.utils import cli
from app.payload import PayloadMetadata
from sanitize_filename import sanitize


def validate_dirname(dirname: str):
    return dirname is not None


def create_payload(metadata: PayloadMetadata, dirname):
    abspath = os.path.abspath(os.path.join(PAYLOADS_DIR, dirname))
    main_file = os.path.join(abspath, PAYLOAD_MAIN_FILE)
    init_file = os.path.join(abspath, PAYLOAD_INIT_FILE)
    os.makedirs(abspath)

    with open(os.path.join(abspath, PAYLOAD_PACKAGE_FILE), 'w') as pf:
        toml.dump(metadata.__dict__, pf)

    open(main_file, 'w').close()
    open(init_file, 'w').close()

    cli.print_pos(f'Payload succesefully created: {abspath}')
    cli.print_pos(f'Main file: {main_file}')


def main():
    basedir = os.path.split(sys.argv[0])[0]

    if not os.path.isdir(os.path.join(basedir, PAYLOADS_DIR)):
        os.chdir('../')

    if not os.path.isdir(PAYLOADS_DIR):
        os.makedirs(PAYLOADS_DIR)

    metadata = PayloadMetadata()
    metadata.name = cli.ask('Enter name:')
    metadata.version = cli.ask('Enter version:')
    metadata.description = cli.ask('Enter description:')
    metadata.author = cli.ask('Enter your nickname/organization:')

    if not metadata.name:
        dirname = sanitize(cli.ask_validated('Payload directory name:', validate_dirname))
    else:
        dirname = sanitize(metadata.name)

    create_payload(metadata, dirname)


main()
