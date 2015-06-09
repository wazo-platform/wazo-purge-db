xivo-purge-db
=============
[![Build Status](https://travis-ci.org/xivo-pbx/xivo-purge-db.png?branch=master)](https://travis-ci.org/xivo-pbx/xivo-purge-db)

xivo-purge-db is a service for deleting (and optionally backup) old database entries on a XiVO server

## Testing

xivo-purge-db contains unittests and integration tests

### unittests

Dependencies to run the unittests are in the `test-requirements.txt` file.

    % pip install -r requirements.txt -r test-requirements.txt

To run the unittests

    % nosetests xivo_purge_db

### Integration tests

You need:

- docker

A docker image named `xivo-purge-db-test` is required to execute the test suite.
To build this image execute:

    % cd integration_tests
    % make test-setup
    % make test-image

There are two steps in preparing the integration tests:

- `make test-setup`: time consuming, but only needs to be run when
  dependencies of xivo-purge-db change in any way.
- `make test-image`: a lot faster, and needs to be run when the code of
  xivo-purge-db changes.

To execute the integration tests execute:

    % docker-compose run sync
    % docker-compose run purgedb

