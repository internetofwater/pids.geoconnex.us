FROM yourls:latest

COPY ./sitemap/_sitemap.xml /var/www/html/sitemap.xml
COPY ./sitemap /var/www/html/sitemap
RUN ["mkdir", "/var/www/html/includes"]
COPY ./class-mysql.php /var/www/html/includes/class-mysql.php
COPY ./class-mysql.php /var/www/html/includes/_class-mysql.php

COPY plugins /var/www/html/user/plugins
COPY plugins/redirect-index/index.php /var/www/html/index.php
