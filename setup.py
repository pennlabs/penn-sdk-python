from setuptools import setup
import penn

setup(
    name='PennSDK',
    description='Python tools for building Penn-related applications',
    url='https://github.com/pennappslabs/penn-sdk-python',
    author='Penn Labs',
    author_email='pennappslabs@gmail.com',
    version=penn.__version__,
    packages=['penn'],
    license='MIT',
    package_data = {
        # If any package contains *.txt or *.rst files, include them:
        '': ['*.txt', '*.rst'],
    },
    long_description=open('./README.rst').read(),
    install_requires=[
        'requests==1.2.3'
    ]
)
