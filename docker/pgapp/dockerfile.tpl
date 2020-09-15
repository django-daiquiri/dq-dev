FROM postgres:latest

ENV PATH="${PATH}:/opt:/vol/tools/shed"

RUN apt update -y && apt install -y \
    postgresql-client

RUN sed -i -e 's/^\(postgres:[^:]\):[0-9]*:[0-9]*:/\1:<UID>:<GID>:/' /etc/passwd