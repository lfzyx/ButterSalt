FROM python:3.6

ADD . /ButterSalt

WORKDIR /ButterSalt

RUN mv config.py.simple config.py

RUN pip install -r requirements.txt

EXPOSE 5000

RUN echo \
"python /ButterSalt/manage.py db init\n"\
"python /ButterSalt/manage.py db migrate\n"\
"python /ButterSalt/manage.py db upgrade\n"\
"exit 0"\
> /etc/rc.local

ENTRYPOINT ["python", "/ButterSalt/manage.py"]

CMD ["runserver", "-h", "0.0.0.0"]