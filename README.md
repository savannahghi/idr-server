## IDR Server

IDR(Integrated Data Repository) Server is a service that houses extract metadata
for/and receives extracted data from [IDR Clients](https://github.com/savannahghi/idr-client).
The service is built mainly using [Django](https://www.djangoproject.com/) and [Django Rest Framework.](https://www.django-rest-framework.org/)


[![Coverage Status](https://coveralls.io/repos/github/savannahghi/idr-server/badge.svg)](https://coveralls.io/github/savannahghi/idr-server)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Project overview
The server has three main entry points:
- admin:

    Admin acts as a supplement for what cannot be handled by **api endpoints**. It uses django's [built-in tool](https://docs.djangoproject.com/en/4.1/ref/contrib/admin/)
    that provides a web interface for managing objects in the database. One can do all the basic CRUD(Create, Update, Delete) and List operations
    using the tool.

- home:

    This the default view of the base url. It displays the dashboards that has been added using admin tool.


- api:

    The server uses [RESTful](https://www.geeksforgeeks.org/rest-api-introduction/) approach to serve the endpoints.
    This [link](https://drf-spectacular.readthedocs.io/en/latest/readme.html) gives detailed description of the available endpoints.

## Getting started

To run the project locally, first ensure you have python >=3.9 and PostgreSQL installed.
Create a database for the app and proceed in with these steps:

1. Ensure you have set the following variables.
   (You can use a simple file_name.sh file that can be sourced)

    | Variable                       | Example value              | Description                                     |
    |--------------------------------|----------------------------|-------------------------------------------------|
    | DJANGO_ADMIN_URL               | admin/        | url to access admin view                        |
    | DJANGO_ALLOWED_HOSTS           | "localhost,127.0.0.1"      | list of allowed hosts                           |
     | DJANGO_DEBUG                   | false                      | whether or not to run the app in debug mode     |
     | DJANGO_SECRET_KEY              | "django_project_secret_key.." | your django secret key                          |                     |
    | DJANGO_SETTINGS_MODULE         | "config.settings.local"    | the configuration file containing your settings |
     | POSTGRES_DB                    | "your_local_db_name"       | the database name in your local env             |
    | POSTGRES_PASSWORD              | "your_local_db_pwd"        | the password to the database                    |
     | POSTGRES_HOST                  | "127.0.0.1"                | host address on which the db is running         |
    | POSTGRES_USER                  | "your_db_user"             | the database user name                          |
    | GOOGLE_CLOUD_PROJECT           | "your_cloud_prj_id"        | gcloud project ID                               |
    | GOOGLE_APPLICATION_CREDENTIALS | "google_app_credentials" | the path to your google app credentials         |
    #### The values for the test variables are the same as above
    | Test Variables | Example value          | Description                                   |
    |------------------------|-----------------------------------------------|-------------------------------------------------|
    |TEST_POSTGRES_DB| "test_db_name"         | your test database name                       |
    |TEST_POSTGRES_HOST| "test host for the db" | local host address on which the db is running |
    |TEST_POSTGRES_PASSWORD| "test password"        | test database password                        |
    |TEST_POSTGRES_PORT| 5432                   | the port on which your db is running          |
    |TEST_POSTGRES_USER| "your test user"       | test db user name                             |

2. Clone the [repo](git@github.com:savannahghi/idr-server.git) and CD into the root of the directory of the application(directory containing manage.py file)


4. Create a virtual environment for the server. You may first have to install [virtualenvwrapper](https://pypi.org/project/virtualenvwrapper/)
    ```
   [machine@user idr-server]$ mkvirtualenv idr_venv

   [machine@user idr-server]$ workon idr_venv
    ```

4. Run pip install to install the required packages and run migrate to create tables.
    ```
   (idr_venv) [machine@user idr-server]$ pip install -r requirements.txt

   (idr_venv) [machine@user idr-server]$ ./manage.py migrate
    ```

5. Run the project by;

    ```
   (idr_venv)[machine@user idr-server]$ ./manage.py runserver
   ```



## Running Tests
```
(idr_venv)[machine@user idr-server]$ pytest .
```

## Licence

[MIT License](https://github.com/savannahghi/idr-client/blob/develop/LICENSE)

Copyright (c) 2022, Savannah Informatics Global Health Institute
