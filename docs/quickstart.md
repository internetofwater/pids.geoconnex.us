# Quickstart

## About

This document provides a quick set up for an up-to-date version of the Permanent Identifier Service. For a quickstart on YOURLS, see https://yourls.org/docs/guide/install. For a quickstart as a contributor, see [Contributor](./contributor/) for the set up of a development environment.

## Install and Run

```bash
git clone https://github.com/internetofwater/pids.geoconnex.us
cd build
```

Unzip the sitemap:
```bash
unzip yourls/sitemap.zip yourls/sitemap
```

If running on localhost:
```bash
docker compose up
```

else, adjust environment variables in [docker-compose.yml](../build/docker-compose.yml),
then run:
```bash
vi docker-compose.yml
docker compose up
```

The PID server will be running on port 8080.
