ROOT_DIR=$(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))
CUR = $PWD -P
setup:
	export PATH=PYTHONPATH:CUR

test:
	cd tests && pwd && \
	python language_object_tests.py
	python *.py
