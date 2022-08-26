## IDR Server

IDR(Integrated Data Repository) Server is a service that houses extract metadata
for/and receives extracted data from [IDR Clients](https://github.com/savannahghi/idr-client).
The service is built mainly using [Django](https://www.djangoproject.com/) and [Django Rest Framework.](https://www.django-rest-framework.org/)


[![Coverage Status](https://coveralls.io/repos/github/savannahghi/idr-server/badge.svg)](https://coveralls.io/github/savannahghi/idr-server)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Project overview
The server has three main entry points:

- api:

    The server uses [RESTful](https://www.geeksforgeeks.org/rest-api-introduction/) approach;\
    this section gives a brief description of the available endpoints.

        -> {base_url}/api
            This is the entry point for all the API requests to the server.

        -> .../sql_database_sources:
            This serves all operations related to adding, updating, listing and deleting sources of data.
            The sources are mainly database vendors e.g MySQL, PostgreSQL etc. This url provides input for
            data source versions.

        -> .../data_source_versions:
            Helps in adding version labels to the database sources created in the previous endpoint.

        -> .../sql_extract_metadata:
            Serves valid sql queries that clients can use to extract data from local databases. The metadata
            includes proper labels that should be tagged along with the data that it extracts.

        -> .../sql_upload_metadata:
            This serves a summary information about the data that the client needs to upload. Data is
            uploaded in form of chunks; every chunk has to be related to a upload_metadata.

        -> .../sql_upload_chunks:
            This serves the actual data that is uploaded by the client. A client shoud first request for
            the creation of upload_metadata before sending chunks to the server.

- home:

    This the default view/landing page of the base url. It displays the dashboards that has been added using admin tool.


- admin:

    Admin acts as a supplement for what cannot be handled by **api endpoints**. It uses django's [built-in tool](https://docs.djangoproject.com/en/4.1/ref/contrib/admin/)
    that provides a web interface for managing objects in the database. One can do all the basic CRUD(Create, Update, Delete) and List operations
    using the tool.



## Getting started

To run the project locally, first ensure you have python >=3.9 and PostgreSQL installed.
Create a database for the app and proceed in with these steps:

1. Ensure you have set the following variables.
   (You can use a simple file_name.sh file that can be sourced)

    | Variable                       | Example value                | Description                   |
    |------------------------------|-------------------------------|-------------------------|
    | DJANGO_ADMIN_URL               | admin/                       | url to access admin view      |
    | DJANGO_ALLOWED_HOSTS           | "localhost,127.0.0.1"        | list of allowed hosts         |
     | DJANGO_DEBUG                   | false                        | whether or not to run the app in debug mode |
     | DJANGO_SECRET_KEY              | "django_project_secret_key.." | django secret key        |
    | DJANGO_SETTINGS_MODULE         | "config.settings.local"      | the configuration file containing your settings |
     | POSTGRES_DB                    | "db_name"                    | the database name in your local env |
    | POSTGRES_PASSWORD              | "db_pwd"                     | the password to the database  |
    | POSTGRES_PORT                    | 5432                     | the port on which the db is running |
    | POSTGRES_HOST                  | "127.0.0.1"                  | host address on which the db is running |
    | POSTGRES_USER                  | "db_user"                    | the database user name        |
    | GOOGLE_CLOUD_PROJECT           | "cloud_prj_id"               | gcloud project ID             |
    | GOOGLE_APPLICATION_CREDENTIALS | "google_app_credentials"     | the path to google app credentials |
    #### The values for the test variables are the same as above
    | Test Variables | Example value     | Description                                   |
    |-------------------|-----------------------------------------------|----------------|
    |TEST_POSTGRES_DB| "test_db_name"    | your test database name                       |
    |TEST_POSTGRES_HOST| "test host for the db" | host address on which the db is running |
    |TEST_POSTGRES_PASSWORD| "test password"   | test database password                        |
    |TEST_POSTGRES_PORT| 5432              | the port on which your db is running          |
    |TEST_POSTGRES_USER| "test user"       | test db user name                             |

2. Clone the [repo](git@github.com:savannahghi/idr-server.git) and CD into the root of the directory of the application(directory containing manage.py file)


4. Create a virtual environment for the server. You may first have to install [virtualenvwrapper](https://pypi.org/project/virtualenvwrapper/)
    ```
   [machine@user idr-server]$ mkvirtualenv idr_venv

   [machine@user idr-server]$ workon idr_venv
    ```

5. Run pip install to install the required packages and run migrate to create tables.
    ```
   (idr_venv) [machine@user idr-server]$ pip install -r requirements.txt

   (idr_venv) [machine@user idr-server]$ ./manage.py migrate
    ```

6. Create the superuser by running and following command and filling the resulting prompts.

    ```
   (idr_venv) [machine@user idr-server]$ ./manage.py createsuperuser
   ```

8. Run the project by;

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
