FROM wazoplatform/wazo-purge-db

ENV PYTHONDONTWRITEBYTECODE='true'

COPY . /usr/src/wazo-purge-db
WORKDIR /usr/src/wazo-purge-db

RUN pip install -Ur requirements.txt
RUN pip install -Ur integration_tests/requirements.txt
RUN python3 -m pip install -e .

WORKDIR contribs/sample-plugin
RUN python3 -m pip install .

WORKDIR /usr/src/wazo-purge-db
RUN cp -r etc/wazo-purge-db /etc

CMD ["pytest", "-v", "-s", "-p", "no:cacheprovider", "integration_tests/suite"]
