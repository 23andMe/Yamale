all: test

test:
	@tox

coverage:
	@tox -- --cov yamale --cov-report term-missing

bamboo:
	@mkdir -p xunit
	@tox -e py27 -- --junitxml=xunit/py27.xml
	@tox -e py27 -- --junitxml=xunit/py34.xml

tag:
	@./setup.py tag

.PHONY: test tag bamboo coverage
