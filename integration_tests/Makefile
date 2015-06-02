.PHONY: test-image test-setup

test-setup:
	docker build -t xivo/xivo-purge-db ..
	docker pull n3llyb0y/wait
	docker pull postgres:9.1

test-image:
	docker build --no-cache -t xivo-purge-db-test -f Dockerfile ..
