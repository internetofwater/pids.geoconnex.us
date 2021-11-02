# MySQL
This is `pids-geoconnex-mysql`, used as the host directory for the `internetofwater/yourls-mysql` docker image. 

This container is run during the Github workflow. 

### Description
The mysql folder is used to build `mysql` and `internetofwater/yourls-mysql` images during the Github workflow. Initially `mysql` is created using `schema.sql.gz`. At the end of the workflow `internetofwater/yourls-mysql` is created using `yourls.sql.gz`.

`schema.sql.gz` is an empty backup of the yourls database with an empty `yourls_url` table and the specified `yourls_options` plugins enabled. `internetofwater/yourls-mysql` includes both `/docker-entrypoint-initdb.d/schema.sql.gz` and the workflow generated backup `/docker-entrypoint-initdb.d/yourls.sql.gz`. `schema.sql.gz` is redundant when `yourls.sql.gz` is included,because `schema.sql.gz` is executed before `yourls.sql.gz`. Each backup drops and rebuilds all the tables in the `yourls` database.

### Usage
The `Dockerfile` moves all files from this directory (`.`) to `/docker-entrypoint-initdb.d/`. Therefore:
- With just `schema.sql.gz`: Build container with empty yourls database for MySQL with plugins enabled.
- With [yourls.sql.gz](https://github.com/internetofwater/geoconnex.us/tree/master/PID-server/backup): Build container with yourls database populated with the most recent database backup.
