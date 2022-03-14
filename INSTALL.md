
# Local Deployment (for test)

Several packages need to be install before running django-weathervis.
The following details how to install those packages and deploy this application.

> Warning: I run on python 3.9, so to avoid any issues when running it, you should do the same. (see [below](#py39))

# Install PostgreSQL and PostGis

## Linux (Ubuntu)

### PostgreSQL

Log into your Ubuntu system and update the system software packages using the following apt command.

    $ sudo apt update
    $ sudo apt -y upgrade

Now install the latest version of PostgreSQL from the default Ubuntu repositories.

    $ sudo apt install postgresql

During the installation, the installer will create a new PostgreSQL cluster (a collection of databases that will be managed by a single server instance), thus initialize the database. The default data directory is /var/lib/postgresql/12/main and the configurations files are stored in the /etc/postgresql/12/main directory.

After PostgreSQL installed, you can confirm that the PostgreSQL service is active, running and is enabled under systemd using the following systemctl commands:

    $ sudo systemctl is-active postgresql
    $ sudo systemctl is-enabled postgresql
    $ sudo systemctl status postgresql

Also, confirm that the Postgresql server is ready to accept connections from clients as follows:

    $ sudo pg_isready

### PostGis (additional to PostgesSQL)

    $ sudo apt update
    $ sudo apt -y upgrade

Wich version of PostgreSQL is installed

    psql --version

> With PostgreSQL 13:
> check package available
>
>    $ apt-cache search postgresql-13-postgis
>
>    $ sudo apt-get install postgresql-13-postgis-3 postgresql-13-postgis-3-scripts

check package

    $ sudo apt list --installed | grep postgresql

### see also
you could also have a look in [postgresql.org download](https://www.postgresql.org/download/)

## Mac OS

see [postgresql.org download](https://www.postgresql.org/download/macosx/)
> Note: I use PostgreSQL 13

[Here](https://realpython.com/lessons/set-up-postgresql-database/) is a video (0:00 to 5:00) which could help you installing PostgreSQL and PostGis
> Note: you do not need to create any table for now.


# Install QGis
Actually we need to install GDAL, GEOS, PROJ.4.
You can installed them individually, or installed QGIS which installed all those libraries

## Linux (Ubuntu)

    $ sudo apt update
    $ sudo apt -y upgrade

    $ sudo apt install gnupg software-properties-common

    $ wget -qO - https://qgis.org/downloads/qgis-2021.gpg.key | sudo gpg --no-default-keyring --keyring gnupg-ring:/etc/apt/trusted.gpg.d/qgis-archive.gpg --import

    $ sudo chmod a+r /etc/apt/trusted.gpg.d/qgis-archive.gpg

    $ sudo add-apt-repository "deb https://qgis.org/ubuntu $(lsb_release -c -s) main"

    $ sudo apt update

    $ sudo apt install qgis qgis-plugin-grass

## Mac OS

see [qgis.org download](https://qgis.org/en/site/forusers/download.html)

[Here](https://realpython.com/lessons/set-up-qgis/) is a video (2:30 to 3:40) which could help you installing QGIS
> Note: regarding QGIS, you should not worried about the python version

# Install and run django-weathervis

1. Create repo 'DJANGO_WEATHERVIS', and go in it:

        $ mkdir DJANGO_WEATHERVIS
        $ cd DJANGO_WEATHERVIS


2. <a name="py39"></a>Create a virtualenv, and activate it:
    Here I use conda, obviously you could use the virtualenv you are familiar with.

    I run on python 3.9, so to avoid issue when running it, you should do the same.
    First select python version you want to use

        $ conda create --name dj-weathervis python=3.9

    Activate the virtualenv

        $ conda activate dj-weathervis

3. <a name="git_dir"></a>Clone the github repo

        $ git clone https://github.com/julienpaul/django-weathervis.git <weathervis>

4. Install the required environment:

        $ cd <weathervis>
        $ pip install -r requirements/local.txt
        $ pre-commit install

5. Create a new PostgreSQL database using createdb:
    First check if PostgreSQL is running

        $ createdb
    > If PostgreSQL isn’t running, we’ll see an error message

    Create the 'weathervis' database

    5.1. Create a PostGIS database template

    > Note: you may need to run those command as superuser `sudo -u postgres`

        $ (sudo -u postgres) createdb template_postgis

        # Allows non-superusers the ability to create from this template
        $ (sudo -u postgres) psql -d postgres -c "UPDATE pg_database SET datistemplate='true' WHERE datname='template_postgis';"
        $ (sudo -u postgres) psql template_postgis -c "create extension postgis"
        $ (sudo -u postgres) psql template_postgis -c "create extension postgis_topology"

    > Warning: check <installdir> path before running:

        $ (sudo -u postgres) psql template_postgis -f <installdir>/postgresql/share/contrib/postgis-2.0/legacy.sql
    > for me it was here:
    >
        /usr/share/postgresql/13/contrib/postgis-3.1/legacy.sql

        # Enable users to alter spatial tables.
        $ (sudo -u postgres) psql -d template_postgis -c "GRANT ALL ON geometry_columns TO PUBLIC;"
        $ (sudo -u postgres) psql -d template_postgis -c "GRANT ALL ON geography_columns TO PUBLIC;"
        $ (sudo -u postgres) psql -d template_postgis -c "GRANT ALL ON spatial_ref_sys TO PUBLIC;"


    5.2. Finally create the 'weathervis' database with PostGIS support:

        $ createdb -T template_postgis weathervis

    > Warning: the database must be named `weathervis`

6. Update the database with the django models.
    in your <weathervis\> repository (created [above](#git_dir)):

        $ python manage.py migrate

7. Load database

    7.1 Create and Load model grid shape files

        $ python manage.py shell
        >>> from src.model_grids.util import upload
        >>> upload()
        >>> exit()

    7.2 Create and load station

        $ python manage.py shell
        >>> from src.stations.util import upload
        >>> upload()
        >>> exit()

    7.3 load other fixture

        $ python manage.py loaddata src/fixtures/**/*.json

8. Finally run the Django development server:

        $ python manage.py runserver

    Open in your browser http://127.0.0.1:8000

> Note: when creating a user, you will have to copy/paste the url from the email print on your terminal to "confirm" the user's email address.
