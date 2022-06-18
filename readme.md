# Dq Dev [![build](https://github.com/django-daiquiri/dq-dev/actions/workflows/build.yaml/badge.svg)](https://github.com/django-daiquiri/dq-dev/actions/workflows/build.yaml)

<!--- mdtoc: toc begin -->

1. [Synopsis](#synopsis)
2. [How to use](#how-to-use)
3. [From scratch](#from-scratch)
4. [Tech background](#tech-background)
   1. [Dependencies](#dependencies)
   2. [Tests](#tests)<!--- mdtoc: toc end -->

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
