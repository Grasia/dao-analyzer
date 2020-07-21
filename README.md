# chain-community-dashboard
DAO visualization tool

## Download
Enter in your terminal (git must be installed) and write down:

`git clone https://github.com/Grasia/chain-community-dashboard`

After that, move to repository root directory with:

`cd chain-community-dashboard`

## Installation
All code has been tested on Linux, but it should work on Windows and macOS, 'cause it just uses the python environment.

So, you must install the following dependencies to run the tool:

* python3 (3.7 or later)
* python3-pip
* virtualenv (not essential)

Even if you install the above dependencies, you must also install the Python dependencies:

`pip3 install -r requirements.txt`

If you don't want to share Python dependencies among other projects, you should use a virtual environment, such as [virtualenv](https://docs.python-guide.org/dev/virtualenvs/).

At first, create a folder where you are going to install all Python dependencies:

`virtualenv -p python3 venv/`

Now, you have to activate it:

`source venv/bin/activate`

Finally, you can install the dependencies:

`pip install -r requirements.txt`

## How to run it?
Before launch the app, you have to run the following script in order to enable the cache stored in `datawarehouse/daostack`:

`python3 cache_scripts/daostack/main.py`

After a few minutes, you can now run the app with:

`python3 index.py`

Now, visit `http://127.0.0.1:8050/apps/daostack` in your web browser.

### Debug mode
Setting the environment variable, `DEBUG`, before running the app, will enable the debug mode.

`export DEBUG=TRUE`

## How to test it?
Run all tests with:
`python3 -m pytest test/`

### Flags for hypothesis testing
Use this flag `--hypothesis-show-statistics` to show statistics.

Use the flag `--hypothesis-seed=<int>` to set a fixed seed, it's useful to reproduce a failure.