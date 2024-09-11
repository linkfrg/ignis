What is Services?
====================

"Services" are objects that allows you to interact with various parts of your system.
For example, control audio, network, notifications and others.

To access them, use the universal ``Service`` class.
Call the ``get()`` method and pass the service name that you need to get access.

.. code-block:: python

    from ignis.services import Service

    SERVICE_NAME = Service.get("SERVICE_NAME")

For example, to get notifications service, use the code below:

.. code-block:: python

    from ignis.services import Service

    notifications = Service.get("notifications")


Where to get a list of all services?
---------------------------------------

A list of all services is available in the `API Reference <api_reference/services/index.rst>`_.