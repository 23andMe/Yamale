all: test

test:
	@tox

coverage:
	@tox -- --cov yamale --cov-report term-missing

tag:
	@./setup.py tag

upload:
	@./setup.py sdist upload

clean:
	@rm -rf .tox *.egg-info dist .coverage

.PHONY: test tag bamboo coverage clean

