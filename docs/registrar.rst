.. _registrar:

Registrar API Wrapper
=====================

.. module:: penn.registrar

This documentation explains the methods of the :class:`Registrar <Registrar>`
object. For the specific fields on the objects returned by these methods,
see `the official documentation
<https://esb.isc-seo.upenn.edu/8091/documentation/>`_.

.. note::
    The Penn Data Warehouse performs nightly maintenance, which causes
    downtime for Penn InTouch and the Penn OpenData Registrar API. This will throw
    an :code:`APIError` in the SDK, which client applications can catch and try to
    fetch the data again later.

.. autoclass:: penn.registrar.Registrar
   :members:
