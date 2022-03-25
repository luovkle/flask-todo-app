# How to use

## Get code

```sh
git clone https://github.com/luovkle/flask-todo-app.git
cd flask-todo-app
```

## Run postgres

Example with docker.

```sh
docker run --rm -d -p 5432:5432 -e POSTGRES_USER=user -e POSTGRES_PASSWORD=password -e POSTGRES_DB=app postgres:13.3-alpine
```

## Install dependencies in a virtual environment

Example with pip and venv.

```sh
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Export environment variables

Example with bash/zsh shell.

```sh
export FLASK_APP=app.run.py
export FLASK_RUN_PORT=8080
export FLASK_DATABASE_HOST="127.0.0.1"
export FLASK_DATABASE_USER="user"
export FLASK_DATABASE_PASSWORD="password"
export FLASK_DATABASE="app"
```

## initialize database

```sh
flask init-db
```

## Running the server

```sh
flask run
```
