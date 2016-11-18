=======================================
PennSDK: Wrapper for Multiple Penn APIs
=======================================

.. image:: https://badge.fury.io/py/PennSDK.png
    :target: http://badge.fury.io/py/PennSDK

.. image:: https://travis-ci.org/pennlabs/penn-sdk-python.svg
    :target: https://travis-ci.org/pennlabs/penn-sdk-python

Penn SDK is the Python library for writing code that interfaces with University of Pennsylvania
data. It consists of wrappers for the Registrar, Dining, and
Directory API's


Getting an API key
------------------

To use these libraries, you must first obtain an API token and password,
which can be done here_. There are separate API tokens and password for each of dining, registrar, news/events/maps, transit, and directory.

There is also a Laundry API, Study Spaces API, and Calendar, which don't need a key.


Documentation
-------------

The full API documentation can be found at
https://esb.isc-seo.upenn.edu/8091/documentation/.

Documentation for the wrapper can be found at http://penn-sdk.readthedocs.org/

Installation
------------

You can install PennSDK easily using pip

.. code-block::

   $ sudo pip install PennSDK

easy_install also works

.. code-block::

   # sudo easy_install PennSDK

Getting Started
---------------
Once you have an API token and Password, you can use the wrapper as follows.

.. code-block:: python

    from penn import Registrar

    REG_USERNAME = 'MY_REGISTAR_USERNAME'
    REG_PASSWORD = 'MY_REGISTRAR_PASSWORD'

    r = Registrar(REG_USERNAME, REG_PASSWORD)

    cis120 = r.course('cis', '120')

    # cis120 is a dictionary parsed from the API json
    my_data = cis120['result_data']

All of other services (Dining, Directory, Transit, News, Map) follow this same basic format, except for the Laundry, Study Spaces, and Calendar API's, which don't need a username and password passed in at initialization. Refer to the wrapper documentation at http://penn-sdk.readthedocs.org/ for more info.


Running Tests
-------------

Once you have an API token and password, you can run the tests by creating a
``tests/credentials.py`` file with them as constants. Depending on what you
want to test, include the following variables. They will be retrieved from your
environment variables by default.

.. code-block:: python

    REG_USERNAME = 'MY_REGISTAR_USERNAME'
    REG_PASSWORD = 'MY_REGISTAR_PASSWORD'

    DIN_USERNAME = 'MY_DINING_USERNAME'
    DIN_PASSWORD = 'MY_DINING_PASSWORD'

    DIR_USERNAME = 'MY_DIRECTORY_USERNAME'
    DIR_PASSWORD = 'MY_DIRECTORY_PASSWORD'

    TRANSIT_USERNAME = 'MY_DIRECTORY_USERNAME'
    TRANSIT_PASSWORD = 'MY_DIRECTORY_PASSWORD'

Then run ``make test`` to run all tests in your shell.

Contributing & Bug Reporting
----------------------------

If you find a bug, please submit it through the `GitHub issues page`_.

Pull requests are welcome!

.. _`GitHub issues page`: https://github.com/pennlabs/penn-sdk-python/issues
.. _`here`: https://secure.www.upenn.edu/computing/da/webloginportal/eforms/index.html?content=kew/EDocLite?edlName=openDataRequestForm&userAction=initiate
