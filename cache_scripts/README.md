# DAO-Analyzer's cache-scripts

## Set-up & Running

The easiest method by far to download and run the application is to use pip to install it

```
pip install dao-analyzer
```

Then, you can use this script using the command `daoa-cache-scripts`

### Download
Enter in your terminal (git must be installed) and write down:

```
git clone https://github.com/Grasia/dao-analyzer
```

After that, move to repository root directory with:

```
cd dao-analyzer
```

### Installation
All code has been tested on Linux, but it should work on Windows and macOS, 'cause it just uses the python environment.

So, you must install the following dependencies to run the tool:

* python3 (3.10 or later)
* python3-pip

Now, install the Python dependencies:

`pip3 install -r requirements.txt`

If you don't want to share Python dependencies among other projects, you should use a virtual environment, such as [virtualenv](https://docs.python-guide.org/dev/virtualenvs/).

### How to run it?
If you want all the data used in the app, you can just use:

```
python3 -m cache_scripts
```

this will create a folder called `datawarehouse` with a lot of files in apache's arrow format.

You can import those files to `pandas` with `read_feather`. For example:

```python
pd.read_feather('datawarehouse/aragon/apps.arr')
```

## Usage guide
If you don't want all the data (and it can take a lot of time), you have a lot of options available to select whichever data you want. The full `--help` output is

```
usage: daoa-cache-scripts [-h] [-V] [-p [{aragon,daohaus,daostack} ...]]
                          [--ignore-errors | --no-ignore-errors] [-d] [-f] [-F] [--skip-daohaus-names]
                          [-n {mainnet,_theGraph,arbitrum,xdai,polygon} [{mainnet,_theGraph,arbitrum,xdai,polygon} ...]]
                          [-c COLLECTORS [COLLECTORS ...]] [--block-datetime BLOCK_DATETIME]
                          [-D DATAWAREHOUSE] [--cc-api-key CC_API_KEY]

Main script to populate dao-analyzer cache

options:
  -h, --help            show this help message and exit
  -V, --version         Displays the version and exits
  -p [{aragon,daohaus,daostack} ...], --platforms [{aragon,daohaus,daostack} ...]
                        The platforms to update. Every platform is updated by default.
  --ignore-errors, --no-ignore-errors
                        Whether to ignore errors and continue (default: True)
  -d, --debug           Shows debug info
  -f, --force           Removes the cache before updating
  -F, --delete-force    Removes the datawarehouse folder before doing anything
  --skip-daohaus-names  Skips the step of getting Daohaus Moloch's names, which takes some time
  -n {mainnet,_theGraph,arbitrum,xdai,polygon} [{mainnet,_theGraph,arbitrum,xdai,polygon} ...], --networks {mainnet,_theGraph,arbitrum,xdai,polygon} [{mainnet,_theGraph,arbitrum,xdai,polygon} ...]
                        Networks to update. Every network is updated by default
  -c COLLECTORS [COLLECTORS ...], --collectors COLLECTORS [COLLECTORS ...]
                        Collectors to run. For example: aragon/casts
  --block-datetime BLOCK_DATETIME
                        Get data up to a block datetime (input in ISO format)
  -D DATAWAREHOUSE, --datawarehouse DATAWAREHOUSE
                        Specifies the destination folder of the datawarehouse
  --cc-api-key CC_API_KEY
                        Set the CryptoCompare API key (overrides environment variable)
```

### Getting only data from a platform
You can select the platform to download data about with the `--platform` selector. Let's download only data for daostack and aragon:

```
daoa-cache-scripts --platforms daostack aragon
```

### Getting only data from a network
You can select the chain to get data from with the `--networks` switch. For example, to get data only for xdai network, you can do:

```
daoa-cache-scripts --networks xdai
```