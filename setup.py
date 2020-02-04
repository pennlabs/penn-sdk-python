from setuptools import setup


setup(
    name='PennSDK',
    description='Python tools for building Penn-related applications',
    url='https://github.com/pennlabs/penn-sdk-python',
    author='Penn Labs',
    author_email='admin@pennlabs.org',
    version='1.8.7',
    packages=['penn'],
    license='MIT',
    package_data={
        # If any package contains *.txt or *.rst files, include them:
        '': ['*.txt', '*.rst'],
        'penn': ['data/laundry.csv'],
    },
    long_description=open('./README.rst').read(),
    install_requires=[
        'nameparser==0.5.6',
        'requests==2.20.0',
        'beautifulsoup4==4.6.0',
        'html5lib==1.0.1'
    ]
)
