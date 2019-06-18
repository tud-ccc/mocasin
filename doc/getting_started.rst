Getting Started
===============

Pykpn sources are available from https://cc.inf.tu-dresden.de/gitlab/pykpn/pykpn

Installation
------------

To use pykpn activate a virtual environment or create a new one as follows:

.. code-block:: sh

   virtualenv -p python3 ~/virtualenvs/pykpn
   source ~/virtualenvs/pykpn/bin/activate

Then we can either install pykpn or make it available for development:

.. code-block:: sh

   cd <path/to/pykpn>
   python setup.py install

or

.. code-block:: sh

   cd <path/to/pykpn>
   python setup.py develop

Please note that this also installs pynauty from the
``third_party_dependencies`` directory.

.. _run tests:

Run Tests
---------

The following command runs all tests:

.. code-block:: sh

   cd <path/to/pykpn>
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

   cd <path/to/pykpn>
   python setup.py doc

The resulting html files are located in ``doc/build/html``.

An Example
----------

Pykpn can be used for a multitude of tasks. One of the core functionalities is
the simulation of KPN applications running an a virtual platform. A simple
 can be started by the following command:

.. code-block:: sh

  cd <path/to/pykpn>
  slx_simulate apps/audio_filter/exynos/config.ini

This simulates the execution of the *Audio Filter* application executing on a
model of the *Exynos* platform.

You can make the output more verbose using ``-v`` or ``-vv``.
