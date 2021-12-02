FROM alpine:latest

RUN apk --update add bash curl grep

HEALTHCHECK --interval=5s --timeout=5s --retries=3 \
    CMD pgrep caddy

ADD ./docker/* /

CMD ["/bin/bash", "/drun.sh"]
