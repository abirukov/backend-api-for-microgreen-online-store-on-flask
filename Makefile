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
	pytest --lf -vv
check:
	make style types test
