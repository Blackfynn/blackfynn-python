.. _models:

.. module:: blackfynn.models

Data Models
============

These model classes are used to represent objects on the Blackfynn platform. Briefly, there are three major classes
of entities: "collection" classes, "data" classes, and "detail" or "helper" classes.

Base

.. autosummary::
   :nosignatures:

   BaseDataNode

Data Catalog Basics

.. autosummary::
   :nosignatures:

   Dataset
   Collection
   DataPackage

Time Series

.. autosummary::
   :nosignatures:

   TimeSeries
   TimeSeriesChannel
   TimeSeriesAnnotationLayer
   TimeSeriesAnnotation

Tabular

.. autosummary::
   :nosignatures:

   Tabular

.. Concepts

.. .. autosummary::
..    :nosignatures:

..    Concept
..    ConceptInstance
..    Relationship
..    Relationship


Base Class
------------

The ``BaseDataNode`` class provides the basic methods available on **all models** listed below.

.. autoclass:: BaseDataNode
   :members:
   :inherited-members:
   :exclude-members: add_properties, insert_property


Data Catalog Basics
--------------------

Note:
   A useful special method for the following classes is ``__contains__``, which enables you to do::

      if my_pkg in my_collection:
         print("the package", pkg, "is in the collection")

Dataset
^^^^^^^^
Datasets are core entities on the Blackfynn platform. All data must be placed in a Dataset, whether directly or nested. Datasets can be thought of as similar to "repositories" in GitHub; they exist directly underneath a user/organization, and all sharing is controlled from their level.

.. autoclass:: Dataset
   :members:
   :inherited-members:
   :exclude-members: add_collaborators, add_properties, insert_property

Collection
^^^^^^^^^^^^
Collections are collections of data that exist inside of a Dataset. These can be thought of as simililar to a folder or directory.

.. autoclass:: Collection
   :members:
   :inherited-members:
   :exclude-members: add_properties, insert_property

Data Package
^^^^^^^^^^^^^
The ``DataPackage`` class is used for all non-specific data classes (i.e. classes that do not need specialized methods).

.. autoclass:: DataPackage
   :members:
   :exclude-members:


Data-Specific Classes
----------------------

Timeseries
^^^^^^^^^^^^

.. autoclass:: TimeSeries
   :members:
   :show-inheritance:

.. autoclass:: TimeSeriesChannel
   :members:
   :show-inheritance:

.. autoclass:: TimeSeriesAnnotation
   :members:
   :show-inheritance:

.. autoclass:: TimeSeriesAnnotationLayer
   :members:
   :show-inheritance:

Tabular
^^^^^^^^^^^^

.. autoclass:: Tabular
   :members:
   :show-inheritance:


Models and Relationships
--------------------------

Models
^^^^^^^

.. autoclass:: Model
   :members:
   :inherited-members:

.. autoclass:: ModelProperty
   :members:
   :inherited-members:

.. autoclass:: ModelPropertyType
   :members:
   :inherited-members:

.. autoclass:: ModelPropertyEnumType
   :members:
   :inherited-members:

.. autoclass:: Record
   :members:
   :inherited-members:

.. autoclass:: RecordSet
   :members:
   :inherited-members:

Relationships
^^^^^^^^^^^^^^^

.. autoclass:: RelationshipType
   :members:
   :show-inheritance:

.. autoclass:: Relationship
   :members:
   :inherited-members:

.. autoclass:: RelationshipSet
   :members:
   :show-inheritance:
