.PHONY: test test-image test-setup

test-setup:
	docker pull n3llyb0y/wait
	docker pull postgres:9.1
	docker pull python:2.7
	docker build -t xivo/xivo-purge-db ..

test-image:
	docker build --no-cache -t xivo-purge-db-test -f Dockerfile ..

test: test-image
	docker-compose run sync
	docker-compose run purgedb
	docker-compose kill
	docker-compose rm -f
