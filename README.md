Penn Course API Client for Python
=====

This module is a thin Python wrapper for the Penn registrar API that provides basic convenience
functions for consuming all three API endpoints.

Full API documentation [here](https://esb.isc-seo.upenn.edu/8091/documentation/).

Pull requests welcome!

Running Tests
-----

To run the tests, you first must obtain an API username and password (see the [main documentation](https://esb.isc-seo.upenn.edu/8091/documentation/)).

Once you have these, create a `tests/credentials.py` file with them as constants:

```
USERNAME = 'UPENN_OD_emjR_1000041'
PASSWORD = 'atvganiimuifudf1r9b6htpibg'
```

Then run `python tests/registrar_tests.py`.
