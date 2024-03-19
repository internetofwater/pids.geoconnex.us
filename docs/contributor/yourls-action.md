# YOURLS Actions Quickstart

This document serves to familiarize the *Contributor* with YOURLS Action by showing how to build and run it from source in a local build environment (*Environment*). This software populates the YOURLS database from a directory tree of CSV mapping files. This is used to load the [Namespaces](/namespaces/) directory to a Yourls compliant, MySQL database.

# Prerequisites

In order to build YOURLS Action you must have the following installed in your *Environment*. 

## Python and Pip
Python and Pip can be downloaded and installed from the official [Python website](https://p.ython.org/). Ensure you select the appropriate version for your operating system.

As of the last update, the YOURLS Action requires Python 3.6 or later. Check the system's documentation or codebase for the specific version requirements.

This documentation may refer to the ``PYTHONPATH`` environment variable, which indicates the directories where Python looks for modules. If not set, Python will use a default path.

Please refer to the Python official documentation for comprehensive information on Python installation, configuration, and development practices.

```bash
python3 --version
pip3 --version
```

## Git

### Installation
Git can be downloaded and installed from the official [Git website](https://git-scm.com/). Follow the installation instructions for your specific operating system.

### Version Check
To check the installed Git version, use the following command:

```bash
git --version
```

## Docker
Docker is used here to launch YOURLS developer runtime service dependencies YOURLS and its database (MySQL). 

### Installation
Docker can be downloaded and installed from the official Docker website. Follow the installation instructions for your specific operating system.

### Validation
Once Docker is installed, you can verify that it's running correctly by executing the following command:

```bash
docker --version
docker info
```

Note: To run docker on alpine, you must have sudo privileges.

# Building YOURLS Action

Choose a starting location to work on your computer:

```bash
export SRC_BASE_DIR=/path/to/dev/directory
```

## Clone
Clone [Yourls Action](https://github.com/cgs-earth/yourls-action.git) from your forked github repository to your *Environment* in a predefined directory location.

```bash
cd $SRC_BASE_DIR
git clone git@github.com:<GH_USER>/yourls-action.git
```

## Runtime Dependencies

### Set up YOURLS environment:
To build the YOURLS database environment, build the MySQL docker image.

```bash
cd $SRC_BASE_DIR/yourls-action/yourls-mysql
docker build -t yourls-mysql .
```

Start the MySQL database:
```bash
docker run -d \
   -p 3306:3306 \
   --name mysql \
   -e "MYSQL_ROOT_PASSWORD=amazingpassword" \
   yourls-mysql
```

### Create a namespace

Create a namespace directory tree, and a CSV mapping file [links.csv](/docs/assets/yourls-action/links.csv).

```bash
mkdir -p $SRC_BASE_DIR/namespaces/iow
vi $SRC_BASE_DIR/namespaces/iow/links.csv
```

### Set up YOURLS Action

Next install the python package YOURLS Action, which loads the directory tree into the MySQL database.

```bash
cd $SRC_BASE_DIR/yourls-action/yourls-action
# if user has sudo privileges
python3 setup.py install
# else
pip3 install .
```

Note: Ensure the location you install yourls-action is on your `$PATH`, otherwise you
won't be able to use the yourls-action command line interface (CLI).

YOURLS Action uses environment variables to connect to the MySQL database:
```bash
export DB_SOCKET_DIR=/var
export YOURLS_DB_HOST=localhost
export YOURLS_DB_PASSWORD=amazingpassword
```

# Running YOURLS Action

To run YOURLS Action, use the CLI:

```bash
yourls-action run $SRC_BASE_DIR/namespaces
```

## Verifying YOURLS Action Output

To verify YOURLS action has inserted the URL mappings run the following...

```bash
docker exec -it mysql \
   sh -c 'mysql -p -h localhost -e \
   "USE yourls; SELECT * FROM yourls_url;"'
```

Note: You will need to provide the MySQL password set above.

The table should appear as follows, with a timestamp of when the row was last updated:

| keyword                                      | url                                               | title                      | timestamp           | ip      | clicks |
|----------------------------------------------|---------------------------------------------------|----------------------------|---------------------|---------|--------|
| /usgs/monitoring-location/([a-zA-Z0-9_]+).*$ | https://waterdata.usgs.gov/monitoring-location/$1 | USGS Monitoring Locations | 2024-03-12 18:09:54 | 0.0.0.0 |      0 |
| iow/homepage                                 | https://internetofwater.org                       | Internet Of Water homepage | 2024-03-12 18:09:54 | 0.0.0.0 |      0 |
