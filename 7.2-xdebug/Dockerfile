#
# NOTE: THIS DOCKERFILE IS GENERATED VIA "update.py"
#
# PLEASE DO NOT EDIT IT DIRECTLY.
#
ARG PHP_VERSION=7.2

FROM aheadworks/mhsendmail as mhsendmail

FROM php:${PHP_VERSION}-fpm-alpine

# FPM options
ARG FPM_USER="root"
ARG FPM_GROUP="root"

# Options
ENV COMPOSER_ALLOW_SUPERUSER=1

ARG PHP_MEMORY_LIMIT="2048M"

ARG WITH_XDEBUG="1"
ARG XDEBUG_IDEKEY="PHPSTORM"
ARG XDEBUG_REMOTE_ENABLE="on"
ARG XDEBUG_REMOTE_PORT=9001
ARG XDEBUG_REMOTE_CONNECT_BACK="1"

ENV XDEBUG_IDEKEY=${XDEBUG_IDEKEY}
ENV XDEBUG_REMOTE_ENABLE=${XDEBUG_REMOTE_ENABLE}
ENV XDEBUG_REMOTE_PORT=${XDEBUG_REMOTE_PORT}
ENV XDEBUG_REMOTE_CONNECT_BACK=${XDEBUG_REMOTE_CONNECT_BACK}
ENV XDEBUG_REMOTE_HOST="host.docker.internal"

### End of arguments/config section ###

MAINTAINER Peter Samoilov <samoilov@aheadworks.com>
ENV _TEMPORARY_REQUIREMENTS="build-base libpng-dev libmcrypt-dev curl-dev libjpeg-turbo-dev freetype-dev icu-dev libxslt-dev libzip-dev $PHPIZE_DEPS"
ENV _COMMON_REQUIREMENTS="nginx py3-click libmcrypt libpng freetype libjpeg-turbo icu-libs libxslt"

RUN apk --no-cache add ${_COMMON_REQUIREMENTS}

RUN apk --no-cache add --virtual .build-dependencies ${_TEMPORARY_REQUIREMENTS} \
    && docker-php-ext-install pdo_mysql \
    && docker-php-ext-configure gd --with-freetype-dir=/usr/include/ --with-jpeg-dir=/usr/include/ \
    && docker-php-ext-install gd \
    && docker-php-ext-install mbstring \
    && docker-php-ext-install zip \
    && docker-php-ext-install intl \
    && docker-php-ext-install xsl \
    && docker-php-ext-install soap \
    && docker-php-ext-install bcmath \
    && if [ "$WITH_XDEBUG" ] ; \
     then pecl install xdebug && docker-php-ext-enable xdebug \
        && echo "xdebug.idekey=\${XDEBUG_IDEKEY}" >> /usr/local/etc/php/conf.d/xdebug.ini \
        && echo "xdebug.remote_enable=\${XDEBUG_REMOTE_ENABLE}" >> /usr/local/etc/php/conf.d/xdebug.ini \
        && echo "xdebug.remote_port=\${XDEBUG_REMOTE_PORT}" >> /usr/local/etc/php/conf.d/xdebug.ini \
        && echo "xdebug.remote_connect_back=\${XDEBUG_REMOTE_CONNECT_BACK}" >> /usr/local/etc/php/conf.d/xdebug.ini \
        && echo "xdebug.remote_host=\${XDEBUG_REMOTE_HOST}" >> /usr/local/etc/php/conf.d/xdebug.ini; \
    fi \
    && if python3 -c "from distutils.version import StrictVersion; exit(StrictVersion('7.2') <= StrictVersion('${PHP_VERSION}'))"; then \
        docker-php-ext-install mcrypt; \
    fi \
    && apk del .build-dependencies

# replace iconv with GNU iconv
RUN apk add gnu-libiconv --update-cache --repository http://dl-cdn.alpinelinux.org/alpine/edge/community/ --allow-untrusted
ENV LD_PRELOAD /usr/lib/preloadable_libiconv.so php

# Patch php-fpm to work as custom user
RUN sed -i s/'user = www-data'/'user = ${FPM_USER}'/g /usr/local/etc/php-fpm.d/www.conf \
    && sed -i s/'group = www-data'/'group = ${FPM_GROUP}'/g /usr/local/etc/php-fpm.d/www.conf

# PHP settings
RUN echo "post_max_size=256M" >> /usr/local/etc/php/conf.d/upload-limit.ini \
    && echo "upload_max_filesize=256M" >> /usr/local/etc/php/conf.d/upload-limit.ini

RUN echo "memory_limit=${PHP_MEMORY_LIMIT}" > /usr/local/etc/php/conf.d/memory-limit.ini
RUN apk add --no-cache --virtual .curl curl \
    && curl -sS https://getcomposer.org/installer | php \
    && mv composer.phar /usr/local/bin/composer \
    && chmod +x /usr/local/bin/composer \
    && apk del .curl \
    && composer global require hirak/prestissimo

# Nginx
RUN mkdir -p /run/nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Fine tune PHP params
RUN find  /usr/local/etc/php-fpm.d/ -type f -name *.conf | xargs sed -i "s/pm.max_children = 5/pm.max_children = 50/g" \
    && find  /usr/local/etc/php-fpm.d/ -type f -name *.conf | xargs sed -i "s/pm.start_servers = 2/pm.start_servers = 10/g" \
    && find  /usr/local/etc/php-fpm.d/ -type f -name *.conf | xargs sed -i "s/pm.min_spare_servers = 1/pm.min_spare_servers = 10/g" \
    && find  /usr/local/etc/php-fpm.d/ -type f -name *.conf | xargs sed -i "s/pm.max_spare_servers = 3/pm.max_spare_servers  = 20/g"

# mhsendmail
COPY --from=mhsendmail /usr/bin/mhsendmail /usr/bin/mhsendmail
RUN echo "sendmail_path=/usr/bin/mhsendmail --smtp-addr \$MAIL_HOST:25 " > /usr/local/etc/php/conf.d/sendmail.ini

# Update host machine script
RUN echo "ip -4 route list match 0/0 | awk '{print \$3\" host.machine\"}' >> /etc/hosts" > /update-host-machine.sh && chmod +x /update-host-machine.sh

# entrypoint & cmd
ADD entrypoint.py /entrypoint.py
RUN chmod +x /entrypoint.py

EXPOSE 80

ENTRYPOINT ["/usr/bin/python3", "/entrypoint.py"]
CMD ["serve"]