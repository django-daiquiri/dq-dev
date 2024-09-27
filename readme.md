# Dq Dev [![build](https://github.com/django-daiquiri/dq-dev/actions/workflows/build.yaml/badge.svg)](https://github.com/django-daiquiri/dq-dev/actions/workflows/build.yaml)

<!-- toc -->

- [Synopsis](#synopsis)
- [How to use](#how-to-use)
- [From scratch](#from-scratch)
- [Tech background](#tech-background)
  - [Dependencies](#dependencies)
  - [Tests](#tests)
  - [CLI Args](#cli-args)

<!-- /toc -->

## Synopsis

A daiquiri docker containerisation that started as development setup. It brings quite a few configuration options that can be found looking into the toml files in the `conf` folder. An abstraction layer that is written in python aims to provide an easier access to all the different functions supporting multiple profiles and other things.

Please make sure that you have [docker](https://www.docker.com/) and [docker compose](https://github.com/docker/compose/releases) to make use of dq dev.

The required python libraries can be installed as usual `pip install -r requirements.txt`.

## How to use

Interaction is done via the `manage.py` script. You can call `-h` for help.

A workflow could be

```python
# create a new profile
python manage.py -c newprof

# set it to active
python manage.py -s newprof

# and run it
python manage.py -r
```

Note that `-r` can also take a profile name as argument. But if none given the active profile will be used for the action. Same for other commands. The idea behind the `active profile` is that one does not have to pass the profile name as argument to the command one wants to run.

Profiles are saved in `usr/profiles/PROFILENAME`. Make sure you edit the `conf.yaml` there to adjust the settings you want to use.

## From scratch

Following directories should be present for a default app setup.

```bash
mkdir dq-project
cd dq-project

# clones daiquiri source into folder daiquiri
git clone git@github.com:django-daiquiri/daiquiri.git

# clones default app into app folder
git clone git@github.com:django-daiquiri/app.git

# clones the dq-dev setup into dq-dev folder
git clone https://github.com/django-daiquiri/dq-dev.git
```

Edit the configuration for the dq-dev setup:

```bash
cd dq-dev
nano tpl/conf.yaml
```

You can have multiple apps on the system. Active app is set via `active_app` entry, `daiquiri` is the default app. Make sure, to check the paths n `folders_on_host` section pointing them to your directories. In case it is needed, make the DB persistent in the `enable_volumes` section.

Set and activate the profile as shown in the previous section. Run the setup.

The instance will be available on `localhost:9280` for the default settings.

## Tech background

I use [caddy](https://github.com/caddyserver/caddy) as http server and reverse proxy. Usually caddy is mounted into the daiquiri docker via the `shed` volume. If caddy does exist there, it will be used. If not the latest caddy will be pulled from github automatically.

### Dependencies

A python script is used to render the `docker-compose.yaml`. The script is called by the makefile and requires `pyYAML`. Make sure it is installed. You can use the requirements file for that.

```
pip install -r requirements.txt
```

### Tests

In the mainfolder is a python script `request_test.py` that fires some simple requests at Daiquiri. It helps to check proxy configurations. Try `python request_test.py -h` to find out what it can do.

### CLI Args

```go mdox-exec="python manage.py -h"
usage: manage.py [-h] [-b [BUILD ...]] [-bnc [BUILD_NO_CACHE ...]]
                 [-r [RUN ...]] [-p [STOP ...]] [-d [DOWN ...]] [-rmi] [-rmn]
                 [-g [TAIL_LOGS ...]] [-c CREATE_PROFILE] [-s SET_PROFILE]
                 [-e [RENDER ...]] [-a [DISPLAY_PROFILE ...]]
                 [--list_snapshots] [--save_snapshot [SAVE_SNAPSHOT ...]]
                 [--restore_snapshot [RESTORE_SNAPSHOT ...]] [-n]

Manage.Py: dq-dev, daiquiri docker compose dev setup

options:
  -h, --help            show this help message and exit
  -b [BUILD ...], --build [BUILD ...]
                        build a profile's containers, exit when done
  -bnc [BUILD_NO_CACHE ...], --build_no_cache [BUILD_NO_CACHE ...]
                        build a profile's containers without using cache, exit when done
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
