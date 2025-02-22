# Quickstart

## About

This document provides a quick set up for an up-to-date version of the Permanent Identifier Service. For a quickstart on YOURLS, see https://yourls.org/docs/guide/install. 
For a quickstart as a contributor, see [Contributor](./contributor/) for the set up of a development environment.


## Install and Run

```bash
git clone https://github.com/internetofwater/pids.geoconnex.us
cd pids.geoconnex.us/build
```

Unzip the sitemap:
```bash
unzip yourls/sitemap.zip -d yourls/sitemap
```

### Localhost Instructions

If running on localhost:
```bash
docker compose up
```
The service will be listening on http://localhost:8080.
To access the admin page, visit http://localhost:8080/admin.

### Custom Host Instructions

If running on a different host, adjust environment variables 
in [docker-compose.yml](../build/docker-compose.yml) before running
```bash
vi docker-compose.yml
docker compose up
```

If running on a different host, the service will be listening at ``YOURLS_SITE`` in [docker-compose.yml](/build/docker-compose.yml).
To access the admin page, visit ``YOURLS_SITE/admin``. Credentials for the YOURLS web-based admin interface is set with environment variables in [docker-compose.yml](/build/docker-compose.yml).
