# simple-server-report

## Description
This is a simple script sending a mail with some status information.
I use it to monitor and maintain some of my hosts.

## Requirements
It runs with Python 3. It doesn't use any external libraries so every
standard Python 3 distribution should work. I tested it with
Python 3.2 & 3.5.

## Configuration and usage

The program is inteded to be used with cron or similar tool rather than running it manually.
Additionally it needs a `config.properites` placed in the root
directory of the application.
The file must have following properties:
```
# SMTP Server data, no default so you need to fill everything
# This MUST be a SSL connection
smtp_host=
smtp_port=

# SMTP Authorization
smtp_user=
smtp_password=
smtp_from=Your Name <your.name@provider.mail.com>
smtp_to=Comma <comma@mail>, Separated <separated@mail>

# CUPS Server settings, again no defaults
cups_host=
cups_port=
# URL you want to use, it may be main page or a printer page
# The content of the page will be included in a mail attachment
cups_url=

# Settings for IP checking. The config below will work fine
ip_api_host=api.ipify.org
ip_api_url=/
```

Then you can configure your cron (`crontab -e`) e. g.
```
0 18 * * * /home/pi/simple-server-report/ && python3 simple-report.py # send a report every day at 18:00
```

## Further improvements

For now it is bare (but good enough) minimum I needed. As a further step
I would like to add a few features (ordered by priority):

1. Process dump
2. Better error handling
3. Collecting report when regular report coudn't be sent
4. More flexible configuration
