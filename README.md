# DAO-Analyzer
It is a tool to visualize DAO metrics. Now, it's focused on the [DAOstack](https://daostack.io/) ecosystem.

## Architecture
There is available a class diagram [here](https://github.com/Grasia/dao-analyzer/src/apps/daostack/class_diagram.png).

## Download
Enter in your terminal (git must be installed) and write down:

`git clone https://github.com/Grasia/dao-analyzer`

After that, move to repository root directory with:

`cd dao-analyzer`

## Installation
All code has been tested on Linux, but it should work on Windows and macOS, 'cause it just uses the python environment.

So, you must install the following dependencies to run the tool:

* python3 (3.7 or later)
* python3-pip
* virtualenv (not essential)

Now, install the Python dependencies:

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

Now, visit `http://127.0.0.1:8050` in your web browser.

### Debug mode
Setting the environment variable, `DEBUG`, before running the app, will enable the debug mode.

`export DEBUG=TRUE`

## How to test it?
Run all tests with:

`python3 -m pytest test/`

### Flags for hypothesis testing
Use this flag `--hypothesis-show-statistics` to show statistics.

Use the flag `--hypothesis-seed=<int>` to set a fixed seed, it's useful to reproduce a failure.

## Deploy
In order to fully deploy the app, use the `deploy.sh` script, which installs all the Python dependencies, updates the datawarehouse, and runs the web-app with gunicorn, using the `gunicorn_config.py` file.

## Publications
* El Faqir, Y., Arroyo, J., Hassan, S. (2020). An overview of Decentralized Autonomous Organizations on the blockchain. Proceedings of the 16th International Symposium on Open Collaboration (Opensym 2020) 11:1-11:8. ACM. 
    * [Freely available here](https://opensym.org/wp-content/uploads/2020/08/os20-paper-a11-el-faqir.pdf).

## Acknowledgements
This work is funded by the Spanish Ministry of Science and Innovation and the [P2P Models](https://p2pmodels.eu/) project, which is funded by the European Research Council.