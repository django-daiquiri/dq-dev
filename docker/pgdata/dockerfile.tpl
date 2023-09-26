FROM postgres:13

ENV PATH="${PATH}:/opt:/vol/tools/shed"

RUN apt update -y && apt install -y \
  postgresql-client

COPY ./rootfs /
RUN chmod -R 777 /tmp
RUN find /tmp/custom_scripts/build -type f -executable | sort | xargs -i /bin/bash {}

# RUN apt install -y <ADDITIONAL_PACKAGES>

RUN sed -i -e 's/^\(postgres:[^:]\):[0-9]*:[0-9]*:/\1:1000:1000:/' /etc/passwd
