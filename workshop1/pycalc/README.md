PyCalc
======

This is an example, simple Calculator app for the first PyArkansas Workshop.

Running
-------

First, you will need to create a virtual environment:

```shell
> python -m venv env
```

This will create an environment in the directory `env`

Next, activate the environment

On Windows:

```shell
> env\Scripts\activate
```

On Linux/Mac:

```shell
> source env/bin/activate
```

Next, install any runtime requirements:

```shell
> pip install -r requirements.txt
```

Finally, you can run the application with either

```shell
> python setup.py run
```

Or

```shell
> python -m pycalc
```

Installation
------------

To install PyCalc, simply run

```shell
> python setup.py install
```

This will create a program named PyCalc in the activated environment's
Scripts/bin folder.

Development
-----------

To develop on PyCalc, create a virtual environment, then also install the dev
requirements:

```shell
> pip install -r dev-requirements.txt
```

This will make it possible to run

```shell
> python setup.py check
```

Which will run `flake8`, `mypy`, and `pytest`. These tools help ensure that the
quality of the code is maintained.

License
-------

This code is public domain and is provided for educational purposes only, and is
provided without warranty or guarantee of functionality. Anyone is free to copy,
modify, and redistribute this code with or without attribution of any kind.
