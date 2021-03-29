FROM debian:latest

ENV USER=dq
ENV UID=<UID>
ENV GNAME=dq
ENV GID=<GID>
ENV HOME=/home/dq

ENV PATH=${PATH}:/home/dq/sh:/home/dq/.local/bin:${HOME}/bin:${HOME}/sh:/vol/tools/shed
ENV PHP_CONF=/etc/php/7.3/fpm/pool.d/www.conf
ENV WORDPRESS_PATH=/home/dq/wp

RUN apt update -y && apt install -y \
    curl \
    git \
    netcat \
    php7.3 \
    php7.3-cli \
    php7.3-fpm \
    php7.3-mysql \
    php-pear \
    python3 \
    python3-dev \
    python3-pip \
    python3-psycopg2 \
    net-tools \
    procps \
    vim \
    libxml2-dev \
    libxslt-dev \
    zlib1g-dev \
    libssl-dev \
    postgresql-client

RUN pear install http_request2

COPY ./rootfs /
RUN chmod -R 777 /tmp
RUN find /tmp -type f -executable -regex ".*\/custom_scripts\/build.*" \
    | sort | xargs -i /bin/bash {}

RUN mkdir -p /run/php \
 && sed -i "s|.*listen =.*|listen = /run/php/php.sock|g" "${PHP_CONF}"

RUN pip3 install --upgrade pip && pip3 install gunicorn
RUN ln -sf /usr/bin/python3 /usr/bin/python

WORKDIR /tmp
RUN curl -O https://wordpress.org/latest.tar.gz \
 && mkdir -p "${WORDPRESS_PATH}" \
 && tar xzvf latest.tar.gz -C "${WORDPRESS_PATH}" --strip-components=1
RUN curl -O https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/wp-cli.phar \
 && chmod +x wp-cli.phar \
 && mv wp-cli.phar /usr/bin/wp

RUN git clone \
    https://github.com/django-daiquiri/wordpress-plugin \
    ${WORDPRESS_PATH}/wp-content/plugins/daiquiri
RUN git clone \
    https://github.com/django-daiquiri/wordpress-theme \
    ${WORDPRESS_PATH}/wp-content/themes/daiquiri

# RUN apt install -y <ADDITIONAL_PACKAGES>

RUN ln -s /vol/tools/shed/caddy /bin/caddy

RUN groupadd -g "${GID}" "${GNAME}" \
 && useradd -m -s /bin/bash -g "${GNAME}" -u "${UID}" "${USER}" \
 && chown -R "${USER}:${GID}" "${HOME}" \
 && chmod -R 777 /tmp /var/log

RUN mkdir -p /run/php \
 && chown -R ${USER}:${USER} /run/php/
RUN sed -i "s/user = .*/user = dq/g" /etc/php/7.3/fpm/pool.d/www.conf \
 && sed -i "s/group = .*/group = dq/g" /etc/php/7.3/fpm/pool.d/www.conf \
 && sed -i "s/listen.owner = .*/listen.owner = dq/g" /etc/php/7.3/fpm/pool.d/www.conf

USER ${USER}

HEALTHCHECK --timeout=3s --interval=60s --retries=3 \
   CMD pgrep php-fpm && pgrep caddy

CMD ["/drun.sh"]
