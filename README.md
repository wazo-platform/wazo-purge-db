wazo-purge-db
=============
[![Build Status](https://jenkins.wazo.community/buildStatus/icon?job=wazo-purge-db)](https://jenkins.wazo.community/job/wazo-purge-db)

wazo-purge-db is a service for deleting (and optionally backing up) old database entries on a Wazo server


Running unit tests
------------------

```
apt-get install libpq-dev python3-dev libyaml-dev
pip install tox
tox --recreate -e py39
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


Developing
----------

When you're developing, once you have done the setup above, you may run
integration tests faster with:

```
cd integration_tests
docker-compose run sync
docker-compose run purgedb  # repeat to run the tests against new code
```
