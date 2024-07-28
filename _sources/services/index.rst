Services
==========
There is a list of built-in services that provide additional functionality to build various components of your desktop.

To access a service, use the universal ``Service`` class:

.. code-block:: python

   from ignis.services import Service

   service_name = Service.get("service_name")

.. warning::
   You don't need to initialize services manually. They will be automatically initialized when imported.

.. danger::
   Some services have additional dependencies, which are listed on the service page.
   Without these dependencies, the service will crash Ignis when you try to import it.

.. toctree:: 
   :glob:
   :maxdepth: 1

   generated/*