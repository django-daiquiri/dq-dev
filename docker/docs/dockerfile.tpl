FROM alpine:latest

ENV VOLDIR="/vol"
ENV TIMEZONE="Europe/Berlin"

ENV USER=docs
ENV UID=<UID>
ENV GNAME=docs
# ENV GID=<GID>
ENV HOME=/home/docs

ENV PATH=${PATH}:${HOME}/bin:${HOME}/sh

RUN apk --update add bash curl git grep openssh

RUN apk --update add tzdata \
 && cp "/usr/share/zoneinfo/${TIMEZONE}" "/etc/localtime" \
 && echo "${TIMEZONE}" > "/etc/timezone" \
 && apk del tzdata \
 && rm -rf /var/cache/apk/*

COPY ./rootfs /
RUN ls ${HOME}/sh

RUN ${HOME}/sh/install_from_github.sh \
    "triole/supervisord/releases/latest" \
    "(?<=href\=\").*_linux_x86_64.tar.gz" \
    "${HOME}/bin"

RUN ${HOME}/sh/install_from_github.sh \
    "caddyserver/caddy/releases/latest" \
    "(?<=href\=\").*_linux_amd64.tar.gz" \
    "${HOME}/bin"

RUN ${HOME}/sh/install_from_github.sh \
    "triole/lunr-indexer/releases/latest" \
    "(?<=href\=\").*_linux_x86_64.tar.gz" \
    "${HOME}/bin"

RUN ${HOME}/sh/install_from_github.sh \
    "triole/webhook/releases/latest" \
    "(?<=href\=\").*_linux_amd64.tar.gz" \
    "${HOME}/bin"

RUN addgroup -S "${USER}" \
 && adduser -s "/bin/false" -h "${HOME}" -G "${GNAME}" -u "${UID}" -S "${USER}"

RUN mkdir -p "${VOLDIR}" \
 && chown -R "${USER}":"${GNAME}" "${HOME}" "${VOLDIR}"

HEALTHCHECK --interval=60s --timeout=5s --retries=3 \
    CMD curl http://localhost:8080

USER ${USER}
CMD ["/home/docs/bin/supervisord", "-c", "/home/docs/conf/supervisord.conf"]
