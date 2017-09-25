# NLP Project Makefile
#

PYTHON=python3
PIP=pip3

all:
	@echo "Possible options: init, test"

init:
	$(PIP) install -r requirements.txt

test:
	$(PYTHON) main.py

clean:
	find . -name '*.pyc' -exec rm -f {} \;