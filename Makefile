define VERSION_SCR
import pkg_resources
print(pkg_resources.require("djdt_flamegraph")[0].version)
endef

VERSION ?= $(shell python -c '$(VERSION_SCR)')

all: test

test:
	@tox

clean:
	@rm -rf .tox *.egg-info dist .coverage
	@find . -name '*.pyc' -exec rm -f {} +
	@find . -name '__pycache__' -exec rm -fr {} +

release:
	@$(MAKE) test
	git tag $(VERSION)
	git push --tags

.PHONY: test tag coverage clean release
