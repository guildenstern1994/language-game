ROOT_DIR=$(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))
CUR = $PWD -P
setup:
	pip install -U -e .
test:
	cd tests && pwd && \
	python -m unittest discover -s ./ -p '*.py'
