# YOURLS PID service

### Description
Attempts to mimic the this [PID service](https://github.com/SISS/PID) using [YOURLS](https://yourls.org), a more actively maintained platform.
YOURLS performs much better at scale ( > 300,000 entries), and allows for the easy modification of the capacities of the service using YOURLS plugins. 

### Requires
- Docker & docker-compose.

YOURLS plugins used & activated:
- [reset-urls](https://gist.github.com/ozh/a0090f46569b50835520d95f9481d9fd#file-plugin-php) 
- [always-302](https://github.com/tinjaw/Always-302)
- [keep-querystring](https://github.com/rinogo/yourls-keep-query-string)
- [redirect-index](https://github.com/tomslominski/yourls-redirect-index)
- [regex-in-urls](https://github.com/webb-ben/plugins/tree/master/regex-in-urls)
- [request-forwarder](https://github.com/webb-ben/plugins/tree/master/request-forward)
- [bulk-import-and-shorten](https://github.com/vaughany/yourls-bulk-import-and-shorten)
- [bulk-API-import](https://github.com/webb-ben/plugins/tree/main/bulk-api-import)

### Installation

1. Clone the repository to your own personal folder. <br>
   `git clone https://github.com/webb-ben/geoconnex.us`<br>
   `cd geoconnex.us/simple-yourls`<br>
   `docker-compose up -d --build`
2. Open yourls admin interface at `http://localhost:8082/admin` and install yourls.
3. Enable all plugins before adding any entries. 
4. To populate database:
 - Look under [python](https://github.com/webb-ben/geoconnex.us/tree/master/simple-yourls/python)
 - Upload a backup of the SQL database using the adminer interface at `http://localhost:8080/`.

#### Login information
- Yourls Interface @ `http://localhost:8082/admin` => User: yourls-admin, Pass: apassword
- Adminter Interface @ `http://localhost:8080/admin` => User: root, Pass: arootpassword, Server: mysql

### License
This service is licensed under the [MIT License](LICENSE).
