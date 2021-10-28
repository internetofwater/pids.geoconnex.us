FROM yourls:latest

# ENV YOURLS_URL_CONVERT=62
# ENV YOURLS_PRIVATE_API="true"
# ENV YOURLS_UNIQUE_URLS="false"

ADD plugins /var/www/html/user/plugins
ADD plugins/redirect-index/index.php /var/www/html

ADD ./sitemap /var/www/html/sitemap
COPY ./sitemap/_sitemap.xml /var/www/html/sitemap.xml