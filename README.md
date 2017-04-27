# ButterSalt

ButterSalt is a GUI Devops tool based on the SaltStack [netapi.rest_cherrypy](https://docs.saltstack.com/en/latest/ref/netapi/all/salt.netapi.rest_cherrypy.html)

ButterSalt uses the [flask](http://flask.pocoo.org) web framework

![Image of saltpad](https://cloud.githubusercontent.com/assets/1881869/25473240/3f825e4c-2b61-11e7-9a48-63f52dcea1e3.png)

A full-access access for user lfzyx need to add the following configuration items to the /etc/salt/master configuration file：:

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

`python3 run.py`

## Initializing the database

Open up a Python terminal in our repository root.

`from ButterSalt import db`

`db.create_all()`