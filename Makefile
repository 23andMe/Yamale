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

clean:
	@rm -rf .tox *.egg-info dist .coverage

.PHONY: test tag bamboo coverage clean
