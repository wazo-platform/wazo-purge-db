.PHONY: test test-image test-setup

test-setup:
	docker pull n3llyb0y/wait
	docker pull postgres:9.6
	docker pull python:2.7

test-image:
	docker build -t wazopbx/xivo-purge-db ..
	docker build --no-cache -t xivo-purge-db-test -f Dockerfile ..

test: test-image
	docker-compose run sync
	docker-compose run purgedb
	docker-compose kill
	docker-compose rm -f
