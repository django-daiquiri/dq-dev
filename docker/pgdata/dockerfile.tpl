FROM  postgis/postgis:16-master

ENV PATH="${PATH}:/opt:/vol/tools/shed"
ENV DEBIAN_FRONTEND=noninteractive

RUN apt update \
      && apt install -y --no-install-recommends \
        git make bison flex \
        gcc \
        postgresql-server-dev-16 \
        postgresql-plpython3-16 \
      && rm -rf /var/lib/apt/lists/*
RUN mkdir /src
RUN cd /src ; GIT_SSL_NO_VERIFY=1 git clone -b aiprdbms16-dev https://github.com/kimakan/pgsphere.git
RUN cd /src/pgsphere; gmake USE_PGXS=1 PG_CONFIG=/usr/bin/pg_config
RUN cd /src/pgsphere; gmake USE_PGXS=1 PG_CONFIG=/usr/bin/pg_config install
RUN rm -fr /src
# Clean up container
RUN apt remove gcc make postgresql-server-dev-16 bison flex -y
RUN apt autoremove -y

RUN mkdir -p /docker-entrypoint-initdb.d/
COPY rootfs/20-init-db.sh /docker-entrypoint-initdb.d/

COPY ./rootfs /
RUN chmod -R 777 /tmp
RUN find /tmp/custom_scripts/build -type f -executable | sort | xargs -i /bin/bash {}

# RUN apt install -y <ADDITIONAL_PACKAGES>

RUN sed -i -e 's/^\(postgres:[^:]\):[0-9]*:[0-9]*:/\1:1000:1000:/' /etc/passwd
