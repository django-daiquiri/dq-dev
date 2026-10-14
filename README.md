# dq-dev [![build](https://github.com/django-daiquiri/dq-dev/actions/workflows/build.yaml/badge.svg)](https://github.com/django-daiquiri/dq-dev/actions/workflows/build.yaml)

<!-- toc -->

- [New pgSphere](#new-pgsphere)
- [Overview](#overview)
- [Setup](#setup)
- [How to use](#how-to-use)
- [From scratch](#from-scratch)
- [Tech background](#tech-background)
  - [Tests](#tests)
  - [CLI Args](#cli-args)

<!-- /toc -->

## New pgSphere

The `pgdata` image includes pgSphere 1.5.2. If you are reusing a database created
with an older pgSphere version, update the extension after rebuilding and
starting the profile with the updated image.

Enter the Daiquiri container, replacing `<profile_name>` with your profile name:

```bash
docker exec -it dqdev-daiquiri-<profile_name> bash
```

Then connect to the scientific database using `DATABASE_DATA` and update the extension:

```bash
psql "$DATABASE_DATA" -c "ALTER EXTENSION pg_sphere UPDATE TO '1.5.2';"
```

Fresh databases initialize the extension automatically.

## Overview

A Python toolset for managing [Daiquiri](https://github.com/django-daiquiri/daiquiri)
containers with Docker Compose. It supports multiple profiles, each with its own
configuration, containers, and network. Configuration templates are in
`conf_tpl/conf.toml` and `conf_tpl/secrets.toml`.

By default, a profile enables the Daiquiri container, an application database
(`pgapp`), and a scientific database (`pgdata`). RabbitMQ is optional and disabled
by default, as is asynchronous processing.

## Setup

You need Python 3.11 or newer, [Docker Engine](https://www.docker.com/), and
[Docker Compose v2](https://github.com/docker/compose), available as `docker compose`.

From a cloned checkout, install the Python dependencies, preferably in an
activated virtual environment:

```bash
cd dq-dev
python -m pip install .
```

## How to use

Run `python manage.py` from the `dq-dev` directory. Use `python manage.py -h` for help.

A typical workflow is:

```bash
# create a new profile
python manage.py -c newprof

# configure host paths and credentials before running it
${EDITOR:-vi} usr/profiles/newprof/conf.toml usr/profiles/newprof/secrets.toml

# set it to active
python manage.py -s newprof

# and run it
python manage.py -r
```

Profiles are saved in `usr/profiles/<profile_name>/`. Creating a profile copies
`conf.toml` and `secrets.toml` from `conf_tpl/`. Configure these files for your app;
the [From scratch](#from-scratch) section shows the settings for the default app.

The active profile is recorded in `usr/profiles/active.toml`. Select it explicitly
with `-s <profile_name>` before running build, run, stop, or down commands.
Running without arguments lists profiles.

`-r` builds and starts the containers, then follows their logs. Pressing `<Ctrl>C`
ends log following; the containers keep running. Use `-p` to stop them or `-d` to
stop and remove them and their Docker volumes.

## From scratch

For a default app using Daiquiri installed from PyPI inside the container:

```bash
mkdir dq-project
cd dq-project

# clone the default app into the app folder
git clone https://github.com/django-daiquiri/app.git

# clone dq-dev
git clone https://github.com/django-daiquiri/dq-dev.git

cd dq-dev
python -m pip install .
python manage.py -c myapp
${EDITOR:-vi} usr/profiles/myapp/conf.toml usr/profiles/myapp/secrets.toml
```

In the generated `conf.toml`, update the existing entries below and keep the
remaining template settings. Replace the example host path with the absolute
path to your app checkout. Keep `active_app = "dq_app"` at the top of the file
and the container's `dq_app` mount point as `/home/dq/app`.

```toml
[folders_on_host]
dq_app = "/absolute/path/to/dq-project/app"
# dq_source = "<HOME>/srv/daiquiri"

[docker_volume_mountpoints]
dq_app = "/home/dq/app"
# dq_source = "/home/dq/source"

[enable_volumes]
pgapp = false
pgdata = false
docs = false

[env.daiquiri]
docs_git_url = ""
```

**Comment out both `dq_source` entries** when using the PyPI package. The
container installs Daiquiri through the app's `daiquiri` extra.

For application content from a Git repository, set `enable_volumes.docs = true`,
configure `folders_on_host.docs`, and set `env.daiquiri.docs_git_url` to the
repository URL. Put any content-repository credentials in the `[daiquiri]`
section of `secrets.toml`.

To persist database data on the host, set `pgapp = true` and `pgdata = true` in
`[enable_volumes]` before the first run. Their data will be stored in
`usr/profiles/myapp/pgapp/` and `usr/profiles/myapp/pgdata/`. These host directories
remain after `-d`.

Activate the profile and start it:

```bash
python manage.py -s myapp
python manage.py -r
```

After initialization, the instance is available at `http://localhost:9280`.
If you change the exposed Daiquiri port, update `env.daiquiri.url_hostname` to
match it.

For framework development, optionally clone
`https://github.com/django-daiquiri/daiquiri.git` and enable both source entries:

```toml
[folders_on_host]
dq_source = "/absolute/path/to/daiquiri"

[docker_volume_mountpoints]
dq_source = "/home/dq/source"
```

The container then installs the mounted Daiquiri checkout in editable mode and
builds its frontend assets.

## Tech background

The Daiquiri container uses Nginx as its HTTP server and reverse proxy. It serves
static assets and protected downloads, and forwards application requests to
port 8000. By default, Django's development server runs on that port; setting
`env.daiquiri.enable_gunicorn = true` selects Gunicorn. Supervisord manages the
container's processes.

### Tests

The tests are currently outdated and will be updated in the near future.

### CLI Args

The parser help for `python manage.py -h`:

```text
usage: manage.py [-h] [-b [BUILD ...]] [-bnc [BUILD_NO_CACHE ...]]
                 [--build-release] [-r [RUN ...]] [-p [STOP ...]]
                 [-d [DOWN ...]] [-rmi] [-rmn] [-g [TAIL_LOGS ...]]
                 [-c CREATE_PROFILE] [-s SET_PROFILE] [-e [RENDER ...]]
                 [-a [DISPLAY_PROFILE ...]] [--list_snapshots]
                 [--save_snapshot [SAVE_SNAPSHOT ...]]
                 [--restore_snapshot [RESTORE_SNAPSHOT ...]] [-n]

manage.py: daiquiri docker compose dev setup

options:
  -h, --help            show this help message and exit
  -b [BUILD ...], --build [BUILD ...]
                        build a profile's containers, exit when done
  -bnc [BUILD_NO_CACHE ...], --build_no_cache [BUILD_NO_CACHE ...]
                        build a profile's containers without using cache, exit
                        when done
  --build-release       build and check a Daiquiri release, then stop the
                        active profile
  -r [RUN ...], --run [RUN ...]
                        run a profile's containers, build if necessary
  -p [STOP ...], --stop [STOP ...]
                        stop profile's running containers
  -d [DOWN ...], --down [DOWN ...]
                        stop and remove profile's running containers, remove
                        docker's volumes, keep folders containing the volume
                        data, they can be reused on next run
  -rmi, --remove_images
                        remove images when running "down", use in combination
                        "-d -rmi"
  -rmn, --remove_network
                        remove daiquiri containers' network
  -g [TAIL_LOGS ...], --tail_logs [TAIL_LOGS ...]
                        tail docker compose logs
  -c CREATE_PROFILE, --create_profile CREATE_PROFILE
                        create a new profile with the default settings
  -s SET_PROFILE, --set_profile SET_PROFILE
                        set profile to active
  -e [RENDER ...], --render [RENDER ...]
                        only render docker-compose.yaml for profile
  -a [DISPLAY_PROFILE ...], --display_profile [DISPLAY_PROFILE ...]
                        display currently active profile
  --list_snapshots      list currently saved snapshots
  --save_snapshot [SAVE_SNAPSHOT ...]
                        save current db and config to snapshot
  --restore_snapshot [RESTORE_SNAPSHOT ...]
                        restore saved snapshot
  -n, --dry_run         do not run any docker-compose commands nor save
                        rendered docker-compose.yaml, just print them

If used without arg, profile list is displayed
```

`--build-release` requires an active profile with both `dq_source` entries
enabled. It starts the profile, waits for initialization, clears the source
checkout's `dist/` directory, installs release dependencies, runs
`daiquiri-admin build` and `twine check dist/*`, then stops the active profile.
Artifacts are written to `dist/` in the mounted source checkout. See the framework's
[release documentation](https://django-daiquiri.github.io/docs/release/) for the
full maintainer workflow.

Snapshot commands require a name, such as `--save_snapshot before_update` or
`--restore_snapshot before_update`. They save ZIP archives in `usr/snapshots/`
and restore files to their original profile path. The intended contents are the
profile directory, including configuration, secrets, and any database data
persisted inside it. The current relative-path handling can produce empty
archives; check the archive contents before relying on a snapshot.

`-n` skips Docker commands and writing the rendered Compose YAML. Initialization,
Dockerfile rendering, and profile or snapshot operations can still change local
files.

Image removal with `-rmi` is currently unreliable.
