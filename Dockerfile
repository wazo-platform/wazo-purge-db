FROM debian:wheezy

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get -qq update
RUN apt-get -qq -y install apt-utils
RUN apt-get -qq -y install \
     git \
     libpq-dev \
     libyaml-dev \
     python \
     python-dev \
     python-pip

RUN mkdir -p /etc/xivo-purge-db/conf.d

RUN mkdir -p /var/run/xivo-purge-db
RUN chmod a+w /var/run/xivo-purge-db

RUN touch /var/log/xivo-purge-db.log
RUN chown www-data: /var/log/xivo-purge-db.log

ADD . /usr/src/xivo-purge-db
WORKDIR /usr/src/xivo-purge-db

RUN pip install -r requirements.txt
RUN pip install -r test-requirements.txt

RUN rsync -av etc/ /etc
RUN ./setup.py install

CMD xivo-purge-db
