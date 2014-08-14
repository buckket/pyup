import click
import paramiko

from .util import style_success, style_warning, style_error


def initialize_ssh_client(hostname, username, port=22):
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.WarningPolicy())
    try:
        client.connect(hostname=hostname, port=port, username=username)
    except paramiko.PasswordRequiredException:
        click.echo(style_error('A password is required for either plaintext auth or key file decryption!'))
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


def upload_file(target, source_file, target_filename, force=False):
    client = initialize_ssh_client(hostname=target.hostname, username=target.username, port=target.port)
    sftp = client.open_sftp()
    sftp.chdir(target.target_dir)

    try:
        sftp.stat(target_filename)
    except IOError:  # using IOError here instead of FileNotFoundError to support Python 2 and 3
        sftp.put(source_file, target_filename, confirm=True)
    else:
        msg = style_warning('File "{}" already exists. Do you want to overwrite?'.format(target_filename))
        if force or click.confirm(msg):
            sftp.put(source_file, target_filename, confirm=True)

    sftp.close()
    client.close()

    return target.url_prefix + target_filename
