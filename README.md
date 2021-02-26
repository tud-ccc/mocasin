mocasin
=====

A framework for modeling dataflow applications and their execution on MPSoC
platforms.

Installation
------------

It is recommended to install mocasin within a virtual environment. Currently we support Python versions 3.6, 3.7, 3.8 and 3.9.
You can create a new environment with
```
virtualenv -p python3 ~/virtualenvs/mocasin
```
Note that you can adjust the path to your needs. You can activate the previously created environment as follows:
```
source ~/source ~/virtualenvs/mocasin/bin/activate
```

Then you can install mocasin and all its dependencies from inside the mocasin root directory:
```
pip install .
```

If you plan to modify the mocasin code base, you should install the package in
development mode:
```
pip install -e .
```

This ensures that any modifications you make, will have an immediate effect to
your installed mocasin package.

You can now execute the mocasin command:
```
mocasin help
```

Configuration
-------------

mocasin uses [hydra](https://hydra.cc/) for its runtime configuration. The mocasin
package provides a basic set of general configuration files.
You can create your own configuration files and extend or override the default
ones. mocasin automatically loads all configuration files located in the local `conf/` directory. If that is not sufficient for your needs you can set the environment variable `export MOCASIN_CONF_PATH=<path1>:<path2>:<...>` to contain more paths

Examples
--------

### Simple tasks

mocasin can execute one of several tasks. It expects the first argument to be a
valid task and all the remaining arguments are passed to hydra.  The `help`
task we used above gives an overview about all available tasks.

`graph_to_dot` is a simple task that takes a dataflow graph and produces a dot file
that represents this graph. There are a view SDF and task graphs available
within the examples directory. See `examples/sdf3/` and `examples/tgff`.
For instance you can visualize an SDF application like this:
```
mocasin graph_to_dot graph=sdf3_reader sdf3.file=<abs_path>/examples/sdf3/medium_acyclic.xml  
```
or a task graph application like this:
```
mocasin graph_to_dot graph=tgff_reader tgff.directory=<abs_path>/examples/tgff/e3s-0.9/ tgff.file=auto-indust-cords.tgff
```
Note that it is currently required for path to be absolute. We are working on a fix that enables use of relative paths.

The above commands will generate an `*.dot` output file. This file can be
viewed for instance with the `xdot` command line tool. Note that hydra
outomatically changes the `CWD` and places the generated output in a
subdirctory depending on the current time: `outputs/<date>/<time>/`.

Hydra allows to print the whole configuration tree using the `-c`
argument. This gives you an overview of the parameters available for the task.
```
mocasin graph_to_dot graph=sdf3_reader -c job
```

### Simulation

One of mocasin's most important tasks is `simulate`. It simulates the exectution
of an application on a given platform. For this, we need also a mapping
that maps dataflow nodes to processors in the platform and traces that describe
the runtime behavior of the application. For instance:
```
mocasin simulate graph=sdf3_reader trace=sdf3_reader platform=odroid mapper=random sdf3.file=<abs_path>/examples/sdf3/medium_acyclic.xml
```
simulates the execution of the specified SDF3 application on the Odroid platform using a random mapping.

#### Trace Viewer

The simulation task also produces a simulation trace that can be viewed in
Google Chrome's built-in trace viewer. On default, the generated trace is
called `trace.json` and placed in the output directory
`outputs/<date>/<time>/`. This can be overwritten using the hydra parameter
`simtrace.file`. To view the trace, open `about://tracing` in Google Chrome
and load the previously generated trace file

Running Tests
-------------

mocasin comes with a set of tests. You can run them as follows:
```
python setup.py test
```

Autocompletion for bash/zsh 
-------------
mocasin supports bash autocompletion.  To activate you need to 
modify the file `misc/bash-autocomplete.sh`. Change the line:
```
MOCASIN_HOME=<path-to-your-mocasin-installation>
```
to point to your `mocasin` installation. For example, if this repository is
in `$HOME/mocasin-git/`, the script should point to:
```
MOCASIN_HOME=$HOME/mocasin-git/mocasin
```
Then, you can active bash autocompletion by running:

```
eval "$(cat misc/bash-autocomplete.sh)"
```
If you use the zsh shell this works by adding
```
autoload -Uz bashcompinit && bashcompinit
```
to your .zshrc configuration file.

Publications
------------

* Christian Menard, Andrés Goens, Gerald Hempel, Robert Khasanov, Julian
  Robledo, Felix Teweleitt, and Jeronimo Castrillon. 2021. Mocasin—Rapid
  Prototyping of Rapid Prototyping Tools: A Framework for Exploring New
  Approaches in Mapping Software to Heterogeneous Multi-cores. In *DroneSE
  and RAPIDO 2021, System Engineering for constrained embedded systems,
  January 18-20, 2021, Virtual event*. ACM, New York, NY, USA, 8 pages.
  https://doi.org/10.1145/3444950.3447285



