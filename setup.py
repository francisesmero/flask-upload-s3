from setuptools import setup, find_packages

setup(
    name='mypackage',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'flask',
        'flask-bootstrap',
        'boto3',
        'Flask_SQLAlchemy',
        'Flask-Table',
        'botocore'
        # add any other required packages here
    ],
)