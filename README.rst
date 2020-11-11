blackfynn-python
================

.. image:: https://travis-ci.org/Blackfynn/blackfynn-python.svg?branch=master
    :target: https://travis-ci.org/Blackfynn/blackfynn-python
.. image:: https://codecov.io/gh/Blackfynn/blackfynn-python/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/Blackfynn/blackfynn-python
.. image:: https://img.shields.io/pypi/pyversions/blackfynn.svg
    :target: https://pypi.org/project/blackfynn/

Python client and command line tool for Blackfynn.

Installation
------------

To install, run

.. code:: bash

    pip install -U blackfynn

See the `installation notes`_ for more details.

.. _installation notes: https://github.com/Blackfynn/blackfynn-python/blob/master/INSTALL.rst

Release
-------

To release, you should:

- Change CHANGELOG.md with the proper changes for the release
- Modify the version in __init.py__
- Merge the branch into master
- Create a new Github Release

Documentation
-------------

Client and command line documentation can be found on `Blackfynn’s
documentation website`_.

.. _Blackfynn’s documentation website: http://developer.blackfynn.io/python

You can also `contribute`_ to Blackfynn's documentation to improve this project and help others learn.

.. _contribute: https://github.com/Blackfynn/blackfynn-python/blob/master/docs/CONTRIBUTION_TEMPLATE.md

Tests
-------------
Install the test requirements before running `pytest`_:

.. _pytest: https://docs.pytest.org/en/latest/usage.html

.. code:: bash

    make install
    pytest

To run the Blackfynn CLI Agent integration tests, you need to `install the agent`_
and run the tests with the `--agent` argument:

.. _install the agent: https://developer.blackfynn.io/agent/index.html

.. code:: bash

    pytest --agent


Contribution
-------------

Please make sure to read the `Contributing Guide`_ before making a pull request.

.. _Contributing Guide: https://github.com/Blackfynn/blackfynn-python/blob/master/docs/CONTRIBUTION_TEMPLATE.md



Changelog
-------------

Changes for each release are documented in the `release notes`_.

.. _release notes: https://github.com/Blackfynn/blackfynn-python/blob/master/CHANGELOG.md
