ifneq (,$(wildcard .env))
$(info Found .env file.)
	include .env
	export
endif

export PYTHONPATH := $(shell pwd):$(PYTHONPATH)
style:
	flake8 .
types:
	mypy .
test:
	pytest --lf -vv --cov=beaver_app --cov-branch --cov-fail-under=80 .
check:
	make style types test
