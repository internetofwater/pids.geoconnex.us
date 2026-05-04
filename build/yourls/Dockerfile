FROM yourls:1.10.2

ENV YOURLS_URL_CONVERT=62 \
    YOURLS_PRIVATE_API=false \
    YOURLS_UNIQUE_URLS=false

COPY --chown=www-data:www-data db.php /var/www/html/user/db.php

ADD plugins /var/www/html/user/plugins
ADD plugins/redirect-index/index.php /var/www/html

ADD ./sitemap /var/www/html/sitemap
COPY ./sitemap/sitemap.xml /var/www/html/sitemap.xml
COPY ./sitemap.xsl /var/www/html/sitemap.xsl
COPY ./favicon.ico /var/www/html/favicon.ico
