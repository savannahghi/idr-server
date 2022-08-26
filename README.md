## IDR Server

IDR(Integrated Data Repository) Server is a service that houses extract metadata
for/and receives extracted data from [IDR Clients](https://github.com/savannahghi/idr-client).
The service is built mainly using [Django](https://www.djangoproject.com/) and [Django Rest Framework.](https://www.django-rest-framework.org/)


[![Coverage Status](https://coveralls.io/repos/github/savannahghi/idr-server/badge.svg)](https://coveralls.io/github/savannahghi/idr-server)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Project overview
The server has two main entry points, namely admin and API. **Admin** is django's built-in tool that provides a web
interface for managing objects in the database. One can do all the basic CRUD(Create, Update, Delete) and List operations
using the tool.


### API
This entry point handles the bulk of the work that comes in form of requests. The server uses [RESTful](https://www.geeksforgeeks.org/rest-api-introduction/) approach;
thus a client sends requests in form of data then the server uses this client input to start internal processing and return
output back to the client.

#### IDR server endpoints
The server has a number of endpoints that serve specific data. This section gives a brief description of each of
them:

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


## Getting started

To run the project locally, first ensure you have python >=3.9 and PostgreSQL installed.
Create a database for the app and proceed in with these steps:

1. Ensure you have set the following variables (you can use a simple .sh file that can be sourced)

| Variable  | Example value                      |
|-----------|------------------------------------|
| DJANGO_ADMIN_URL    | admin/                             |
| DJANGO_ALLOWED_HOSTS | "localhost,127.0.0.1"              |
 |DJANGO_DEBUG| false                              |
 |DJANGO_SECRET_KEY| "your_django_project_secret_key.." |
|DJANGO_SETTINGS_MODULE| "config.settings.local"            |
 |POSTGRES_DB| "your_local_db_name"               |
|POSTGRES_PASSWORD| "your_local_db_pwd"                |
 |POSTGRES_HOST| "127.0.0.1"                        |
|POSTGRES_USER| "your_db_user"                     |
|GOOGLE_CLOUD_PROJECT| "your_cloud_prj_id"                |
|GOOGLE_APPLICATION_CREDENTIALS| "path/to/google_app_credentials"   |


2. Clone the [repo](git@github.com:savannahghi/idr-server.git) and CD into the root of the directory of the application.


4. Create a virtual environment for the server. You may first have to install [virtualenvwrapper](https://pypi.org/project/virtualenvwrapper/)

   [machine@user idr-server]$ mkvirtualenv idr_venv

   [machine@user idr-server]$ workon idr_venv


4. Run pip install to install the required packages and run migrate to create tables.

   (idr_venv) [machine@user idr-server]$ pip install -r requirements.txt

   (idr_venv) [machine@user idr-server]$ ./manage.py migrate


5. Run the project by;

   (idr_venv)[machine@user idr-server]$ ./manage.py runserver


## Deployment


The application is deployed via [Google Cloud Build]( https://cloud.google.com/build ) to [Google Cloud Run]( https://cloud.google.com/run ).
There's a cloudbuild.yaml file in the home folder. Secret variables are managed with [Google Secret Manager]( https://cloud.google.com/secret-manager ).
