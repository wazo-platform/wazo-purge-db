.PHONY: test test-image test-setup egg-info

egg-info:
	(cd .. && python setup.py egg_info)

test-setup:
	docker pull postgres:9.6
	docker pull wazopbx/wait

test-image:
	docker build -t wazopbx/wazo-purge-db ..
	docker build --no-cache -t wazo-purge-db-test -f Dockerfile ..

test: egg-info test-image
	docker-compose run sync
	docker-compose run purgedb
	docker-compose kill
	docker-compose rm -f
