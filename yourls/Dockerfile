FROM yourls:latest

COPY ./sitemap/_sitemap.xml /usr/source/yourls/sitemap.xml
COPY ./sitemap /usr/source/yourls/sitemap
COPY ./class-mysql.php /usr/source/yourls/class-mysql.php

COPY plugins /var/www/html/user/plugins
COPY plugins/redirect-index/index.php /var/www/html/index.php
