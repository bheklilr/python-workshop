from setuptools import setup, find_packages
from setuptools import Command
from pkg_resources import EntryPoint, Distribution
import subprocess as sp

version = '1.0.0'


class CheckCommand(Command):
    """This is a custom setup.py command that runs multiple code quality tools.
    This class is passed to the `setup` method and is used to extend the default
    commands for setup.py.  To find out what all commands are available, try
    running `python setup.py --help-commands`.

    It works by inheriting from `setuptools.Command` and overriding the `run()`
    method.  The `run` method is where the logic for this command is defined.

    Because the `Command` class expects there to be arguments most of the time,
    there are two other methods, `initialize_options` and `finalize_options`
    that must also be defined for this class to work, even if they do nothing.

    Right now, the tools that are run are:

      * flake8 - A style checking tool. This checks for problems like lines that
                 are too long, variable names that don't follow the same
                 convention, and common problems that could become bugs.
      * mypy - A static type checker that takes advantage of the new type
               annotations in Python 3.6
      * pytest - A powerful unit testing framework. Testing code is important to
                 ensure correctness and robustness of code.
    """

    #: This class-level variable is where you would place any additional
    #: arguments if you needed them.
    user_options = []

    def initialize_options(self):
        """The `Command` class requires that this method is defined."""
        pass

    def finalize_options(self):
        """The `Command` class requires that this method is defined as well. Did
        you know that if you have a docstring in an empty method you don't need
        a `pass` statement?
        """

    def run_flake8(self):
        try:
            import flake8  # noqa
        except ImportError:
            self.warn('flake8 is not installed, skipping code style checks.')
        else:
            self.announce('Checking code style...', level=2)
            output = sp.getoutput('flake8 pycalc')
            if len(output) > 0:
                self.announce('Code style problems found:', level=3)
                for line in output.split('\n'):
                    self.announce('\t' + line, level=3)

    def run_mypy(self):
        try:
            import mypy  # noqa
        except ImportError:
            self.warn('mypy is not installed, skipping type checks.')
        else:
            self.announce('Type checking...', level=2)
            output = sp.getoutput('mypy pycalc')
            if len(output) > 0:
                self.announce('Type problems found:', level=3)
                for line in output.split('\n'):
                    self.announce('\t' + line, level=3)

    def run_pytest(self):
        try:
            import pytest
        except ImportError:
            self.warn('pytest is not installed, skipping tests.')
        else:
            pytest.cmdline.main([])

    def run(self):
        self.run_flake8()
        self.run_mypy()
        self.run_pytest()


class RunCommand(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        # Get the entry points, with gui_scripts taking precedence
        scripts = self.distribution.entry_points.get(
            'gui_scripts',
            self.distribution.entry_points.get('console_scripts', []),
        )
        if len(scripts) == 0:
            self.warn('No scripts defined in gui_scripts or console_scripts.')
            return

        script = scripts[0]

        if len(scripts) > 1:
            self.warn('More than one script specified, running the first one: {}'.format(script))

        # This is a bit advanced, but use the pkg_resources module to load the
        # entry point.  In order to actually load it, we have to provide a
        # Distribution object, and an empty Distribution will work.
        ep = EntryPoint.parse(script, dist=Distribution())
        # Load the entry point (this is the actual function to run)
        function_to_run = ep.load()
        # And run it
        function_to_run()


setup(
    name="pycalc",
    version=version,
    author="Aaron Stevens",
    author_email="bheklilr2@gmail.com",
    description="A simple calculator app",
    packages=find_packages('.', exclude=['docs', 'tests']),
    entry_points={
        'gui_scripts': [
            'PyCalc=pycalc.__main__:main'
        ]
    },
    setup_requires=[
        'mypy',
        'flake8',
        'pytest',
    ],
    cmdclass={
        'check': CheckCommand,
        'run': RunCommand,
    }
)
