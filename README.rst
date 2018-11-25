twitter
=======

Twitter clone api implementation

.. image:: https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg
     :target: https://github.com/pydanny/cookiecutter-django/
     :alt: Built with Cookiecutter Django


:License: MIT

Basic Commands
--------------

Setting Up Your Users
^^^^^^^^^^^^^^^^^^^^^
Only superusers can be created for this app, it doesn't offer any registration endpoints.

* To create an **superuser account**, use this command::

    $ python manage.py createsuperuser

How to run application?
-----------------------

1. create database using docker

``docker run -d -p 5432:5432 -e POSTGRES_PASSWORD=<pw> --name=<name> postgres:<version>``

2. connect to database with some tool(I used pgcli) with your password(you can change that)

``pgcli -h 127.0.0.1 -U postgres``

3. create database twitter

``create database twitter``

4. position yourself in root directory and migrate migrations to database

``python manage.py migrate``

5. (optional) create your own data or load fixtures with this command

``python manage.py loaddata */fixtures/*``

6. run server on port 5100 (this will serve admin interface on http://localhost:5100/admin/ and api on http://127.0.0.1:5100/api/)

``python manage.py runserver 5100``

Api authentification
--------------------

The easiest way to authenticate is with JWT(Json web token) on `http://127.0.0.1:5100/api-auth/login/`
