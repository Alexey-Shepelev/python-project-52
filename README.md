# Task manager

A simple web application for managing tasks in a company or team. Implemented in the Django 4 framework using built-in class-based views and a PostgreSQL database.

#### [Task Manager](https://sailor-python-project-52-production.up.railway.app) - link to the project risen on Railway.

## How to install and use
#### Install PostgreSQL and create database
for tests and local using this section may be skipped and SQLite can be used
```commandline
sudo apt install postgresql
```
```commandline
whoami
{yourusername}
sudo -u postgres createuser --createdb {yourusername}
createdb {yourdb}
```
#### Clone the repo
```commandline
git clone git@github.com:Alexey-Shepelev/python-project-52.git
```
#### Change directory
```commandline
cd python-project-52
```
#### Rename `.env.sample` file to `.env` and add following variables:
`SECRET_KEY={your_secret_key}`

`DATABASE_URL=postgresql://{yourusername}:{password}@{host}:{port}/{yourdb}`<br> 
<small>delete if intend to use SQLite</small>

`ROLLBAR_ACCESS_TOKEN={your_rollbar_token}`<br>
<small>to use Rollbar</small>

#### Install dependencies and make migrations
```commandline
make install
make migrate
```

Start command for local use
```commandline
make dev
```

Start command for deploy
```commandline
make start
```

---

### Tests, linter and Codeclimate statuses:
[![Actions Status](https://github.com/Alexey-Shepelev/python-project-52/workflows/hexlet-check/badge.svg)](https://github.com/Alexey-Shepelev/python-project-52/actions)
[![ci-tests](https://github.com/Alexey-Shepelev/python-project-52/actions/workflows/ci-tests.yml/badge.svg)](https://github.com/Alexey-Shepelev/python-project-52/actions/workflows/ci-tests.yml)
[![Maintainability](https://api.codeclimate.com/v1/badges/3dfdd05bc70770b32112/maintainability)](https://codeclimate.com/github/Alexey-Shepelev/python-project-52/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/3dfdd05bc70770b32112/test_coverage)](https://codeclimate.com/github/Alexey-Shepelev/python-project-52/test_coverage)

---

#### Screenshots:

|     |     |
|-----|-----|
|     |     |