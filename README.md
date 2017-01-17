# ButterSalt

ButterSalt is a GUI Devops tool based on the SaltStack [netapi.rest_cherrypy](https://docs.saltstack.com/en/latest/ref/netapi/all/salt.netapi.rest_cherrypy.html)

You need to add the following configuration items to the /etc/salt/master configuration file：

<pre>
external_auth:
  pam:
    test:
        - .*
        - '@runner'
        - '@wheel'

rest_cherrypy:
  port: 8000
  disable_ssl: True
</pre>