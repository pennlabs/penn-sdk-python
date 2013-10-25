from distutils.core import setup
import penn

setup(
    name='PennSDK',
    description='Python tools for building Penn-related applications',
    url='https://github.com/pennappslabs/penn-sdk-python',
    author='PennApps Labs',
    author_email='pennappslabs@gmail.com',
    version=penn.__version__,
    packages=['penn'],
    license='MIT',
    long_description=open('README.md').read(),
    install_requires=[
        'requests==1.2.3'
    ]
)
