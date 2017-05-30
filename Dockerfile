FROM python:latest

WORKDIR /webapps34
ADD . /webapps34

RUN pip --install -r requirements.txt

EXPOSE 80

ENV NAME InTune

RUN /webapps34/manage.py collectstatic --noinput
RUN /webapps34/manage.py migrate

CMD ["uwsgi", "--ini uwsgi.ini"]
