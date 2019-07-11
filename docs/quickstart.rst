Getting Started in Python
=========================

Python client and command line tool for Blackfynn.

Installation
------------

The Python client is compatible with Python 2.7 and 3.4-3.7.

.. code:: bash

    $ pip install -U blackfynn


Configuration
-------------

.. important::

    In order to conect to Blackfynn using *any* client, first you must
    `Generate an API token & secret <http://help.blackfynn.com/blackfynn-developer-tools/overview/creating-an-api-key-for-the-blackfynn-clients>`_.
    Once you have generated your API keys, don't close your browser window until
    you have used your keys in the following steps.

To create a configuration profile, run ``bf profile create`` from the command line:

.. code:: bash

    $ bf profile create

When prompted, give your profile a unique name, or press enter to name your profile ``default``:

.. code:: bash

   Profile name [default]: my_profile

When prompted, paste in your new API key (also called a token) and press enter:

.. code:: bash

   API token: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx

Now paste in the API secret key and press enter:

.. code:: bash

   API secret: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx

Finally, enter ``y`` to set this profile as the *default profile*:

.. code:: bash

   Would you like to set 'my_profile' as default (Y/n)? y
   Default profile: my_profile

To verify that your profile was set up correctly, run ``bf status``:

.. code:: bash

   $ bf status

   Active profile:
     my_profile

   Blackfynn environment:
     User          : <your email>
     Organization  : <your organization>
     API Location  : https://api.blackfynn.io
     Streaming API : https://streaming.blackfynn.io

Using this technique you can add multiple connection profiles belonging to different organizations.

Basic Usage
--------------

Import and Initialize
~~~~~~~~~~~~~~~~~~~~~~

.. note::

   If you are using Python 2.7 it is highly recommended that you add
   ``from __future__ import print_function`` to the top of your scripts. This will
   allow you to easily use Python 3 in the future.

.. code:: python

    from blackfynn import Blackfynn

    bf = Blackfynn()

This will use your *default profile* to establish a connection. Alternatively, you
may want to specify a profile explicitly by name:

.. code:: python

    bf = Blackfynn('my_profile')

Where ``my_profile`` is an existing profile.


Basic Operations
~~~~~~~~~~~~~~~~~~~~~~

Get your datasets::

    # print your available datasets
    for ds in bf.datasets():
        print(" Found a dataset: ", ds.name)

    # grab some dataset by name
    ds1 = bf.get_dataset('my dataset 1')

    # list items inside dataset (first level)
    print(ds1.items)

Upload some files into your dataset::

    ds1.upload('/path/to/data.pdf')

Get a data package::

    # use ID to get a package
    pkg = bf.get('N:package:1234-1234-1234-1235')

Rename it & add some properties::

    pkg.name = "My new package name"
    pkg.set_property('Temperature', 83.0)
    pkg.update()


Uploading files
----------------

.. note::
  You must upload files into a ``Dataset`` or ``Collection``.

You can upload using the ``.upload()`` methods provided on ``Dataset`` and ``Collection`` objects::

    # upload a file into a dataset (ds)
    ds.upload('/path/to/my_data.nii.gz')

Retrieving data
----------------

Let's say you grab a ``TimeSeries`` package::

    ts = bf.get('N:package:your-timeseries-id')

You can get the first minute of data in 1-second chunks::

    for chunk in ts.get_data_iter(chunk_size='1s', length='1m'):
        # do something with data (pandas Dataframe)
        print("Mean values =", chunk.mean())

You can do the same thing for a single channel::

    channel = ts.channels[0]
    for chunk in channel.get_data_iter(chunk_size='5s', length='10m'):
        # do something with data (pandas Series)
        print("Max value =", chunk.max())
