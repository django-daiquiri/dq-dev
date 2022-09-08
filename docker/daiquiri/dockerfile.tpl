FROM debian:latest

ENV USER=dq
ENV UID=<UID>
ENV GNAME=dq
# ENV GID=<GID>
ENV HOME=/home/dq

ENV INIT_FINISHED_FILE=${HOME}/run/init.finished

ENV PATH=${PATH}:/home/dq/sh:/home/dq/.local/bin:${HOME}/bin:${HOME}/sh:/vol/tools/shed

RUN apt update -y
RUN apt update -y && apt install -y \
    curl \
    file \
    gettext \
    git \
    jq \
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
    libssl-dev

RUN apt -y install gnupg2 wget vim
RUN echo "deb http://apt.postgresql.org/pub/repos/apt \
    $(cat /etc/os-release | grep -Po "(?<=VERSION_CODENAME=).*")-pgdg main" \
    > /etc/apt/sources.list.d/pgdg.list
RUN wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add
RUN apt -y update && apt -y install postgresql-client

COPY ./rootfs /
RUN mkdir ${HOME}/log ${HOME}/run

RUN ${HOME}/sh/install-from-github.sh \
    "triole/supervisord/releases/latest" \
    "(?<=href\=\").*_linux_x86_64.tar.gz" \
    "${HOME}/bin"

RUN ${HOME}/sh/install-from-github.sh \
    "triole/lunr-indexer/releases/latest" \
    "(?<=href\=\").*_linux_x86_64.tar.gz" \
    "${HOME}/bin"

RUN ${HOME}/sh/install-from-github.sh \
    "triole/webhook/releases/latest" \
    "(?<=href\=\").*_linux_amd64.tar.gz" \
    "${HOME}/bin"

RUN ${HOME}/sh/install-from-github.sh \
    "aptible/supercronic/releases/latest" \
    "(?<=href\=\").*-linux-amd64" \
    "${HOME}/bin/supercronic"


RUN groupadd "${GNAME}" \
 && useradd -m -s /bin/bash -g "${GNAME}" -u "${UID}" "${USER}"

RUN chown -R ${USER}:${USER} /tmp

RUN find /tmp -type f -executable -regex ".*\/custom_scripts\/build.*" \
    | sort | xargs -i /bin/bash {}

RUN pip3 install --upgrade pip && pip3 install gunicorn
RUN ln -sf /usr/bin/python3 /usr/bin/python

# RUN apt install -y <ADDITIONAL_PACKAGES>

RUN ln -s /vol/tools/shed/caddy /bin/caddy

RUN ${HOME}/sh/add_user.sh
USER ${USER}

HEALTHCHECK --timeout=3s --interval=60s --retries=3 \
   CMD ${HOME}/sh/healthcheck.sh

CMD ["/bin/bash", "/drun.sh"]
