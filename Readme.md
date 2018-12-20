# docker-phpdev

Base image for php development. 

**Development purposes only**

This image doing a lot of "wrong" things useful at dev stage, however it is extremely dangerous at production(e.g. runs php-fpm as root)

## What's inside

* PHP-fpm
* nginx
* crontab
* composer
* mhsendmail
* python

#### PHP extensions
* bcmath
* gd
* intl
* mbstring
* pdo_mysql
* soap
* xsl
* xdebug [optional]
* zip

## Building 

Specific PHP version

```bash
docker build -t aheadworks/phpdev:7.2 --build-arg PHP_VERSION=7.2 .
```

With XDebug support

```bash
docker build -t aheadworks/phpdev:7.1-xdebug --build-arg PHP_VERSION=7.1-xdebug --build=arg WITH_XDEBUG=1 .
```

#### Accessible build arguments

```
FPM_USER="root"
FPM_GROUP="root"

PHP_MEMORY_LIMIT=2048M

XDEBUG_IDEKEY="PHPSTORM"
XDEBUG_REMOTE_ENABLE="on"
XDEBUG_REMOTE_PORT=9001
XDEBUG_REMOTE_CONNECT_BACK="on"
```

## Usage
When run without commands starts nginx listening at port 80, fpm at port 9000, etc.

```bash
docker run -p80:80 aheadworks/phpdev:7.2 
Starting crond...
Starting nginx & fpm...
[20-Dec-2018 08:44:20] NOTICE: fpm is running, pid 10
[20-Dec-2018 08:44:20] NOTICE: ready to handle connections
```

When run with `docker run` passes params directly to shell

```bash
docker run aheadworks/phpdev:7.2 uname -a
Linux b89a1a21b62d 4.9.125-linuxkit #1 SMP Fri Sep 7 08:20:28 UTC 2018 x86_64 Linux
```
