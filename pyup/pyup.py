import os

from six.moves import urllib

import click

from . import __app_name__
from . import __version__

from .ssh import upload_file
from .config import TargetConfig
from .util import style_success, style_warning, style_error
from .util import filename_to_uuid


@click.command()
@click.option('-c', '--clipboard', help='paste URL to clipboard', is_flag=True, default=False)
@click.option('-l', '--launch', help='open URL in browser', is_flag=True, default=False)
@click.option('-u', '--uuid', help='use a uuid as filename', is_flag=True, default=False)
@click.option('-f', '--force', help='overwrite file without asking', is_flag=True, default=False)
@click.argument('source_file', type=click.Path(resolve_path=True, exists=True, readable=True))
@click.argument('target', type=click.STRING, required=False)
@click.version_option(version=__version__, prog_name=__app_name__)
def pyup(clipboard, launch, uuid, force, source_file, target):

    # app_config = AppConfig(app_name=__app_name__, config_file='pyup.ini')
    # app_config.read_config()

    target_config = TargetConfig(app_name=__app_name__, config_file='targets.ini')
    if not target_config.read_config(target):
        return False
    if not target_config.is_complete():
        click.echo(style_error('Config values are missing.'))
        return False

    if uuid:
        target_filename = filename_to_uuid(source_file)
    else:
        target_filename = str(os.path.basename(source_file))
        try:
            from slugify import slugify_filename
            target_filename = slugify_filename(target_filename)
        except ImportError:
            click.echo(style_warning('slugify not available. Skipping! '
                                     '(pip install awesome-slugify if you want to use this feature)'))

    remote_url = upload_file(target_config, source_file, target_filename, force)
    remote_url_safe = urllib.parse.quote(remote_url, safe='~:/')

    if clipboard:
        try:
            import pyperclip
            pyperclip.copy(remote_url_safe)
        except ImportError:
            click.echo(style_warning('pyperclip not installed. Unable to copy URL to clipboard.'))
    if launch:
        click.launch(remote_url_safe)

    click.echo(style_success(remote_url_safe))


if __name__ == '__main__':
    pyup()
