FROM python:latest

WORKDIR /build/webapps34
ADD . /build/

RUN apt-get update
RUN apt-get install -y redis-server
RUN wget https://bootstrap.pypa.io/get-pip.py
RUN python2.7 get-pip.py
RUN pip2.7 install supervisor
RUN pip3 install -r /build/requirements.txt

EXPOSE 80

ENV NAME InTune

RUN ./manage.py test
RUN ./manage.py collectstatic --noinput --settings=webapps34.deploy_settings
RUN ./manage.py migrate --settings=webapps34.deploy_settings

CMD supervisord -c /build/supervisord.conf
