# ButterSalt

[![Build Status](https://travis-ci.org/lfzyx/ButterSalt.svg?branch=master)](https://travis-ci.org/lfzyx/ButterSalt)

ButterSalt is a GUI Devops tool based on the SaltStack [netapi.rest_cherrypy](https://docs.saltstack.com/en/latest/ref/netapi/all/salt.netapi.rest_cherrypy.html)

ButterSalt uses the [flask](http://flask.pocoo.org) web framework

A full-access access for linux user lfzyx need to add the following configuration items to the /etc/salt/master configuration file：:

<pre>
external_auth:
  pam:
    lfzyx:
        - .*
        - '@runner'
        - '@wheel'

rest_cherrypy:
  port: 8000
  disable_ssl: True
</pre>

> You need to replace the lfzyx with the user on the salt-master server

## Install

`git clone https://github.com/lfzyx/ButterSalt.git`

`pip3 install -r requirements.txt`

edit the config.py and modify the SALT_API option to you salt api address

`python3 manage.py runserver`


## Docker

`docker pull lfzyx/buttersalt`

`docker run --env DASHBOARD_ADMIN=USERNAME:PASSWD --env SALT_API_URI=http://Pam-USERNAME:Pam-PASSWD@URL:PORT -p 5000:5000 lfzyx/buttersalt`


