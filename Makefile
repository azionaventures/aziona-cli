.PHONY: help

help: ## helper
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

.DEFAULT_GOAL := help

setup:
	chmod -R +x ./bin && ./bin/setup.sh

deploy:
	./bin/deploy.sh

build-wheel:
	./bin/build-wheel.sh 

build-docs:
	./bin/build-docs.sh

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