# YOURLS PID service

### Description
Attempts to mimic the this [PID service](https://github.com/SISS/PID) using [YOURLS](https://yourls.org), a more actively maintained platform.
YOURLS performs much better at scale ( > 300,000 entries), and allows for the easy modification of the capacities of the service using YOURLS plugins. 

### Requires
- Docker & docker-compose.
- Python based API to populate database from XML. Faster ways to add data, and more data types need to be added at some point.

YOURLS plugins used & activated:
- [reset-urls](https://gist.github.com/ozh/a0090f46569b50835520d95f9481d9fd#file-plugin-php) 
- [always-302](https://github.com/tinjaw/Always-302)
- [keep-querystring](https://github.com/rinogo/yourls-keep-query-string)
- [redirect-index](https://github.com/tomslominski/yourls-redirect-index)
- [regex-in-urls](https://github.com/webb-ben/geoconnex.us/tree/master/simple-yourls/yourls/plugins/regex-in-urls)
- [request-forward](https://github.com/webb-ben/geoconnex.us/tree/master/simple-yourls/yourls/plugins/request-forward)

### Installation

1. Clone the repository to your own personal folder. <br>
   `git clone https://github.com/webb-ben/geoconnex.us`<br>
   `cd geoconnex.us/simple-yourls`<br>
   `docker-compose up -d --build`
2. Open yourls admin interface at `http://localhost:8082/admin` and install yourls.
3. Enable all plugins before adding any entries. 
4. To populate database:
 - Run `populate_db.py` which reads from the XML files at `../BACKUP/backup_current/`. 
   Requires pyourls3 installed in your python environment.
   Removes the first '/' from each short URL for YOURLS compatibility.
   Can use the flags -s -r to control the order in which the database is populated. 
   <br><br>or<br><br>
 - Upload a backup of the SQL database using the adminer interface at `http://localhost:8080/`.

#### Login information
- Yourls Interface @ `http://localhost:8082/admin` => User: yourls-admin, Pass: apassword
- Adminter Interface @ `http://localhost:8080/admin` => User: root, Pass: arootpassword, Server: mysql

### License
This service is licensed under the [MIT License](LICENSE).
