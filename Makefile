all: test

test:
	@tox

tag:
	@./setup.py tag

upload:
	@./setup.py sdist upload

clean:
	@rm -rf .tox *.egg-info dist .coverage

.PHONY: test tag coverage clean

