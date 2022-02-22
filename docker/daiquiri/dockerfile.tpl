FROM debian:latest

ENV USER=dq
ENV UID=<UID>
ENV GNAME=dq
# ENV GID=<GID>
ENV HOME=/home/dq

ENV INIT_PID_FILE=/tmp/init.pid

ENV PATH=${PATH}:/home/dq/sh:/home/dq/.local/bin:${HOME}/bin:${HOME}/sh:/vol/tools/shed

RUN apt update -y
RUN apt update -y && apt install -y \
    curl \
    git \
    netcat \
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

COPY ./rootfs /
RUN mkdir ${HOME}/log
RUN echo "docker build" > "${INIT_PID_FILE}"

RUN ${HOME}/sh/install-from-github.sh \
    "triole/supervisord/releases/latest" \
    "(?<=href\=\").*_linux_x86_64.tar.gz" \
    "${HOME}/bin"

RUN chmod -R 777 /tmp
RUN find /tmp -type f -executable -regex ".*\/custom_scripts\/build.*" \
    | sort | xargs -i /bin/bash {}

RUN pip3 install --upgrade pip && pip3 install gunicorn
RUN ln -sf /usr/bin/python3 /usr/bin/python

# RUN apt install -y <ADDITIONAL_PACKAGES>

RUN ln -s /vol/tools/shed/caddy /bin/caddy

RUN groupadd "${GNAME}" \
 && useradd -m -s /bin/bash -g "${GNAME}" -u "${UID}" "${USER}" \
 && chown -R "${USER}:${GID}" "${HOME}" \
 && chmod -R 777 /tmp /var/log

USER ${USER}

HEALTHCHECK --timeout=3s --interval=60s --retries=3 \
   CMD pgrep caddy

CMD ["/home/dq/bin/supervisord", "-c", "/home/dq/conf/supervisord.conf"]
