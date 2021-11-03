FROM yourls:latest

COPY --chown=www-data:www-data db.php /var/www/html/user/db.php

ADD plugins /var/www/html/user/plugins
ADD plugins/redirect-index/index.php /var/www/html

ADD ./sitemap /var/www/html/sitemap
COPY ./sitemap/_sitemap.xml /var/www/html/sitemap.xml
