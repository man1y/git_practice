Provisoning a new site
======================

## Required packages:
* nginx
* Python 3.10
* venv + pip
* Git
eg, on Ubuntu:
  sudo apt-get install nginx git python3.10-venv

## Nginx Virtual Host config
* see nginx.template.conf
* replace SITENAME with, e.g., staging.mydomain.com

## Systemd service
* see gunicorn-systemd.template.service
* replace SITENAME with, e.g., staging.mydomain.com

## Folder structure:
Assume we have a user account at /home/username

/home/username
└── sites
    └── superlists-staging.manly.org
        ├── database
        ├── source
        ├── static
        └── venv
