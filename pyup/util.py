import os
import uuid

import click


def style_success(message):
    status = click.style('Success', fg='green')
    return '{status}: {message}'.format(status=status, message=message)


def style_warning(message):
    status = click.style('Warning', fg='yellow')
    return '{status}: {message}'.format(status=status, message=message)


def style_error(message):
    status = click.style('Error', fg='red')
    return '{status}: {message}'.format(status=status, message=message)


def filename_to_uuid(filename):
    file_name, file_extension = os.path.splitext(filename)
    return str(uuid.uuid4()) + file_extension
