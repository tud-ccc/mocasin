Continuous Integration
======================

GitLab's continuous integration is configured by a file named
``.gitlab-ci.yml``.  As long as this file is present in a branch, the
configured CI jobs will be executed for this branch. This allows to modify the
configuration and the jobs to be run as is needed by each branch. See
https://docs.gitlab.com/ee/ci/yaml/ for documentation of the configuration
format.

There are currently two runners configured on factor. One excepts jobs tagged
with ``python3.6`` and the other excepts jobs tagged with ``python3.7``. Having
two separate runners allows for parallel execution of tests for both python
versions.
