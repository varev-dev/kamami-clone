FROM prestashop/prestashop:1.7.8

RUN apt-get update \
    && apt-get install -y ca-certificates \
    && update-ca-certificates \
    && a2enmod ssl \
    && rm -rf /var/lib/apt/lists/*

COPY ./sources /var/www/html

COPY ./config/ssl/certs /etc/apache2/ssl
COPY ./config/ssl/000-default.conf /etc/apache2/sites-available/000-default.conf

WORKDIR /var/www/html

CMD ["apache2-foreground"]
