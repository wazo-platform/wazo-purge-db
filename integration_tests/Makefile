.PHONY: test test-image test-setup

test-setup:
	docker pull postgres:9.6
	docker pull wazopbx/wait

test-image:
	docker build -t wazopbx/xivo-purge-db ..
	docker build --no-cache -t xivo-purge-db-test -f Dockerfile ..

test: test-image
	docker-compose run sync
	docker-compose run purgedb
	docker-compose kill
	docker-compose rm -f
