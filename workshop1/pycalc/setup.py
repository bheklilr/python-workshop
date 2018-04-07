from setuptools import setup, find_packages
from setuptools import Command
from pkg_resources import EntryPoint, Distribution
import subprocess as sp

version = '1.0.0'


class CodeQualityCommand(Command):
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

    description = 'Runs various code quality checks'

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
        """Runs the flake8 command on the pycalc module."""
        try:
            # This is imported inside this method since flake8 is only a
            # development dependency.  It may not be installed, so waiting to
            # import it until this method is run means that we can handle what
            # to do if it isn't installed.
            # The noqa commend here prevents flake8 from flagging this line as a
            # style problem.
            import flake8  # noqa
        except ImportError:
            self.warn('flake8 is not installed, skipping code style checks.')
        else:
            self.announce('Checking code style...', level=2)
            # The subprocess module provides tools for executing other programs
            # via the command line.  This is a very simple way to do this.
            output = sp.getoutput('flake8 pycalc')
            if len(output) > 0:
                self.announce('Code style problems found:', level=3)
                for line in output.split('\n'):
                    self.announce('\t' + line, level=3)

    def run_mypy(self):
        """Runs the mypy command on the pycalc module."""
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
        """Runs the pytest command on the pycalc's test module."""
        try:
            import pytest
        except ImportError:
            self.warn('pytest is not installed, skipping tests.')
        else:
            # pytest is nice in that it makes it easy to run its main method
            # without having to resort to using subprocess
            pytest.cmdline.main([])

    def run(self):
        self.run_flake8()
        self.run_mypy()
        self.run_pytest()


class RunCommand(Command):
    """This is a custom setup.py command that runs the pycalc main method to
    launch the program.  It is just a convenience method around running
    `python -m pycalc`
    """

    description = 'Runs the first gui_script or console_script'

    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        """This method could be simpler by using the subprocess module, but the
        "correct" way to do things is to use the pkg_resources module to load
        the main method dynamically using the specification given by the
        `entry_points`.  This means that if the `entry_points` is changed, then
        this method will still work.
        """

        # Get the entry points, with gui_scripts taking precedence
        gui_scripts = self.distribution.entry_points.get('gui_scripts', [])
        console_scripts = self.distribution.entry_points.get('console_scripts', [])
        scripts = gui_scripts + console_scripts

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


# The `setuptools.setup` function is the standard way to manage Python projects.
# Virtually every python project out there uses setuptools or it's older cousin
# distutils.
# This function takes a lot of metadata about your project, like the name,
# author, version, etc. and builds a command line interface for managing it.
#
# Try running `python setup.py --help-commands` to see all of the commands.
setup(
    name="pycalc",
    version=version,
    author="Aaron Stevens",
    author_email="bheklilr2@gmail.com",
    description="A simple calculator app",
    url="https://github.com/bheklilr/python-workshop/tree/master/workshop1/pycalc",
    packages=find_packages('.', exclude=['docs', 'tests']),
    license='UNLICENSE',
    keywords='example tkinter calculator',
    project_urls={
        'Bug Tracker': 'https://github.com/bheklilr/python-workshop/issues',
        'Source Code': 'https://github.com/bheklilr/python-workshop/tree/master/workshop1/pycalc',
    },
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
        'code_quality': CodeQualityCommand,
        'run': RunCommand,
    }
)
