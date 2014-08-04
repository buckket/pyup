#!/usr/bin/env python3

import os
import uuid
import urllib.parse

import click
import paramiko


SSH_HOSTNAME = "uncloaked.net"
SSH_USERNAME = "loom"
SSH_PORT = 22

TARGET_DIR = 'public_html/stuff/'
URL_PREFIX = 'http://uncloaked.net/~loom/stuff/'


def initialize_ssh_client(hostname, username, port=22):
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.WarningPolicy())
    try:
        client.connect(hostname=hostname, port=port, username=username)
    except paramiko.PasswordRequiredException:
        click.echo('Warning: a password is required for either plaintext auth or key file decryption!')
        password = click.prompt('Password', hide_input=True)
        try:
            client.connect(hostname=hostname, port=port, username=username, password=password)
        except paramiko.AuthenticationException:
            client.close()
            raise
    except paramiko.AuthenticationException:
        client.close()
        raise
    return client


def upload_file(source_file, target_dir, target_filename):
    client = initialize_ssh_client(hostname=SSH_HOSTNAME, username=SSH_USERNAME)
    sftp = client.open_sftp()
    sftp.chdir(target_dir)
    sftp.put(source_file, target_filename, confirm=True)
    sftp.close()
    client.close()
    return URL_PREFIX + target_filename


def filename_to_uuid(filename):
    file_name, file_extension = os.path.splitext(filename)
    return str(uuid.uuid4()) + file_extension


@click.command()
@click.option('-c', '--clipboard', help='paste URL to clipboard', is_flag=True, default=False)
@click.option('-l', '--launch', help='open URL in default browser', is_flag=True, default=False)
@click.option('-u', '--uuid', help='use uuids for filename', is_flag=True, default=False)
@click.argument('source_file', type=click.Path(resolve_path=True, exists=True))
@click.version_option(version='0.1', prog_name='pyup')
def pyup(clipboard, launch, uuid, source_file):

    if uuid:
        target_filename = filename_to_uuid(source_file)
    else:
        target_filename = str(os.path.basename(source_file))
        try:
            from slugify import slugify_filename
            target_filename = slugify_filename(target_filename)
        except ImportError:
            click.echo('Warning: slugify not available. Skipping! '
                       '(pip install awesome-slugify if you want to use this feature)')

    remote_url = upload_file(source_file, TARGET_DIR, target_filename)
    remote_url_safe = urllib.parse.quote(remote_url, safe='~:/')

    click.echo('Success: {url}'.format(url=remote_url_safe))

    if clipboard:
        try:
            import pyperclip
            pyperclip.copy(remote_url_safe)
        except ImportError:
            click.echo('Warning: pyperclip not installed. Unable to copy URL to clipboard.')

    if launch:
        click.launch(remote_url_safe)


if __name__ == '__main__':
    pyup()
