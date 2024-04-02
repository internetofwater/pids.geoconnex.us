FROM yourls:1.9.2-fpm-alpine

ENV YOURLS_URL_CONVERT=62 \
    YOURLS_PRIVATE_API="false" \
    YOURLS_UNIQUE_URLS="false"

COPY --chown=www-data:www-data db.php /var/www/html/user/db.php

ADD plugins /var/www/html/user/plugins
ADD plugins/redirect-index/index.php /var/www/html

ADD ./sitemap /var/www/html/sitemap
COPY ./sitemap/_sitemap.xml /var/www/html/sitemap.xml
COPY ./favicon.ico /var/www/html/favicon.ico
