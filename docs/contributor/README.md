# Contributor Onboarding
This document serves as a prerequisite knowledge checklist for Open Source contributors (Contributor(s)) to the Geoconnex system (System). The System is composed of multiple components which in turn leverage various Open Source software projects and their toolchains.

# Prerequisite Knowledge

The Contributor should become proficient with the following programming languages, data models, file formats, toolchains, and last but not least, the Geoconnex Components and related dependent services that comprise the System.

## Programming Languages

### [Python](https://python.org)
What the [Build Action](#build) for the Geoconnex Permanent Identifier (PID) server is written in.

### [PHP](https://www.php.net/)
What the [PID Server](#pid-server) Geoconnex components are written in.

### [Bash](https://www.gnu.org/software/bash/manual/bash.html)
Used to create various scripts in the [Geoconnex component](#geoconnex-components) toolchain

## File Formats

### XML
File format used to create Sitemap Indexes and Sitemaps Files crawled by Google and [Glean

### CSV
File format used to create mappings from Geoconnex IRIs to their corresponding location on the web.

### [Dockerfile](https://docs.docker.com/engine/reference/builder/) 
File format used to build Docker images. Specifies how to package all [Geoconnex components](#geoconnex-components).

### [Sitemap](https://www.sitemaps.org/protocol.html)
An xml document that contains URLs of a Publisher's http endopoints for which JSON-LD documents can be extracted and aggregated.

### [Sitemap Index](https://www.sitemaps.org/protocol.html#index)
An xml document that contains URLs of Publisher specific [sitemaps](#Sitemap), 

## Tool(chain)s

[Geoconnex components](#geoconnex-components) are invariably deployed and orchestrated as Docker containers at runtime. 

### [docker](https://docs.docker.com/engine/reference/commandline/cli/) 
### [docker compose](https://docs.docker.com/compose/)
*See Also* [Yaml](#yaml), 
### [make](https://www.gnu.org/software/make/manual/make.html) 
*See Also* [Makefile](#makefile)

## Software Frameworks

[Yourls](https://yourls.org/) is an open source URL shorter which the [PID Server](#pid-server) is built upon and deployed by [Aggregators](https://github.com/internetofwater/harvest.geoconnex.us/blob/main/README.md#persona-aggregator). The data pipeline created by the System which connects [Publishers](https://github.com/internetofwater/harvest.geoconnex.us/blob/main/README.md#persona-publisher) to [Aggregators](https://github.com/internetofwater/harvest.geoconnex.us/blob/main/README.md#persona-aggregator) is performed here.


## System Components 

### Geoconnex Components

#### [PID Server](https://github.com/internetofwater/pids.geoconnex.us) 

Pemanent Identifier (PID) Server is used to provide re-directs to Geoconnex webpages and provides a Sitemap index of HTML pages that [Gleaner](https://github.com/gleanerio/gleaner) ingests to geoconnex. It is implemented using cloud native services, leveraging GCP's Cloud Run and Cloud SQL.

### Dependent (Cloud) Services 

See Also [Reference Services](README.md#reference-services)

#### Cloud Run

Used by [YOURLS](https://yourls.org/) to serve redirects to all [Publishers](https://github.com/internetofwater/harvest.geoconnex.us/blob/main/README.md#persona-publisher). The current reference implementation used by [pids.geoconnex.us](https://pids.geoconnex.us) is YOURLS on Cloud Run to scale the number of instances as requests are recieved from [Users](https://github.com/internetofwater/harvest.geoconnex.us/blob/main/README.md#persona-user).

#### Cloud MySQL Database

Used by [YOURLS](https://yourls.org/) to host all 1:1 and Regex URL mappings of all data from [Publishers](README.md#persona-publisher) in geoconnex. The structure of this table is prescribed by YOURLS.
