from setuptools import setup

setup(
    name='pyup',
    version='0.1',
    url='http://github.com/buckket/pyup',
    packages=['pyup'],
    description='Simple file uploader',
    entry_points={'console_scripts': ['pyup = pyup.pyup:pyup']},
    install_requires=['click', 'paramiko'],
)
