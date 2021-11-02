# Geoconnex-Yourls Permanent Identifier Service (PIDS)

### Description
This repository is responsible for CI/CD of Geoconnex PIDS. The workflow of this repository is responsible for building the Docker images of [Yourls](https://hub.docker.com/_/yourls) and [MySQL:5.7](https://hub.docker.com/_/mysql) for https://geoconnex.us. Commits to the `namespaces` folder of [geoconnex.us](https://github.com/internetofwater/geoconnex.us) are automatically commited to the `build/namespaces` folder local to this repository. The GitHub workflow for this repository generates a SQL dump and a sitemap of the `namespaces` folder. These artifacts are used in the building of the Docker images `internetofwater/yourls` and `internetofwater/yourls-mysql` as well as being committed to back to [geoconnex.us/PID-server/backup](https://github.com/internetofwater/geoconnex.us/tree/master/PID-server).

### Features of this Repository
More information can be found in the README.md of each folder. As a brief overview:
- `.github/workflows`: YAML configuration for GitHub actions.
- `build`: Files required to build python container to load namespaces into MySQL and build sitemap.
- `mysql`: Files required for Continuous Deployment of Yourls table in MySQL. Used to generate `internetofwater/yourls-mysql`.
- `yourls`: Files required for the Continuous Deployment of Yourls. Used to generate `internetofwater/yourls` (Note: Sitemap is built and located in this folder during the workflow, but is hosted in the [geoconnex.us](https://github.com/internetofwater/geoconnex.us) repository and `internetofwater/yourls` Docker image)

### Installation

1. Clone the repository to your own personal folder. <br>
   `git clone https://github.com/internetofwater/pids.geoconnex.us`<br>
   `cd pids.geoconnex.us`<br>
   `docker-compose up -d --build`
2. Open yourls admin interface and install yourls.
3. Enable all plugins before adding any entries. 

### License
This service is licensed under the [MIT License](LICENSE).
