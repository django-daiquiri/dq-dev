# Dqdev Reverse Proxy

This folder contains a reverse proxy docker setup meant for local tls tests. It spins up a docker exposing port `443` and acts as reverse proxy forwarding all requests to dq-dev running behind it.

The hostname is `dqdev-rp`. If you want to connect to the reverse proxy please make sure that your machine can resolve the hostname. You may need to add something like `127.0.0.1 dqdev-rp` to your `/etc/hosts`.

The reverse proxy tries to connect to a dqdev profile called `test`. If you wan't it to work a differently named profile you need to generate new tls keys, adjust settings in the `Caddyfile` and change the network name in `run.sh`.

Please also keep in mind that your `test` profile config needs the following settings.

```toml
[env.daiquiri]
url_hostname = "dqdev-rp"
url_protocol = "https"
```
