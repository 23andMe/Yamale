define VERSION_SCR
import pkg_resources
print(pkg_resources.require("yamale")[0].version)
endef

VERSION ?= $(shell .tox/py27/bin/python -c '$(VERSION_SCR)')

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
	@git push --tags --all

.PHONY: test tag coverage clean release
