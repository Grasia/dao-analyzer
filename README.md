# DAO-Analyzer
It is a tool to visualize DAO metrics. Currently, it shows DAO from [DAOstack](https://daostack.io/), [DAOhaus](https://daohaus.club/), and [Aragon](https://aragon.org/). Web site: [http://dao-analyzer.science/](http://dao-analyzer.science/)

## Set-up & Running (Download app)
You can either install it on your local machine, or if you prefer it, you can use the official docker image.

> If you only want to retrieve the data used by our application, you can follow [this guide](./cache_scripts/README.md) instead

The easiest method by far to download and run the application is to use pip to install it

```
pip install dao-analyzer
```

Then, you can run the app using the commands `daoa-cache-scripts` and `daoa-server`

### How to run it?
Before launching the app, you have to run the following script in order to enable the cache stored in `datawarehouse`:

```
daoa-cache-scripts
```

After a few minutes, you can now run the app with:

```
daoa-server
```

Now, visit `http://127.0.0.1:8050` or the address given in the program output with your web browser.

### Environment variables
To be able to access all the features of dao-analyzer, you can specify the following
environment variables:

```
# The CrytptoCompare API key to be used to get token prices
DAOA_CC_API_KEY = "your_api_key"

# The path of the datawarehouse
DAOA_DW_PATH = './datawarehouse' # <-- Default value
```

## Build application
Enter in your terminal (git must be installed) and write down:

`git clone https://github.com/Grasia/dao-analyzer`

After that, move to repository root directory with:

```
cd dao-analyzer
```

Build the `dao_analyzer_components` (not necessary if you only want to get the data, but not to display it)

```
cd dao_analyzer_components && npm ci && npm build
```

Then, go back to the root folder of the project, and install the package

```
pip install -e .
```

If you don't want to share Python dependencies among other projects, you should use a virtual environment, such as [virtualenv](https://docs.python-guide.org/dev/virtualenvs/).

## Using Docker <a name="docker"></a>
If you use Docker, you can just use the images at [grasia/dao-analyzer](https://hub.docker.com/r/grasia/dao-analyzer). The tags with the `-cached` suffix have a pre-populated data warehouse (this means the image uses more space, but takes less time to load). To use it, just run the command:

```
docker run --name dao-analyzer -it -p80:80 grasia/dao-analyzer:latest
```

or

```
docker run --name dao-analyzer -it -p80:80 grasia/dao-analyzer:latest-cached
```

> `dao-analyzer` is the container name, you can put whatever you want, but remember
> to change it also on the following command

Now, you can update the datawarehouse using:

```
docker exec -it dao-analyzer python -m cache_scripts
```

You can even add it to your system as a cron job to update it daily, weekly, etc...

## Technical details

### Architecture
There is available a class diagram of the [DAOstack app](https://github.com/Grasia/dao-analyzer/blob/master/dao_analyzer/apps/daostack/class_diagram.png), the [DAOhaus app](https://github.com/Grasia/dao-analyzer/blob/master/dao_analyzer/apps/daohaus/class_diagram.png), and the [Aragon app](https://github.com/Grasia/dao-analyzer/blob/master/dao_analyzer/apps/aragon/class_diagram.png).

### Debugging

This app uses `flask`, so you can use the `FLASK_ENV` variable, which also enables debug mode (among other things) when set to `development`.

```
export FLASK_ENV=development
```

### How to test it?
Run all tests with:

`tox`

or

`python3 -m pytest test/`

#### Flags for hypothesis testing
Use this flag `--hypothesis-show-statistics` to show statistics.

Use the flag `--hypothesis-seed=<int>` to set a fixed seed, it's useful to reproduce a failure.



## Deploy
In order to fully deploy the app, use the `deploy.sh` script, which installs all the Python dependencies, updates the datawarehouse, and runs the web-app with gunicorn, using the `gunicorn_config.py` file.

### Matomo integration
To enable Matomo integration, you just have to pass the following environment variables like this:
```bash
DAOA_MATOMO_URL = "https://matomo.example.com"
DAOA_MATOMO_SITE_ID = 1
```

You can check if the integration is working visiting the page and then your dashboard. The integration uses Javascript, so if there are any errors, you should be able to see them using "Inspect view" in your browser.

## Publications

* Javier Arroyo, David Davó, Elena Martínez-Vicente, Youssef Faqir-Rhazoui, and Samer Hassan (2022). "DAO-Analyzer: Exploring Activity and Participation in Blockchain Organizations.". Companion Publication of the 2022 Conference on Computer Supported Cooperative Work and Social Computing (CSCW'22 Companion). ACM, 193–196.
    * [Freely available here](https://doi.org/10.1145/3500868.3559707)

* Youssef Faqir-Rhazoui, Javier Arroyo and Samer Hassan (2021). "A comparative analysis of the platforms for decentralized autonomous organizations in the Ethereum blockchain." Journal of Internet Services and Applications volume 12, Article number: 9.
    * [Freely available here](https://jisajournal.springeropen.com/articles/10.1186/s13174-021-00139-6).

* Youssef Faqir-Rhazoui, Miller Janny Ariza-Garzón, Javier Arroyo and Samer Hassan (2021). "Effect of the Gas Price Surges on User Activity in the DAOs of the Ethereum Blockchain." Extended Abstracts of the 2021 CHI Conference on Human Factors in Computing Systems, Article No.: 407, Pages 1–7.
    * [Freely available here](https://dl.acm.org/doi/pdf/10.1145/3411763.3451755?casa_token=cU40LWnMO0EAAAAA:608tLS07Ya0KuhrBXihSSCRqMV72jDOu0XfP3jXnH64z4c2glcY43w69feOikee4t2oxoQ4doxAFjg).

* Youssef Faqir-Rhazoui, Javier Arroyo, and Samer Hassan (2021). "A Scalable Voting System: Validation of Holographic Consensus in DAOstack." Proceedings of the 54th Hawaii International Conference on System Sciences, 5557-5566.
    * [Freely available here](https://scholarspace.manoa.hawaii.edu/bitstream/10125/71296/0543.pdf).

* Youssef Faqir-Rhazoui, Javier Arroyo, and Samer Hassan. (2020). An overview of Decentralized Autonomous Organizations on the blockchain. Proceedings of the 16th International Symposium on Open Collaboration (Opensym 2020) 11:1-11:8. ACM. 
    * [Freely available here](https://opensym.org/wp-content/uploads/2020/08/os20-paper-a11-el-faqir.pdf).

## Acknowledgements
This work is funded by the Spanish Ministry of Science and Innovation and the [P2P Models](https://p2pmodels.eu/) project, which is funded by the European Research Council.
