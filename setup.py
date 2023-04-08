from setuptools import setup, find_packages

setup(
    name='mypackage',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'flask',
        'flask-bootstrap'
        'boto3'
        
        # add any other required packages here
    ],
)