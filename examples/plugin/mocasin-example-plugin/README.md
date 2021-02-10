mocasin-example-plugin
======================

This is a small example plugin that illustrates how mocasin can be extended by
external packages.


Installation
------------

Assuming you have installed mocasin already, simply run `pip install .` in this
directory to install the plugin. If you plan on changing the code in this
repository, you should install in developer mode with `pip install -e .`.

Usage
-----

After installation you have access to an example graph and its corresponding trace.
You can use them for arbitrary mocasin commands. For instance:
```
mocasin simulate graph=example trace=example mapper=random platform=odroid
```

How it works
------------

The key part is the `hydra_plugins` namespace package which provides a
[hydra search path plugin](https://hydra.cc/docs/advanced/plugins/).
This hydra plugin essentially expands hydra's search path by the `conf` directory
in the `mocasin_example_package`. This `conf` directory simply provides
additional configurations for the `graph` and `trace` config groups. These in
turn instruct hydra to instantiate the `ExampleGraph` and
`ExampleTraceGenerator` classes defined in the `mocasin_graph_plugin.graph` and
`mocasin_graph_plugin.trace` modules.
