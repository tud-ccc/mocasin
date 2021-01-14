Writing Documentation
=====================

Documenting Code
----------------

Code should always be documented in place using pythons doc strings. Please use
the `Google Style`_ as it works well with sphinx and produces readable doc
strings. A good example of a well documented class within mocasin is
:class:`RuntimeChannel`. Note how it is possible to reference other methods or
classes within mocasin and even within other projects (as it is done for the
Environment class).

.. _Google Style: https://www.sphinx-doc.org/en/1.5/ext/example_google.html

General Text
------------

While code documentation is key for our project, we also want to have some
explanatory texts like this one. New sites can simply be added by creating a
new ``.rst`` file within the ``doc`` directory and referencing to it in the
toctree statement of ``doc\index.rst``. A full quide on resStructuredText can
be found here: http://docutils.sourceforge.net/docs/user/rst/quickref.html.

Configuration
-------------

The way sphinx generates our documentation can be configured in multiple
places, most notably in ``doc/conf.py``. For instance the dictionary
``intersphinx_mapping`` can be use to configure sources for external
documentation that can be referenced.

Updating Online Documentation
-----------------------------

Given root access to factor, the online documentation can be updated with the
following command:

.. code-block:: sh

   scp -r <path/to/mocasin>/doc/build/html/* root@factor:/var/www/mocasin
