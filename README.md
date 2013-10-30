Penn Course API Client for Python
====

This module is a thin Python wrapper for the Penn registrar API that provides basic convenience
functions for consuming all three API endpoints.


Getting an API key
----

To use this library, you must first obtain an API token and password, which can be done
[here](https://secure.www.upenn.edu/computing/da/webloginportal/eforms).

Documentation
----

The full API documentation can be found [here](https://esb.isc-seo.upenn.edu/8091/documentation/).
Documentation for the wrapper can be found at http://penn-sdk.readthedocs.org/

Running Tests
----

Once you have an API token and password, you can run the tests by creating a `tests/credentials.py`
file with them as constants:

```
USERNAME = 'MY_USERNAME'
PASSWORD = 'MY_PASSWORD'
```

Then run `python tests/registrar_tests.py`.

Contributing and Bug Reporting
----

If you find a bug, please submit it through the
[GitHub issues page](https://github.com/pennappslabs/penn-sdk-python/issues).

Pull requests are welcome!
