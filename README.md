# chain-community-dashboard
DAO visualization tool

## Installation
All code has been tested on Linux, so, you must install the following dependencies to run the tool:

* python3 (3.7 or later)
* python3-pip
* virtualenv

Even if you install the above dependencies, you must also install the Python dependencies:

`pip3 install -r requirements.txt`

If you don't want to share Python dependencies among other projects, you must use a virtual environment, sush as [virtualenv](https://docs.python-guide.org/dev/virtualenvs/).

At first, create a folder where you are going to install all Python dependencies:

`virtualenv -p python3 venv/`

Now, you have to activate it:

`source venv/bin/activate`

Finally, you can install the dependencies:

`pip install -r requirements.txt`

## How to run it?
You can run it on debug mode, if you set an environment variable named `DEBUG`

`export DEBUG=TRUE`

After that, run the web app with:

`python3 index.py`

Now, visit `http://127.0.0.1:8050/apps/dashboard` in your web browser.

## How to test it?
Run all tests with:
`python3 -m pytest test/`

### Flags for hypothesis testing
Use this flag `--hypothesis-show-statistics` to show statistics.

Use the flag `--hypothesis-seed=<int>` to set a fixed seed, it's useful to reproduce a failure.