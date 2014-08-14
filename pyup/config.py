import os

from six.moves import configparser

import click

from .util import style_success, style_warning, style_error


class TargetConfig(object):

    def __init__(self, app_name, config_file):
        self.app_name = app_name
        self.config_file = config_file

        self.target = None

        self.port = None
        self.hostname = None
        self.username = None
        self.target_dir = None
        self.url_prefix = None

    def is_complete(self):
        return self.port and self.hostname and self.username and self.target_dir and self.url_prefix

    def _read_section(self, parser, section_name):
        self.target = section_name

        section = parser[section_name]
        self.port = int(section.get('port', 22))
        self.hostname = section.get('hostname', None)
        self.username = section.get('username', None)
        self.target_dir = section.get('target_dir', None)
        self.url_prefix = section.get('url_prefix', None)

    def read_config(self, section=None):
        app_dir = click.get_app_dir(app_name=self.app_name, force_posix=True)
        cfg = os.path.join(app_dir, self.config_file)

        if not os.path.isdir(app_dir) or not os.path.isfile(cfg):
            click.echo(style_warning('No valid config files or targets found, executing config wizard.'))
            if not self.config_wizard():
                click.echo(style_error('Config wizard failed to complete successfully.'))
                return False

        parser = configparser.SafeConfigParser()
        parser.read([cfg])

        sections = parser.sections()

        if len(sections) == 0:
            click.echo(style_warning('The config file appears to be empty.'))
            if click.confirm('Rewrite config using config wizard?'):
                if self.config_wizard():
                    parser.read([cfg])
                    sections = parser.sections()
                else:
                    click.echo(style_error('Config wizard failed to complete successfully.'))
                    return False
            else:
                return False

        if section:
            if section in sections:
                self._read_section(parser, section)
                return True
            else:
                click.echo(style_error('Target "{}" doesnt exist.'.format(section)))
                return False

        if len(sections) == 1:
            self._read_section(parser, sections[0])
            return True

        elif len(sections) > 1:
            click.echo(style_error('More than one target found! Please choose one of the following: {}'.format(
                ', '.join(sections))))
            return False

    def config_wizard(self):
        app_dir = click.get_app_dir(app_name=self.app_name, force_posix=True)
        cfg = os.path.join(app_dir, self.config_file)

        click.echo('This wizard will guide you through the initial configuration.')

        if not os.path.isdir(app_dir):
            if click.confirm('Config directory "{}" not found. Create?'.format(app_dir)):
                os.makedirs(app_dir)
            else:
                return False

        if not os.path.isfile(cfg):
            if not click.confirm('Config file "{}" not found. Create?'.format(cfg)):
                return False

        parser = configparser.SafeConfigParser()
        while click.confirm('Add new target? ({:d} present)'.format((len(parser.sections())))):
            target = click.prompt("Enter the target's name/alias (example)")
            hostname = click.prompt("Enter the target's hostname or IP address (example.com)")
            port = click.prompt("Enter the target's SSH port", type=int, default=22)
            username = click.prompt("Enter your SSH username (user)")
            target_dir = click.prompt("Enter the directory to which files will be uploaded (public_html/)")
            url_prefix = click.prompt("Enter the base URL to which the file name will be appended"
                                      " (http://example.org/files/)")
            parser[target] = {
                'port': port,
                'hostname': hostname,
                'username': username,
                'target_dir': target_dir,
                'url_prefix': url_prefix,
            }
        with open(cfg, 'w') as configfile:
            parser.write(configfile)

        click.echo(style_success('Config file was saved successfully.'))
        return True
