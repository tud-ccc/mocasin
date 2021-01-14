Getting Started
===============

Mocasin sources are available from https://cc.inf.tu-dresden.de/gitlab/mocasin/mocasin

Dependencies
------------

The mocasin package depends on python and virtualenv. We support python 3.6 and python 3.7. To use some of the numerical libraries included you also need BLAS+LAPACK.

In a Debian-based system (e.g. Ubuntu), you can install these as follows:

.. code-block:: sh

   sudo apt-get install python3.7 python3-virtualenv libblas-dev liblapack-dev 

Installation
------------

To use mocasin activate a virtual environment or create a new one as follows:

.. code-block:: sh

   virtualenv -p python3 ~/virtualenvs/mocasin
   source ~/virtualenvs/mocasin/bin/activate

Then we can either install mocasin or make it available for development:

.. code-block:: sh

   cd <path/to/mocasin>
   python setup.py install

or

.. code-block:: sh

   cd <path/to/mocasin>
   python setup.py develop

Please note that this also installs pynauty from the
``third_party_dependencies`` directory.

.. _run tests:

Run Tests
---------

The following command runs all tests:

.. code-block:: sh

   cd <path/to/mocasin>
   python setup.py pytest

Pytest can be configured by creating a file ``pytest.ini``. A list of available
options can be found here:
https://docs.pytest.org/en/latest/reference.html#configuration-options. For
instance, the option 'testpath' can be used to run test only within one
directory. This is especially useful during development as it allows to only
run selected tests.

Building the Documentation
--------------------------

The documentation is build by the following command:

.. code-block:: sh

   cd <path/to/mocasin>
   python setup.py doc

The resulting html files are located in ``doc/build/html``.

An Example
----------

Mocasin can be used for a multitude of tasks. One of the core functionalities is
the simulation of KPN applications running an a virtual platform. A simple
 can be started by the following command:

.. code-block:: sh

  cd <path/to/mocasin>
  scripts/mocasin_manager.py task=simulate app_name=audio_filter platform_name=exynos

This simulates the execution of the *Audio Filter* application executing on a
model of the *Exynos* platform. Here we are using the mocasin_manager, which is
a general manager script that has all tasks available. In fact, since the default
application and platform are *Audio Filter* and *Exynos*, we could run the command as:

.. code-block:: sh

  cd <path/to/mocasin>
  scripts/mocasin_manager.py task=simulate

You can make the output more verbose by changing the log level, e.g. ``log_level=INFO``
or ``log_level=DEBUG``. The default is ``log_level=WARNING``, by setting it to ``log_level=ERROR`` you can also
suppress warnings.

Using the ``hydra.verbose`` option, you can also show the debug output of specfig
packages or modules. For instance:

.. code-block:: sh

  cd <path/to/mocasin>
  scripts/mocasin_manager.py task=simulate log_level=INFO hydra.verbose=mocasin.simulate.channel



To see the available options, like tasks, applications or architectures, use

.. code-block:: sh

  cd <path/to/mocasin>
  scripts/mocasin_manager.py --help
