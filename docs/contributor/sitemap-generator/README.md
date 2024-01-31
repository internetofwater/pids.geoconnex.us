# Sitemap Generator Quickstart

This document serves to familiarize the *Contributor* with Sitemap Generator by showing how to build and run it from source in a local build environment (*Environment*). This software builds the [Geoconnex Sitemap](https://geoconnex.us/iow/sitemap). This is used to load the [Namespaces](/namespaces/) directory to a crawlable index of all geoconnex.us based IRIs.

# Prerequisites

In order to build Sitemap Generator you must have the following installed in your *Environment*. 

## Python
Python can be downloaded and installed from the official [Python website](https://python.org/). Ensure you select the appropriate version for your operating system.

As of the last update, the Sitemap Generator requires Python 3.6 or later. Check the system's documentation or codebase for the specific version requirements.

This documentation may refer to the ``PYTHONPATH`` environment variable, which indicates the directories where Python looks for modules. If not set, Python will use a default path.

Please refer to the Python official documentation for comprehensive information on Python installation, configuration, and development practices.

```bash
python3 --version
pip3 --version
```

# Building Sitemap Generator

Choose a starting location to work on your computer:

```bash
export SRC_BASE_DIR=/path/to/dev/directory
```

## Clone
Clone from the CGS GitHub repository to your *Environment* in a predefined directory location.

```bash
mkdir $SRC_BSAE_DIR
cd $SRC_BASE_DIR
git clone https://github.com/cgs-earth/sitemap-generator.git
```

## Runtime Dependencies

### Set up Sitemap Generator environment:

First install the python package Sitemap Generator, which loads the filesystem into the a sitemap index hierarchy.

```bash
cd $SRC_BASE_DIR/sitemap-generator
python3 setup.py install
```

Note: Ensure the location you install sitemap-generator is on your `$PATH`, otherwise you
won't be able to use the sitmap-generator CLI.

### Set up Namespace filesystem:
This example includes both 1:1 CSV mapping files and Regex CSV mappings with their pre-generated sitemap.
Create a namespace filesystem, and a CSV mapping file [links.csv](links.csv) and [regex-pids__0.xml](regex-pids__0.xml).

```bash
mkdir -p $SRC_BASE_DIR/namespaces/iow
vi $SRC_BASE_DIR/namespaces/iow/links.csv
# Repeat for Regex-XML if desired, Regex CSV files are ignored.
mkdir -p $SRC_BASE_DIR/namespaces/ref
vi $SRC_BASE_DIR/namespaces/ref/regex-pids__0.xml
```

The structure of this filesystem will be re-used in the structure of the sitemap index filesystem.

### Set up reference namespace:
Sitemap Generator uses git to track when files change, This is inserted as the `<lastmod>` tag inside the sitemap.
As such we need to download our reference namespace:

```bash
cd $SRC_BASE_DIR
git clone https://github.com/internetofwater/geoconnex.us.git
```

### Set environment variables

Sitemap Generator uses environment variables:

```bash
export SOURCE_REPO=$SRC_BASE_DIR/geoconnex.us
export SITEMAP_DIR=$SRC_BASE_DIR/sitemap
```

# Running Sitemap Generator

To run Sitemap Generator, use the CLI:

```bash
sitemap-generator run $SRC_BASE_DIR/namespaces
```

## Verifying Sitemap Generator Output

To verify Sitemap Generator has indexed the sitemaps run the following...

```bash
ls $SITEMAP_DIR/**
```

Note: Sitemap generator uses the full path when generating the sitemap index file.
The geoconnex sitemap runs with namespaces at the root of the filesystem:

```bash
export SITEMAP_DIR=/sitemap
cp $SRC_BASE_DIR/geoconnex.us/namespaces/* /namespaces
sitemap-generator run /namespaces
```

Which will better reflect the live sitemap index file.

```bash
ls /sitemap/**
cat /sitemap/_sitemap.xml
```
