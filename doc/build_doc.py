import distutils.cmd
import subprocess


class BuildDocCommand(distutils.cmd.Command):
    """A custom command to build the documentation

    Runs sphinx-apidoc first and than executes the sphinx comand.
    """

    description = 'run sphinx-apidoc and sphinx'
    user_options = []

    def initialize_options(self):
        """Set default values for options."""
        # Each user option must be listed here with their default value.

    def finalize_options(self):
        """Post-process options."""

    def run(self):
        """Run command."""
        subprocess.run(['sphinx-apidoc', '-f', '-o', './doc/api', './pykpn',
                        '**/test', 'test_*'])
        self.run_command('build_sphinx')
