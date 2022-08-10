> Based on https://simpleisbetterthancomplex.com/series/2017/10/16/a-complete-beginners-guide-to-django-part-7.html

Upfront we will have **web server**. The web server will receive all requests to the server. But it won’t try to do anything smart with the request data. All it is going to do is decide if the requested information is a static asset that it can serve by itself, or if it’s something more complicated. If so, it will pass the request to **Web Server Gateway Interface (WSGI)**.

The **web server** will also be configured with **HTTPS certificates**. Meaning it will only accept requests via HTTPS. If the client tries to request via HTTP, the web server will first redirect the user to the HTTPS, and only then it will decide what to do with the request.

**The Web Server Gateway Interface (WSGI)** is an application server. Depending on the number of processors the server has, it can spawn multiple workers to process multiple requests in parallel. It manages the workload and executes the Python and Django code.

**Django** is the one doing the hard work. It may access the database (PostgreSQL) or the file system. But for the most part, the work is done inside the views, rendering templates. After Django process the request, it returns a response to Gunicorn, who returns the result to the Web Server that will finally deliver the response to the client.

We are also going to install **PostgreSQL**, a production quality database system. Because of Django’s ORM system, it’s easy to switch databases.

The last step is to install a **process control system**. It will keep an eye on the WSGI and Django to make sure everything runs smoothly. If the server restarts, or if WSGI crashes, it will automatically restart it.

# Domain Name
Your domain name is the address for your website.
It’s important to have a domain name to serve the application, configure an email service and configure an https certificate.

- IT create domain name **weathervis.uib.no**

# Prepare the server (centos)
### update(s) (as root)
~~~bash
sudo dnf check-update
sudo dnf -y upgrade
~~~

<!--
~~~bash
sudo apt-get update
sudo apt-get -y upgrade
~~~
-->
> **NOTE:**
> If you get any prompt during the upgrade, select the option “keep the local version currently installed”.

> **NOTE:**
> `Error: Failed to download metadata for repo ‘appstream’`
> If you get this error, you have to migrate from CentOS 8 to CentOS Stream 8, run the following commands:
> ~~~bash
> dnf --disablerepo '*' --enablerepo=extras swap centos-linux-repos centos-stream-repos
> dnf distro-sync
> ~~~
>
> see https://haydenjames.io/fix-error-failed-to-download-metadata-for-repo-appstream-centos-8/


## <a name="py39"></a>Python 3.X (If not already installed)
### install (as root)
~~~bash
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt-get update
sudo apt-get install python3.X
~~~

## Virtual env (If not already installed)
> **NOTE:**
> Here I use conda, obviously you could use the virtualenv you are familiar with.

### Conda
First check conda channels

~~~bash
conda config --show channels
~~~

If need be add conda-forge channel
~~~bash
conda config --add channels conda-forge
conda config --set channel_priority strict
~~~

Create python 3.9 env
~~~bash
conda create -n dj-weathervis python=3.9
~~~

Activate this environment
~~~bash
conda activate dj-weathervis
~~~

<!--
### Virtualenv
~~~bash
wget https://bootstrap.pypa.io/get-pip.py
sudo python3.X get-pip.py
sudo pip3.X install virtualenv
~~~
-->

## Web Server: Apache
### install (as root)

Update the local Apache httpd package index to reflect the latest upstream changes:
~~~bash
sudo dnf update httpd
~~~

Once the packages are updated, install the Apache package:
~~~bash
sudo dnf install httpd
~~~

### Checking your Web Server
Apache does not automatically start on CentOS once the installation completes. You will need to start the Apache process manually:
~~~bash
sudo systemctl start httpd
~~~

Verify that the service is running with the following command:
~~~bash
sudo systemctl status httpd
~~~

You will see an active status when the service is running
However, the best way to test this is to request a page from Apache.
You can access the default Apache landing page to confirm that the software is running properly through your IP address. If you do not know your server’s IP address, you can get it a few different ways from the command line.

Type this at your server’s command prompt:
~~~bash
hostname -I
~~~

This command will display all of the host’s network addresses, so you will get back a few IP addresses separated by spaces. You can try each in your web browser to see if they work.

When you have your server’s IP address, enter it into your browser’s address bar:
~~~bash
http://your_server_ip
~~~

You’ll see the default CentOS 8 Apache web page


To stop your web server, type:
~~~bash
sudo systemctl stop httpd
~~~

see also https://www.digitalocean.com/community/tutorials/how-to-install-the-apache-web-server-on-centos-7

<!--
> **NOTE:**
> on Ubuntu
> ~~~bash
> sudo apt-get install apache2
> ~~~
-->

<!--
## Web Server: Nginx
### install (as root)

~~~bash
sudo apt-get -y install nginx
~~~
-->

## Supervisor
### install (as root)
<!-- https://cloudwafer.com/blog/installing-supervisor-on-centos-8/ -->
~~~bash
sudo dnf update -y
sudo dnf install epel-release

sudo dnf update
sudo dnf -y install supervisor

sudo systemctl start supervisord
sudo systemctl enable supervisord

sudo systemctl status supervisord
~~~

To stop supervisor
~~~bash
sudo systemctl stop supervisord
~~~

> **NOTE:**
> If you get `Failed to enable unit`, try reboot the server
> ~~~bash
> sudo reboot
> ~~~

<!--
> **NOTE:**
> on Ubuntu
> ```bash
> sudo apt-get -y install supervisor
>
> sudo systemctl enable supervisor
> sudo systemctl start supervisor
> ```
-->

## DataBase
### Install PostgreSQL (as root)
Log into your system and update the system software packages using the following apt command.
~~~bash
sudo dnf check-update
sudo dnf -y upgrade
~~~

<!-- https://www.centlinux.com/2021/10/install-postgis-for-postgresql-on-centos-rhel-8.html -->

Install the repository RPM:
~~~bash
sudo dnf install -y https://download.postgresql.org/pub/repos/yum/reporpms/EL-8-x86_64/pgdg-redhat-repo-latest.noarch.rpm
~~~

Disable the built-in PostgreSQL module:
~~~bash
sudo dnf -qy module disable postgresql
~~~

Install PostgreSQL:
~~~bash
sudo dnf install -y postgresql14-server
sudo dnf install -y postgresql14-devel
~~~

Initialize the PostgreSQL database server.
~~~bash
sudo /usr/pgsql-14/bin/postgresql-14-setup initdb
~~~

Enable and start PostgreSQL database service.
~~~bash
sudo systemctl enable --now postgresql-14
~~~

Verify the version of your PostgreSQL database.
~~~bash
psql -V
~~~

After PostgreSQL installed, you can confirm that the PostgreSQL service is active, running and is enabled under systemd using the following systemctl commands:
~~~bash
sudo systemctl start postgresql-14
sudo systemctl is-active postgresql-14
sudo systemctl is-enabled postgresql-14
sudo systemctl status postgresql-14
~~~

> **NOTE:**
> To stop
> ~~~bash
> sudo systemctl stop postgresql-14
> ~~~

Also, confirm that the Postgresql server is ready to accept connections from clients as follows:
~~~bash
pg_isready
~~~

> **NOTE:**
> you may need to add pgsql path to the environment variable **PATH**
> ~~~bash
> find / -name pg_isready
> ~~~
> in your **.bashrc**
> ~~~bash
> MY_BIN_PATH=/usr/pgsql-14/bin/
> [ ! -z "${PATH##*${MY_BIN_PATH}*}" ] && export PATH=$PATH:$MY_BIN_PATH
> ~~~

### Install PostGIS (as root)
Some of the required packages by PostGIS are not available in standard and PostgreSQL yum repositories, therefore, you are required to install EPEL (Extra Packages for Enterprise Linux) yum repository.

~~~bash
sudo dnf install -y https://dl.fedoraproject.org/pub/epel/epel-release-latest-8.noarch.rpm
~~~

You also need to enable PowerTools repository.

For CentOS / Rocky Linux you can execute following command to enable PowerTools repository.

~~~bash
sudo dnf -y config-manager --set-enabled PowerTools
~~~

> **NOTE:**
> Running ```dnf repolist all``` will show you all the repos on your system, including the disabled ones.
> Then you can copy/paste the exact repo id.
> If you are fully updated on CentOS Stream, the command should be:
> ~~~bash
> sudo dnf config-manager --set-enabled powertools
> ~~~

Build cache for newly installed yum repositories.

~~~bash
sudo dnf makecache
~~~

Now, you can install PostGIS extension on you PostgreSQL server. There are many versions of PostGIS available in PostgreSQL yum repository.
Choose the version that matches your database version.

~~~bash
sudo dnf install -y postgis32_14
~~~

Check packages
~~~bash
rpm -qa | grep postg
~~~

> **See also**
> you could also have a look in [postgresql.org download](https://www.postgresql.org/download/)

### install QGIS (as root)
Actually we need to install GDAL, GEOS, PROJ.4.
You can installed them individually, or installed QGIS which installed all those libraries as we do here.

~~~bash
sudo dnf check-update
sudo dnf -y upgrade
~~~
<!--
https://courses.neteler.org/qgis-2-10-rpms-for-fedora-21-centos-7-scientific-linux-7/
https://download.qgis.org/en/site/forusers/alldownloads.html#qgis-ltr-long-term-release
https://copr.fedorainfracloud.org/coprs/mlampe/qgis-ltr/
-->

~~~bash
sudo dnf install epel-release
sudo dnf update
sudo wget -O /etc/yum.repos.d/mlampe-qgis-lt-epel-8.repo https://copr.fedorainfracloud.org/coprs/mlampe/qgis-ltr/repo/epel-8/mlampe-qgis-ltr-epel-8.repo

sudo dnf update
sudo dnf install qgis qgis-grass qgis-python
~~~

### install Postfix mail (as root)

Check whether Sendmail is installed on your system.
If Sendmail is already installed, remove it.
~~~bash
rpm -qa | grep sendmail

sudo dnf remove sendmail
~~~

Update Your System
~~~bash
sudo dnf check-update
sudo dnf -y upgrade
~~~

Install Postfix
~~~bash
sudo dnf install postfix
~~~

Enable Postfix Services
~~~bash
rpm -qa|grep postfix

sudo systemctl enable postfix
sudo systemctl start postfix
sudo systemctl status postfix
~~~

Install mailx Email Client
~~~bash
sudo dnf install mailx -y
~~~

Check mail command version
~~~bash
mail -V
~~~

Send a Test email using mail command in Linux
~~~bash
echo "This is test email" | mail -s "Test Email" <your-mail@example.com>
~~~


## DJANGO_WEATHERVIS
### <a name="git_repo"></a>Install django-weathervis (as application user -**centos**-)
Create repo **<DJANGO_WEATHERVIS>**:

> **Exemple:**
> ~~~bash
> <DJANGO_WEATHERVIS>=/home/centos/DJANGO_WEATHERVIS/
> ~~~

~~~bash
mkdir -p <DJANGO_WEATHERVIS>
cd <DJANGO_WEATHERVIS>
~~~

Make sure, the virtualenv is activate
~~~bash
conda activate dj-weathervis
~~~

Install release X.X.X of django-weathervis directly from github repo
~~~bash
cd <DJANGO_WEATHERVIS>
pip3 install -e git+https://github.com/julienpaul/django-weathervis.git@0.1.0#egg=django-weathervis
~~~

The django code should be in **<DJANGO_WEATHERVIS>/src/django-weathervis**

Check version
~~~bash
pip show django-weathervis
~~~

> **Note:**
> Alternatively you could clone the github repo
> ~~~bash
> git clone --depth 1 --branch <tag_name> https://github.com/julienpaul/django-weathervis.git <DJANGO_WEATHERVIS>/src/django-weathervis
> ~~~

Install the required environment:
~~~bash
cd <DJANGO_WEATHERVIS>/src/django-weathervis
pip install -r requirements.txt
~~~

# Setup

## Database Setup (as root)
Switch to the postgres user:
~~~bash
sudo su - postgres
~~~

Create a PostGIS database template
~~~bash
createdb template_postgis

# Allows non-superusers the ability to create from this template
psql -d postgres -c "UPDATE pg_database SET datistemplate='true' WHERE datname='template_postgis';"
psql template_postgis -c "create extension postgis"
psql template_postgis -c "create extension postgis_topology"
~~~

> Warning: check <installdir> path before running:
> ~~~bash
>  find /usr/ -name legacy.sql
>  $ /usr/pgsql-14/share/contrib/postgis-3.2/legacy.sql
> ~~~

~~~bash
psql template_postgis -f <installdir>/postgis-3.2/legacy.sql
~~~

Enable users to alter spatial tables.
~~~bash
psql -d template_postgis -c "GRANT ALL ON geometry_columns TO PUBLIC;"
psql -d template_postgis -c "GRANT ALL ON geography_columns TO PUBLIC;"
psql -d template_postgis -c "GRANT ALL ON spatial_ref_sys TO PUBLIC;"
~~~

Create a database user:
~~~bash
createuser u_weathervis
~~~
Create a new database and set the user as the owner:
~~~bash
createdb -T template_postgis weathervis --owner u_weathervis
~~~
Define a strong password for the user:
~~~bash
psql -c "ALTER USER u_weathervis WITH PASSWORD '<YOUR_PASSWORD>'"
~~~
> **Tips:**
> Save your password in a password manager like Bit Warden

We can now exit the postgres user:
~~~bash
exit
~~~

## Django Project Setup

Switch to the application user:
~~~bash
sudo su - centos
~~~

First, we can check where we are:
~~~bash
pwd
/home/centos
~~~

We use a **.env** file to store the database credentials, the secret key and other configuration parameters:
~~~bash
export DJANGO_READ_DOT_ENV_FILE=True
export DJANGO_WEATHERVIS_CFG_PATH=/home/centos/.config/django-weathervis/
~~~

Now let's create this file. You find a template **.env.dist** in **ROOT_DIR**.
> **Note:**
> Most of those parameters will use default value if not set up.

Generate Django SECRET_KEY, and copy it in the **.env** file:
~~~python
from django.core.management.utils import get_random_secret_key
SECRET_KEY = get_random_secret_key()
~~~
> **Tips:**
> Save your secret key in a password manager like Bit Warden

You will need at least those parameters in the **.env** file:
~~~bash
DJANGO_SECRET_KEY=<YOUR_SECRET_KEY>
DATABASE_URL=postgis://u_weathervis:<YOUR_PASSWORD>@localhost:5432/weathervis
REDIS_URL=redis://127.0.0.1:6379/1
DJANGO_DADMINS=[("""Julien Paul""", "julien.paul@uib.no")]
DJANGO_ALLOWED_HOSTS=.weathervis.uib.no,localhost,127.0.0.1
DJANGO_ACCOUNT_ALLOW_REGISTRATION=False
DJANGO_SECURE_SSL_REDIRECT=False
DJANGO_ADMIN_URL='admin/'
~~~


Migrate the database with the django models.
in your **<DJANGO_WEATHERVIS>/src/django-weathervis** repository (created [above](#git_repo)):
~~~bash
export DJANGO_SETTINGS_MODULE='config.settings.production'
python manage.py migrate
~~~

Migrate the static files:
~~~bash
python manage.py collectstatic
~~~

Create a super user for the application:
~~~bash
python manage.py createsuperuser
~~~
> **Tips:**
> Save your password in a password manager like Bit Warden

## Configuring Gunicorn
Gunicorn is the one responsible for executing the Django code behind a proxy server.

Create a new file named **gunicorn_start** inside **<DJANGO_WEATHERVIS>**:
~~~bash
#!/bin/bash

NAME="django_weathervis"
DIR=<DJANGO_WEATHERVIS>/src/django-weathervis
USER=centos
GROUP=centos
WORKERS=1
# BIND=unix:<DJANGO_WEATHERVIS>/run/gunicorn.sock
BIND=127.0.0.1:8000
DJANGO_SETTINGS_MODULE=config.settings.production
DJANGO_WSGI_MODULE=config.wsgi
LOG_LEVEL=error

# load .bashrc
source ~/.bashrc

cd $DIR
conda activate dj-weathervis

export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DIR:$PYTHONPATH

exec gunicorn ${DJANGO_WSGI_MODULE}:application \
  --name $NAME \
  --workers $WORKERS \
  --user=$USER \
  --group=$GROUP \
  --bind=$BIND \
  --log-level=$LOG_LEVEL \
  --log-file=-
~~~

This script will start the application server. We are providing some information such as where the Django project is, which application user to be used to run the server, and so on.

Now make this file executable:

~~~bash
chmod u+x gunicorn_start
~~~

Create two empty folders inside **<DJANGO_WEATHERVIS>**, one for the socket file and one to store the logs:
~~~bash
mkdir -p run logs
~~~

Check Gunicorn
~~~bash
cd <DJANGO_WEATHERVIS>/src/django-weathervis
gunicorn --bind 0.0.0.0:8000 config.wsgi:application
~~~

You will see
~~~bash
[2021-09-08 15:20:17 +0000] [12789] [INFO] Starting gunicorn 20.1.0
[2021-09-08 15:20:17 +0000] [12789] [INFO] Listening at: http://0.0.0.0:8000 (12789)
[2021-09-08 15:20:17 +0000] [12789] [INFO] Using worker: sync
[2021-09-08 15:20:17 +0000] [12791] [INFO] Booting worker with pid: 12791
~~~
which means you have successfully bonded your gunicorn to run your Django app.

<!--
To test out success you can type in your IP with port :8000 and see your application run.
you may have a UFW firewall protecting your server. In order to test the development server, we’ll have to allow access to the port we’ll be using.
Create an exception for port 8000 by typing:
~~~bash
sudo ufw allow 8000
~~~

To Delete Firewall Rules
~~~bash
sudo ufw delete allow 8000
~~~

> **Note:**
> To install UFW:
> ~~~bash
> sudo dnf install epel-release -y
>
> # install
> sudo dnf install ufw -y
>
> # enable
> sudo ufw enable
> ~~~
> Check the status of UFW:
> ~~~bash
> sudo ufw status
> ~~~
> To disable UFW, you’ve to run this command:
> ~~~bash
> sudo ufw disable
> ~~~
-->
<!-- https://shouts.dev/articles/install-and-setup-ufw-firewall-on-centos-8-rhel-8 -->

## Configuring Supervisor
First, create an empty log file inside the **<DJANGO_WEATHERVIS>**/logs/ folder:

~~~bash
touch logs/gunicorn.log
~~~

Now create a new supervisor file:
~~~bash
# sudo vim /etc/supervisor/conf.d/django_weathervis.conf
sudo vim /etc/supervisord.d/supervisord.ini
~~~

~~~bash
[program:django_weathervis]
command=<DJANGO_WEATHERVIS>/gunicorn_start
user=centos
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=<DJANGO_WEATHERVIS>/logs/gunicorn.log
~~~

Save the file and run the commands below:

~~~bash
sudo supervisorctl start django_weathervis
# sudo supervisorctl reread
# sudo supervisorctl update
~~~

Now check the status:

~~~bash
sudo supervisorctl status django_weathervis

$ django_weathervis                       RUNNING   pid 308, uptime 0:00:07
~~~

If the systemctl status command indicated that an error occurred or if you do not find the myproject.sock file in the directory, it’s an indication that Gunicorn was not able to start correctly. Check the Gunicorn process logs by typing:

~~~bash
sudo journalctl -u gunicorn
~~~


## Configuring Apache

<!-- https://medium.com/django-deployment/how-to-setup-apache-with-gunicorn-6616986f1702 -->
<!--
> **Note:**
> we may need to add two folders
> - **sites-available**
> - **sites-enabled**
> ~~~bash
> sudo mkdir /etc/httpd/sites-available /etc/httpd/sites-enabled
> ~~~
> and edit the configuration file **/etc/httpd/conf/httpd.conf**
> ~~~bash
> # Load config from sites-enabled directory
> IncludeOptional sites-enabled/*.conf
> ~~~

Create **/etc/httpd/sites-available/weathervis.conf**
~~~bash
<VirtualHost *:80>
    ServerName weathervis.uib.no

    ProxyPass /static/ !
    ProxyPass /media/ !
    ProxyRequests off
    ProxyPreserveHost off

    ProxyPass / http://127.0.0.1:8000/
    ProxyPassReverse / http://127.0.0.1:8000/

    Alias /static /home/centos/DJANGO-WEATHERVIS/src/django-weathervis/staticfiles
    <Directory /home/centos/DJANGO-WEATHERVIS/src/django-weathervis/staticfiles>
      Require all granted
    </Directory>

    Alias /media /home/centos/Code/DJANGO_WEATHERVIS/src/django-weathervis/src/media
    <Directory /home/centos/Code/DJANGO_WEATHERVIS/src/django-weathervis/src/media>
      Require all granted
    </Directory>

    LogLevel warn
    ErrorLog /var/www/weathervis/log/error.log
    CustomLog /var/www/weathervis/log/requests.log combined
</VirtualHost>
~~~

Create link to **/etc/httpd/sites-enabled**
~~~bash
cd /etc/httpd/sites-enabled
ln ../sites-available/weathervis.conf .
~~~
-->

Save default confifugration file
~~~bash
cd /etc/httpd/
mkdir -p conf.d.bak
mv conf.d/* conf.d.bak/.
~~~

Create **/etc/httpd/conf.d/weathervis.conf**
~~~bash
<VirtualHost *:80>
    ServerName weathervis.uib.no

    ProxyPass /static/ !
    ProxyPass /media/ !
    ProxyRequests off
    ProxyPreserveHost off

    ProxyPass / http://127.0.0.1:8000/
    ProxyPassReverse / http://127.0.0.1:8000/

    Alias /static /home/centos/Code/DJANGO_WEATHERVIS/src/django-weathervis/staticfiles
    <Directory /home/centos/Code/DJANGO_WEATHERVIS/src/django-weathervis/staticfiles>
      Require all granted
    </Directory>

    Alias /media /home/centos/Code/DJANGO_WEATHERVIS/src/django-weathervis/src/media
    <Directory /home/centos/Code/DJANGO_WEATHERVIS/src/django-weathervis/src/media>
      Require all granted
    </Directory>

    LogLevel warn
    ErrorLog /var/www/weathervis/log/error.log
    CustomLog /var/www/weathervis/log/requests.log combined
</VirtualHost>
~~~


Create log folder
~~~bash
mkdir -p /var/www/weathervis/log

# change security context
chcon -t httpd_sys_rw_content_t /var/www/weathervis
~~~

Re-run Apache
~~~bash
apachectl graceful
~~~

Make file from **staticfiles** and **media** are readable
~~~bash
cd <DJANGO_WEATHERVIS>/src/django-weathervis
chcon --user system_u --type httpd_sys_content_t -Rv staticfiles
cd <DJANGO_WEATHERVIS>/src/django-weathervis/src
chcon --user system_u --type httpd_sys_content_t -Rv media
~~~

Check log file **/var/www/weathervis/log/error.log**
If you get this error
~~~bash
[Wed Mar 30 13:41:29.126168 2022] [proxy:error] [pid 118176:tid 140598723974912] (13)Permission denied: AH00957: HTTP: attempt to connect
 to 127.0.0.1:8000 (127.0.0.1) failed
[Wed Mar 30 13:41:29.126225 2022] [proxy_http:error] [pid 118176:tid 140598723974912] [client 78.188.166.132:41936] AH01114: HTTP: failed
 to make connection to backend: 127.0.0.1
~~~
you may fix it with:
~~~bash
/usr/sbin/setsebool -P httpd_can_network_connect 1
~~~

## check fonts
~~~bash
fc-list
~~~

Download fonf-family from https://fonts.google.com/
~~~bash
sudo mkdir -p /usr/local/share/fonts/<font-family>
sudo cp -v <font>.zip /usr/local/share/fonts/<font-family>/.
~~~

Rebuild the font cache
~~~bash
cd /usr/local/share/fonts/<font-family>
sudo unzip <font>.zip
sudo fc-cache -v
~~~

## Configuring HTTPS Certificate
<!-- https://letsencrypt.org/getting-started/ -->
go to https://certbot.eff.org/ and follow the instructions

## Check
Verify Apache is running:
~~~bash
sudo systemctl status httpd
~~~

Verify Postfix is running:
~~~bash
sudo systemctl status postfix
~~~

Verify Supervisor is running:
~~~bash
sudo systemctl status supervisord
~~~

Verify Gunicorn is running (Superivsor should be running):
~~~bash
sudo supervisorctl status django_weathervis
~~~

## Load database
~~~bash
cd <DJANGO_WEATHERVIS>/src/django-weathervis/

export DJANGO_SETTINGS_MODULE=config.settings.production
~~~

Create user's groups with permission
~~~bash
python manage.py create_groups
~~~

Create and load model grid shape files
~~~bash
python manage.py shell
>>> from src.model_grids.util import upload
>>> upload()
>>> exit()
~~~

Create and load stations
~~~bash
python manage.py shell
>>> from src.stations.util import upload
>>> upload()
>>> exit()
~~~

Create and load domains
~~~bash
python manage.py shell
>>> from src.domains.util import upload
>>> upload()
>>> exit()
~~~

Load other fixtures
~~~bash
python manage.py loaddata src/fixtures/**/*.json
~~~

# Synchronize

The django-weathervis webpage must be synchronized with the weathervis software to work properly.
> **Note:**
>  The weathervis software is running on another server (centos_calc)

The weathervis software uses the **sites.yaml** file created from the django-weathervis station database.
Create **bin/push_to_centos_calc.sh**, to push this file to centos_calc
~~~bash
#!/usr/bin/bash

# set up
centos_calc=158.39.77.94
centos_serve=158.39.201.233

remote_dir=/home/centos/progs/islas/weathervis/weathervis/data
local_dir=/home/centos/DJANGO-WEATHERVIS/src/django-weathervis/src/stations/data

# push sites.yaml into islas/weathervis/weathervis/data/sites.yaml (centos_calc)
rsync -az --stats -e "ssh -i /home/centos/.ssh/islas-key.pem" ${local_dir}/stations.yaml ${centos_calc}:${remote_dir}/sites.yaml
~~~

> **Note:**
> the file **stations.yaml** is updated each time a station is changed or created
> on the database, and renamed to **sites.yaml** when push on centos_calc.


The django-weathervis uses plots created by the weathervis software.
Create **bin/pull_from_centos_calc.sh** to pull plots from centos_calc to django-weathervis server
~~~bash
#!/usr/bin/bash

# set up
centos_calc=158.39.77.94
centos_serve="158.39.201.233"

remote_dir="/home/centos/www/gfx"
local_dir="/home/centos/DJANGO-WEATHERVIS/src/django-weathervis/src/media"

# pull gfx folder (from centos_calc) into media/weathervis
rsync -az --stats --delete --exclude='home' -e "ssh -i /home/centos/.ssh/islas-key.pem" ${centos_calc}:${remote_dir} ${local_dir}
~~~

To update the django-weathervis database, after synchronized **gfx** folder, we need to run:
~~~bash
python /home/centos/DJANGO-WEATHERVIS/src/django-weathervis/manage.py update_plot
~~~

To do all this regularly we use **crontab**
~~~bash
SHELL=/bin/bash
BASH_ENV=~/.bashrc_conda
MAILTO=juliem.paul@uib.no

# Example of job definition:
# m h dom mon dow   command

# * * * * *  command to execute
# ┬ ┬ ┬ ┬ ┬
# │ │ │ │ │
# │ │ │ │ │
# │ │ │ │ └───── day of week (0 - 6) (Sunday=0 or 7) OR sun,mon,tue,wed,thu,fri,sat
# │ │ │ └────────── month (1 - 12)
# │ │ └─────────────── day of month (1 - 31)
# │ └──────────────────── hour (0 - 23)
# └───────────────────────── min (0 - 59)

# Note: log are stored in /var/log/cron
# -----

# For details see man 4 crontabs

# every hours (at :00), pull plots from centos_calc:
00 * * * * /home/centos/bin/pull_from_centos_calc.sh

# every hours (at :05), pull plots from centos_calc:
05 * * * * conda activate dj-weathervis; python /home/centos/DJANGO-WEATHERVIS/src/django-weathervis/manage.py update_plot

# every hours (at :00), push sites.yaml to centos_calc:
00 * * * * /home/centos/bin/push_to_centos_calc.sh
~~~

> **Note:**
> To update the django-weathervis database, we first need to activate conda environment.
> Sourcing **~/.bashrc** in **crontab** won't work as the file will not be running
> interactively. Which means that the conda snippet will never get executed.
> To solve this, create **~/.bashrc_conda**
> ~~~bash
> # >>> conda initialize >>>
> # !! Contents within this block are managed by 'conda init' !!
> __conda_setup="$('/home/centos/miniconda3/bin/conda' 'shell.bash' 'hook' 2> /dev/null)"
> if [ $? -eq 0 ]; then
>     eval "$__conda_setup"
> else
>     if [ -f "/home/centos/miniconda3/etc/profile.d/conda.sh" ]; then
>         . "/home/centos/miniconda3/etc/profile.d/conda.sh"
>     else
>         export PATH="/home/centos/miniconda3/bin:$PATH"
>     fi
> fi
> unset __conda_setup
> # <<< conda initialize <<<
>
> export DJANGO_READ_DOT_ENV_FILE=True
> export DJANGO_WEATHERVIS_CFG_PATH=/home/centos/.config/django-weathervis/
> export DJANGO_SETTINGS_MODULE=config.settings.production
> ~~~
> We also export few variables needed by django-weathervis.
