VERSION ?= $(shell cat yamale/VERSION)

all: test

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

.PHONY: test tag coverage clean release
