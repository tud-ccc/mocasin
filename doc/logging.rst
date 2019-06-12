Logging
=======

Pykpn provides a customized logger that builds on the :mod:`logging` package.
Please use this logger whenever writing pykpn code. See the module
documentation for details: :mod:`pykpn.util.logging`.

Configuring the Logger
----------------------

The logger should be configured once in the main function.  The logger can be
easily setup by using the functions :func:`~pykpn.util.logging.add_cli_args`
and :func:`~pykpn.util.logging.setup_from_args`.
:func:`~pykpn.util.logging.add_cli_args` extends a given
:class:`~argparse.ArgumentParser` by cli arguments for configuring the
logger. :func:`~pykpn.util.logging.setup_from_args` then configures the logger
according to the parsed arguments.

.. code-block:: python

   import argparse
   from pykpn.util import logging

   log = logging.getLogger(__name__)

   def main():
       parser = argparse.ArgumentParser()
       logging.add_cli_args(parser)
       # add more args here ...
       args = parser.parse_args()
       logging.setup_from_args(args)

       # do something useful ...

   if __name__ == '__main__':
       main()

Using the Logger
----------------

To use the logger, simply add the following lines at the top of your module:

.. code-block:: python

   from pykpn.util import logging

   log = logging.getLogger(__name__)

Then you can use the ``log`` object to write log messages:

.. code-block:: python

   log.info("Info Test")
   log.debug("Debug Test")
   log.warn("Warning Test")
   log.error("Error Test")

Advanced Usage
--------------

Sometimes it is useful to automatically manipulate the output stream to display
additional information. This can be achieved by using a
:class:`logging.LoggerAdapter`. For instance
:class:`~pykpn.simulate.adapter.SimulateLoggerAdapter` is a custom adapter that
extends the printed message by the current simulation time and the name of the
simulated object being processed. An instance of :class:`logging.LoggerAdapter`
can be used as any other :class:`~logging.Logger` object.
