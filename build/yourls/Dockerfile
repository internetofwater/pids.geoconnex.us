FROM yourls:latest

ENV YOURLS_URL_CONVERT=62 \
    YOURLS_PRIVATE_API="true" \
    YOURLS_UNIQUE_URLS="false"

COPY --chown=www-data:www-data db.php /var/www/html/user/db.php

ADD plugins /var/www/html/user/plugins
ADD plugins/redirect-index/index.php /var/www/html

ADD sitemap.zip /sitemap.zip
RUN apt-get update -y && apt-get install -y unzip \
    # unzip sitemap
    && unzip /sitemap.zip -d /var/www/html/sitemap \
    && ls -R /var/www/html/sitemap \
    && mv /var/www/html/sitemap/_sitemap.xml /var/www/html/sitemap.xml \
    # cleanup
    && apt autoremove -y  \
    && apt-get -q clean \
    && rm -rf /var/lib/apt/lists/*
