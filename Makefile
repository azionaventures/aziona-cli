.PHONY: help

help: ## helper
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

.DEFAULT_GOAL := help

setup-dev:
	chmod -R +x ./scripts && ./scripts/development/setup.sh

build-wheel:
	./scripts/ci/build-wheel.sh 

build-docs:
	./scripts/ci/build-docs.sh

build-docker:
	./scripts/development/build-docker.sh $(VERSION)

run-test:
	./scripts/ci/run-test.sh

lint:
	pre-commit run --all-files

lint-black:
	black aziona

lint-flake8:
	flake8 aziona

lint-isort:
	isort aziona

git-del-branch:
	git branch | grep -v "main" | xargs git branch -D

git-del-merged-branch:
	git branch --merged | grep -v \* | xargs git branch -D 