from setuptools import setup


setup(
    name='PennSDK',
    description='Python tools for building Penn-related applications',
    url='https://github.com/pennlabs/penn-sdk-python',
    author='Penn Labs',
    author_email='pennappslabs@gmail.com',
    version='1.2.1',
    packages=['penn'],
    license='MIT',
    package_data={
        # If any package contains *.txt or *.rst files, include them:
        '': ['*.txt', '*.rst'],
    },
    long_description=open('./README.rst').read(),
    install_requires=[
        'requests==2.4.3',
        'beautifulsoup4==4.3.2',
        'html5lib==0.999'
    ]
)
