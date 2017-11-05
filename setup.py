from setuptools import setup


setup(
    name='PennSDK',
    description='Python tools for building Penn-related applications',
    url='https://github.com/pennlabs/penn-sdk-python',
    author='Penn Labs',
    author_email='admin@pennlabs.org',
    version='1.6.6',
    packages=['penn'],
    license='MIT',
    package_data={
        # If any package contains *.txt or *.rst files, include them:
        '': ['*.txt', '*.rst'],
        'penn': ['data/laundry.csv'],
    },
    long_description=open('./README.rst').read(),
    install_requires=[
        'nameparser==0.4.0',
        'requests==2.4.3',
        'beautifulsoup4==4.3.2',
        'html5lib==0.999'
    ]
)
