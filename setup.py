from setuptools import setup

from pyup import __version__


setup(
    name='pyup',
    version=__version__,

    url='http://github.com/buckket/pyup',

    author='buckket',

    packages=['pyup'],
    entry_points={'console_scripts': ['pyup = pyup.pyup:pyup']},

    install_requires=['six', 'click', 'paramiko'],

    description='Simple file uploader',
    long_description=open('./README', 'r').read(),
    keywords='sftp, command-line tools',

    license='WTFPL',
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Utilities',
    ],
)
