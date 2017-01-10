# Makefile: hello

VERSION=$(shell git rev-parse --short=8 HEAD)

.PHONY: all

all: clean build

build:
	tox -e py34

clean:
	# Clean previous build outputs (e.g. class files) and temporary files. Customize as needed.
	:

# Python virtualenv automatic setup. Ensures that targets relying on the virtualenv always have an updated python to
# use.
#
# This is intended for developer convenience. Do not attempt to make venv in a Docker container or use a virtualenv in
# docker container because you will be going into a world of darkness.

venv: venv/bin/activate

venv/bin/activate: requirements.txt
	test -d venv || virtualenv venv --python python3
	venv/bin/pip install -Ur requirements.txt
	touch venv/bin/activate
