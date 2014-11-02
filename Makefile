all: test

test:
	@tox

tag:
	@./setup.py tag

.PHONY: test tag
