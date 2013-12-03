===============================
PennSDK: Penn Course API Client
===============================

.. image:: https://badge.fury.io/py/PennSDK.png
    :target: http://badge.fury.io/py/PennSDK

.. image:: https://pypip.in/d/PennSDK/badge.png
        :target: https://crate.io/packages/PennSDK/

PennSDK is a thin Python wrapper for the Penn registrar API that provides basic convenience
functions for consuming all three API endpoints.


Getting an API key
------------------

To use this library, you must first obtain an API token and password, which can be done
here_.

Documentation
-------------

The full API documentation can be found at https://esb.isc-seo.upenn.edu/8091/documentation/.

Documentation for the wrapper can be found at http://penn-sdk.readthedocs.org/

Running Tests
-------------

Once you have an API token and password, you can run the tests by creating a ``tests/credentials.py``
file with them as constants:

.. code-block:: python

    USERNAME = 'MY_USERNAME'
    PASSWORD = 'MY_PASSWORD'

Then run ``python tests/registrar_tests.py``.

Contributing & Bug Reporting
----------------------------

If you find a bug, please submit it through the `GitHub issues page`_.

Pull requests are welcome!

.. _`GitHub issues page`: https://github.com/pennappslabs/penn-sdk-python/issues
.. _`here`: https://secure.www.upenn.edu/computing/da/webloginportal/eforms/index.html?content=kew/EDocLite?edlName=registrarApiAccessForm&userAction=initiate
