.PHONY: help

help: ## helper
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

.DEFAULT_GOAL := help

setup:
	chmod -R +x ./scripts && ./scripts/development/setup.sh

wheel-build:
	./scripts/ci/build-wheel.sh

docs-build:
	./scripts/ci/build-docs.sh

docker-build:
	./scripts/docker/build.sh $(AZIONA_VERSION) $(DOCKER_TAG)

run-test:
	./scripts/ci/run-test.sh

lint:
	pre-commit run --all-files

git-del-branch:
	git branch | grep -v "main" | xargs git branch -D

git-del-merged-branch:
	git branch --merged | grep -v \* | xargs git branch -D
