FROM rabbitmq:3.8-management

ENV USER=dq
ENV UID=<UID>
ENV GNAME=dq
ENV GID=<GID>
ENV HOME=/home/dq

COPY ./rootfs /

RUN groupadd -g "${GID}" "${GNAME}" \
 && useradd -m -s /bin/bash -g "${GNAME}" -u "${UID}" "${USER}" \
 && chown -R "${USER}:${GID}" "${HOME}" \
 && chmod -R 777 /tmp /var/log

USER ${USER}

HEALTHCHECK --timeout=3s --interval=60s --retries=3 \
     CMD rabbitmq-diagnostics -q ping

CMD ${HOME}/sh/launch-rabbitmq.sh
