FROM python:3.6

ADD . /ButterSalt

WORKDIR /ButterSalt

RUN mv config.py.simple config.py

RUN pip install -r requirements.txt

EXPOSE 5000

ENTRYPOINT ["python", "/ButterSalt/manage.py"]

CMD ["runserver", "-h", "0.0.0.0"]