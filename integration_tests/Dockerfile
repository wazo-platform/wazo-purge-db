FROM xivo/xivo-purge-db

ADD . /usr/src/xivo-purge-db
WORKDIR /usr/src/xivo-purge-db

RUN pip install -r requirements.txt
RUN pip install -r test-requirements.txt
RUN python setup.py install

WORKDIR contribs/sample-plugin
RUN python setup.py install

WORKDIR /usr/src/xivo-purge-db
RUN cp -r etc/ /etc

CMD nosetests integration_tests/suite
