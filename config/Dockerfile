FROM prestashop/prestashop:1.7.8

RUN apt-get update \
    && apt-get install -y ca-certificates \
    && update-ca-certificates \
    && a2enmod ssl \
    && rm -rf /var/lib/apt/lists/*
