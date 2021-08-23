# Flask Finances API

A simple finances API made with Flask and SQLAlchemy


# Techs used
- Flask
- SQLalchemy

# Installing the Development Environment
- Install python3 on your machine. You can download it on the following link: https://www.python.org/downloads/
- install virtualenv package with pip:
```bash
$ pip install virtualenv
```
- Clone this repository on your machine
- cd into the repository folder, and create a python virtual environment:
```bash
$ cd flask_finances_api

$ virtualenv venv
```
- Activate your new python virtual environment:
```bash
# Windows OS
$ .\venv\Script\activate.bat

# Unix OS
$ source /venv/bin/activate

```
- Install all the python packages from the requirements.txt file
```bash
$(venv) pip install -r requirements.txt
```

# Configuring the envionment variables
- To run the Flask application, you will need to create a `.env` file on the root of the project with the following variables:
```
export FLASK_APP=src
export FLASK_ENV=development
export SECRET_KEY=<define_a_secretkey_here>
export DATABASE_URL=<define_a_database_url_here>
```

# Configuring the database
This project needs a Relational Database, like PostgreSQL or MySQL. You can choose the one you like the most. After creating it, you will need to add the url on the `DATABASE_URL` environment variable.

After that, run the following commands:
```bash
$(venv) flask db migrate

$(venv) flask db upgrade
```

# Starting the Local Server
- To start the local server, run the following command:
```bash
$(venv) flask run
```

This will start the server on the port 5000.