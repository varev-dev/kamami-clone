FROM prestashop/prestashop:1.7.8

RUN apt-get update \
    && apt-get install -y ca-certificates \
    && update-ca-certificates \
    && a2enmod ssl \
    && rm -rf /var/lib/apt/lists/*

COPY --chown=www-data:www-data ./sources /var/www/html
RUN rm -rf /var/www/html/install

COPY --chown=www-data:www-data ./config/ssl/certs /etc/apache2/ssl
COPY --chown=www-data:www-data ./config/ssl/000-default.conf /etc/apache2/sites-available/000-default.conf

COPY ./entrypoint.sh /entrypoint.sh
RUN chmod u+x /entrypoint.sh

WORKDIR /var/www/html

USER www-data

ENTRYPOINT ["/entrypoint.sh"]