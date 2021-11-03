# Build
This is `pids-geoconnex-build`, used to populate the yourls tables (for the `internetofwater/yourls-mysql:latest` docker image), and to build the sitemap (for the `internetofwater/yourls:latest` docker image).

This container is run during the Github workflow.

### Description
The build folder is intended to run after the creation of a MySQL server with a valid yourls database. `yourls_api.py` connects to either the yourls instance or the MySQL server directly and populates the `yourls_url` table from the namespaces folder. During this process a sitemap is generated for each CSV file in namespaces (Note: a CSV file with a regex entry will not generate a sitemap from the CSV).

- `namespaces` is a copy of the namespaces folder of [geoconnex.us](https://github.com/internetofwater/geoconnex.us/namespaces).
- `yourls_api.py` and `yourls_client.py` are modified versions of [pyourls](https://pypi.org/project/yourls/).
- `sitemap-schema.xml` and `sitemap-url.xml` are templates used to generate the geoconnex sitemap.
- `requirements.txt` is used by the `Dockerfile` to install the necessary python packages.

### Usage
This container cannot run in isolation and has to be able to connect to either MySQL or Yourls. This can be done by running both containers inside of docker compose (uncomment the python build image), or on the same network as one. The workflow creates the MySQL inside of docker compose but runs the build image using docker run on the `yourls_host` network.

The basic command is to build this container is:
`docker build -t build_yourls_uploader .`

The command to run that container is:
```
docker run --rm --network=pids_yourls_host --name build_yourls \
    --env YOURLS_DB_PASSWORD=${YOURLS_DB_PASSWORD:-arootpassword} --env YOURLS_DB_USER=${YOURLS_DB_USER:-root} \
    -v /sitemap:/sitemap build_yourls_uploader \
    python yourls_client.py --options <path/to/csv>
```
with the following options

`-s <url>` The stem of the persistent identifiers. In our case, usually `https://geoconnex.us/`

`-a <url>` The url of the PID server management layer. In our case, `https://pids.geoconnex.us`

`-u` The username (same as before)

`-p` The password (same as before)

`<path/to/csv>` can be a local directory with many CSV files, the path of a single CSV file, or the URL of a hosted CSV file.
