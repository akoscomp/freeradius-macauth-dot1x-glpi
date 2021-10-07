FROM phpdockerio/php80-fpm:latest
#WORKDIR "/application"

# Fix debconf warnings upon build
ARG DEBIAN_FRONTEND=noninteractive

# Install selected extensions and other stuff
RUN apt-get update \
    && apt-get -y --no-install-recommends install  php8.0-memcached php8.0-mysql php8.0-bz2 php8.0-gd php8.0-imagick php8.0-imap php8.0-intl php8.0-ldap php8.0-xmlrpc php-cas\
    && apt-get clean; rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* /usr/share/doc/*

