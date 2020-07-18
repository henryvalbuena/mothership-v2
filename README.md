# Mothership V2
Backend app to manage multiple APIs for front-end apps

## Apps Supported
- Latte Machine [app](https://github.com/henryvalbuena/latte-machine)

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by navigating to the `requirements` directory and running:

```bash
pip install -r requirements-dev.txt
```

This will install all of the required packages we selected within the `requirements-prod.txt` and `requirements-dev.txt` files.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) are libraries to handle the lightweight sqlite database. Since we want you to focus on auth, we handle the heavy lift for you in `./src/database/models.py`. We recommend skimming this code first so you know how to interface with the Drink model.

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

## Running the server

We are going to be using the `manage.py` module, which is going to set up our app and database.

To initialize the database, execute:

```bash
./manage.py flask db upgrade
```

To run the server, execute:

```bash
./manage.py flask run
```

## API Docs

Check [here](https://github.com/henryvalbuena/mothership-v2/blob/master/api_docs/latte_machine/README.md)

## Author

Henry Valbuena

## License

[Here](https://github.com/henryvalbuena/mothership-v2/blob/master/LICENSE)
