FROM wazopbx/wazo-purge-db

ADD . /usr/src/wazo-purge-db
WORKDIR /usr/src/wazo-purge-db

RUN pip install -Ur requirements.txt
RUN pip install -Ur integration_tests/requirements.txt
RUN python setup.py develop

WORKDIR contribs/sample-plugin
RUN python setup.py install

WORKDIR /usr/src/wazo-purge-db
RUN cp -r etc/wazo-purge-db /etc

CMD ["pytest", "integration_tests/suite"]
