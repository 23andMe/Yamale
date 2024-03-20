VERSION ?= $(shell cat yamale/VERSION)

all: test

lint:
	@ruff check --fix .
	@ruff format .

test:
	@tox

clean:
	@rm -rf .tox *.egg-info dist .coverage
	@find . -name '*.pyc' -exec rm -f {} +
	@find . -name '__pycache__' -exec rm -fr {} +

release:
	@git tag $(VERSION)
	@git push --follow-tags --all
	@git push --tags

install-hooks:
	@pre-commit install -f --install-hooks -t pre-commit

.PHONY: test lint tag coverage clean release install-hooks
