Mocasin Coding Style
====================

Auto-Formatting
---------------

We use [black](https://black.readthedocs.io/en/stable/) to automatically format
our code base. This is enforced in our CI tests and only correctly formatted
code is accepted. To apply black to your code simply run `black .` in the
repository root. Note that most IDEs allow integrating `black` directly in the
workflow and, for instance, run black automatically on each
save. Alternatively, [git hooks](https://git-scm.com/book/pl/v2/Customizing-Git-Git-Hooks)
could be setup to automatically apply black before each commit.

To setup the git hooks, please perform the following actions:
1. Install `pre-commit`: `pip install pre-commit`
2. Add the file `.pre-commit-config.yaml` to the root of the project with the
following content:
```
repos:
  - repo: https://github.com/psf/black
    rev: stable
    hooks:
      - id: black
        language_version: python3
```

3. Then execute `pre-commit install` to install git hooks in your `.git/`
 directory.

You can update the hooks to the latest version by running
 `pre-commit autoupdate`.

Linting
-------

Auto-formatting does not cover all aspects of programming. While it enforces a
specific look, it does not check for common problems in the code base and does
not enforce best practice. We use [flake8](https://flake8.pycqa.org/en/latest/)
for additional linting. Our code base currently does not comply with flake8 in
large parts. Thus we do not enforce compatibility in our CI tests. However,
the goal is to add warning free code in all new commits.

### Setup

To run flake8, please install `flake8` as well as the `pep8-naming` and
`flak8-docstrings` plugins:
```
pip install flake8 pep8-naming flake8-docstrings
```

Run flak8 with:
```
flake8 .
```
or
```
flake8 path/to/file.py
```

Note that many IDEs support integrating flake8 in the workflow. elpy for emacs,
for instance, automatically shows warnings reported by flake8 without
additional configuration.

### Ignoring rules

Sometimes it is reasonable to violate the rules flake8 checks for. For
instance, a long line could not be avoided, maybe because a comment contains a
very long URL. In such cases, rules can be disabled with `# noqa <rule>`.
For example:
```
example = lambda: 'example'  # noqa: E731
```
Be sure to always specify a specific rule and never use `# noqa` without a
rule. Should it turn out that a rule does not make sense at all for our code
base, we can discuss to ignore this rule in `setup.cfg`

Documentation
-------------

Any new code should at least provide a minimal documentation (this is checked
by `flake8-docstrings`). We use the [Google Style](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html)
to format our docstrings. This style is both easy to parse by humans and well
supported by `sphinx-apidoc` for automatically generating API documentation.
Note that we currently don't use this style consistently in our code base, but
any new commits should use the Google Style.

All Other Aspects
-----------------

For all other aspects of coding style, we don't enforce strict rules. However,
the primary objective should be to write code that is easy to parse and
understand by you as well as other developers. For further reading of good
practice, we refer to the
[Goole Python Style Guide](https://google.github.io/styleguide/pyguide.html).
