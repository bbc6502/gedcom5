
.PHONY: help clean requirements

help:
	@cat makefile

clean:
	@rm -fr venv dist

venv:
	@python3.11 -m venv venv

requirements: venv
	@venv/bin/pip3 install --upgrade pip -r requirements.txt

test:
	@venv/bin/pytest --cov --cov-branch

build:
	@rm -fr dist
	@venv/bin/python -m build

test-deploy: build
	@venv/bin/python -m twine upload --repository testpypi dist/*

deploy: build
	@venv/bin/python -m twine upload dist/*
