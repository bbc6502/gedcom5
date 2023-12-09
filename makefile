
.PHONY: help clean requirements build

help:
	@cat makefile

clean:
	@rm -fr venv dist build

venv:
	@python3.11 -m venv venv

requirements: venv
	@venv/bin/pip3 install --upgrade pip -r requirements.txt

test: venv
	@venv/bin/pytest --cov --cov-branch --cov-report term-missing

build: venv
	@rm -fr dist build
	@venv/bin/python -m build

test-deploy: build
	@venv/bin/python -m twine upload --repository testpypi dist/*

deploy: build
	@venv/bin/python -m twine upload dist/*
