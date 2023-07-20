# Yourls
This is `pids-geoconnex-yourls`, used as the host directory for the `internetofwater/yourls` docker image. 

This container is not used during the Github workflow.

### Description
The yourls folder is used to build `internetofwater/yourls` image during the Github workflow. The purpose of this `Dockerfile` is to move the necessary files to `/var/www/html`. For that reason, as is, this container is not buildable. For the `Dockerfile` to properly create a container, either remove the sitemap lines from the `Dockerfile`, or download and unzip the sitemap from [here](https://github.com/internetofwater/geoconnex.us/tree/master/PID-server/backup).

Yourls allows for plugins that can modify the behavior of Yourls without modifying core code. These Yourls plugins are moved into the user's folder of plugins.
- [404-if-not-found](https://github.com/YOURLS/404-if-not-found/)
- [always-302](https://github.com/tinjaw/Always-302) (modified to 303)
- [bulk-import-and-shorten](https://github.com/vaughany/yourls-bulk-import-and-shorten)
- change-title
- [keep-querystring](https://github.com/rinogo/yourls-keep-query-string)
- [reset-urls](https://gist.github.com/ozh/a0090f46569b50835520d95f9481d9fd#file-plugin-php) 
- [redirect-index](https://github.com/tomslominski/yourls-redirect-index)
- [request-forwarder](https://github.com/webb-ben/plugins/tree/master/request-forward)
- [sleeky-backend](https://sleeky.flynntes.com)
- [bulk-api-import](https://github.com/webb-ben/plugins/tree/main/bulk-api-import)
- [regex-in-urls](https://github.com/webb-ben/plugins/tree/master/regex-in-urls)

In order to run serverless on Google Cloud Platform, Yourls requires an alternative driver for MySQL, `db.php`. Informed by this [issue](https://github.com/YOURLS/YOURLS/issues/3101) and this [GCP guide](https://cloud.google.com/sql/docs/mysql/connect-run#php).

### Usage
The `Dockerfile` moves various Yourls related files to `/var/www/html`.
- This docker image is intended to connect to a preconfigured database with enabled plugins. For that reason, at a bare minimum, `plugins` must be copied to `/var/www/html/user/plugins` & `plugins/redirect-index/index.php` must be copied to `/var/www/html/index.php`.
- To easily host the sitemap under the same domain name as Yourls, the sitemap folder is moved to `/var/www/html/sitemap`. The sitemap file structure is the same as the namespaces file structure. Additionally the sitemap index, `sitemap/_sitemap.xml`, is moved and renamed to `/var/www/html/sitemap.xml`.
- `db.php` disables the `db_connect_custom_dsn` yourls hook and forces socket connections with a default `DB_SOCKET_DIR=/cloudsql`. If using a different host remove this line or try using socket connections instead!
