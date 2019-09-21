import os
from setuptools import setup, find_packages

__version__ = '0.1'

setup(
    name='jublia_email_autosend',
    version=__version__,
    packages=find_packages(exclude=['tests']),
    install_requires=[
        'flask',
        'flask-sqlalchemy',
        'flask-restful',
        'flask-migrate',
        'flask-marshmallow',
        'marshmallow-sqlalchemy',
        'python-dotenv',
        'apispec[yaml]',
        'apispec-webframeworks',
    ],
    entry_points={
        'console_scripts': [
            'jublia_email_autosend = jublia_email_autosend.manage:cli'
        ]
    }
)
