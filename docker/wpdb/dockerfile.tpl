FROM mysql:5.7-debian

RUN apt update -y

# RUN apt install -y <ADDITIONAL_PACKAGES>

RUN sed -i -e 's/^\(mysql:[^:]\):[0-9]*:[0-9]*:/\1:<UID>:<GID>:/' /etc/passwd
