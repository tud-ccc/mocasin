Testing
=======

Our test infrastructure is based on pytest_. See :ref:`run tests` for
instruction on how to run tests.

.. _pytest: https://docs.pytest.org/en/latest/

Writing Tests
-------------

Test should be placed in a sub-package named ``test`` (see for instance
`pykpn.simulate.test`). Pytest's auto-discovery searches for all modules
starting with ``test_`` and within the modules searches for all functions
starting with ``test_``. Each of these functions is considered an individual
test and executed automatically when running pytest.

Please refer to pytest's documentation_ for more details on how pytests helps
when writing tests. Especially useful are fixtures_ for providing test
input. Code that is common to all multiple modules within a package can be
placed in a module named ``conftest.py``. Pytest will import this module
automatically before running any tests. See :mod:`pykpn.simulate.test.test_process`
for an example test module.

.. _documentation: https://docs.pytest.org/en/latest/
.. _fixtures: https://docs.pytest.org/en/latest/fixture.html

Configuration
-------------

Pytest can be configured by creating a file name ``pytest.ini`` in the pykpn
root directory (where ``setup.py`` lives). See
https://docs.pytest.org/en/latest/reference.html#ini-options-ref for a list of
all configuration options. One important option is ``testpaths`` that can be
used to configure which tests should be run. pytest can be set to verbose by
adding ``addopts=-vv``. See the example below:

.. code-block:: ini

   [pytest]
   testpaths="scripts"
   addopts=-vv
