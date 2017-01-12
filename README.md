# ButterSalt

ButterSalt is a GUI Devops tool based on the SaltStack [netapi.rest_cherrypy](https://docs.saltstack.com/en/latest/ref/netapi/all/salt.netapi.rest_cherrypy.html)

需要在 master 的配置文件中添加以下的配置项：

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