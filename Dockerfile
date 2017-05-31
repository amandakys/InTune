FROM python:latest

WORKDIR /build/webapps34
ADD . /build/

RUN pip install -r /build/requirements.txt

EXPOSE 80

ENV NAME InTune

RUN ./manage.py test
# RUN ./manage.py collectstatic --noinput
RUN ./manage.py migrate

CMD uwsgi --ini /build/uwsgi.ini
