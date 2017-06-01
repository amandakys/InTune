FROM python:latest

WORKDIR /build/webapps34
ADD . /build/

RUN pip install -r /build/requirements.txt

EXPOSE 80

ENV NAME InTune

RUN ./manage.py test --settings=webapps34.deploy_settings
RUN ./manage.py collectstatic --noinput --settings=webapps34.deploy_settings
RUN ./manage.py migrate --settings=webapps34.deploy_settings

CMD uwsgi --ini /build/uwsgi.ini
