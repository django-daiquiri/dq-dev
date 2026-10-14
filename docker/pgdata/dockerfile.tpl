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
RUN cd /src ; GIT_SSL_NO_VERIFY=1 git clone --depth 1 --branch 1.5.2 https://github.com/postgrespro/pgsphere.git;
RUN cd /src/pgsphere; make USE_HEALPIX=0
RUN cd /src/pgsphere; make USE_HEALPIX=0 install
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

CMD ["postgres", "-c", "log_checkpoints=off"]
