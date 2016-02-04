xivo-purge-db
=============
[![Build Status](https://travis-ci.org/xivo-pbx/xivo-purge-db.png?branch=master)](https://travis-ci.org/xivo-pbx/xivo-purge-db)

xivo-purge-db is a service for deleting (and optionally backup) old database entries on a XiVO server


Running unit tests
------------------

```
apt-get install libpq-dev python-dev libyaml-dev
pip install tox
tox --recreate -e py27
```


Running integration tests
-------------------------

You need Docker installed.

```
cd integration_tests
pip install -U -r test-requirements.txt
make test-setup
make test
```
