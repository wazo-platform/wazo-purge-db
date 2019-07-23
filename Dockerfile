FROM python:3.5-stretch

RUN mkdir -p /etc/wazo-purge-db/conf.d

RUN mkdir -p /var/run/wazo-purge-db
RUN chmod a+w /var/run/wazo-purge-db

RUN touch /var/log/wazo-purge-db.log
RUN chown www-data: /var/log/wazo-purge-db.log

ADD . /usr/src/wazo-purge-db
WORKDIR /usr/src/wazo-purge-db

RUN pip install -r requirements.txt

RUN cp -r etc/ /etc
RUN ./setup.py install

CMD ["wazo-purge-db"]
