# Geoconnex-Yourls Permanent Identifier Service (PIDS)
[![Yourls for geoconnex.us](https://github.com/internetofwater/pids.geoconnex.us/actions/workflows/build.yml/badge.svg?)](https://github.com/internetofwater/pids.geoconnex.us/actions/workflows/build.yml)
### Description
This repository is responsible for CI/CD of Geoconnex PIDS. The workflow of this repository is responsible for building the Docker images of [Yourls](https://hub.docker.com/_/yourls) and [MySQL:5.7](https://hub.docker.com/_/mysql) for https://geoconnex.us. Commits to the `namespaces` folder of [geoconnex.us](https://github.com/internetofwater/geoconnex.us) are automatically commited to the `build/namespaces` folder local to this repository. The GitHub workflow for this repository generates a SQL dump and a sitemap of the `namespaces` folder. These artifacts are used in the building of the Docker images `internetofwater/yourls` and `internetofwater/yourls-mysql` as well as being committed to back to [geoconnex.us/PID-server/backup](https://github.com/internetofwater/geoconnex.us/tree/master/PID-server).

### Features of this Repository
More information can be found in the README.md of each folder. As a brief overview:
- [build](build/): Files required for the Continuous Deployment of Yourls and continuous deployment of Yourls table in MySQL.
- [docs](docs/): Documentation for quickstart and contributor onboarding.
- [namespaces](namespaces/): Geoconnex namespace directory tree
- [workflows](.github/workflows): YAML configuration for GitHub actions.


### Installation

1. Clone the repository to your own personal folder and run:
```
   git clone https://github.com/internetofwater/pids.geoconnex.us
   cd pids.geoconnex.us/build
   docker-compose up -d --build
```
2. Open yourls admin interface and install yourls.
3. Enable all plugins before adding any entries. 

### License
This service is licensed under the [MIT License](LICENSE).
