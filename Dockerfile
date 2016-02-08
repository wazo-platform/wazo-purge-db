FROM python:2.7.9

RUN mkdir -p /etc/xivo-purge-db/conf.d

RUN mkdir -p /var/run/xivo-purge-db
RUN chmod a+w /var/run/xivo-purge-db

RUN touch /var/log/xivo-purge-db.log
RUN chown www-data: /var/log/xivo-purge-db.log

ADD . /usr/src/xivo-purge-db
WORKDIR /usr/src/xivo-purge-db

RUN pip install -r requirements.txt

RUN cp -r etc/ /etc
RUN ./setup.py install

CMD ["xivo-purge-db"]
