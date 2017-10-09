# NLP Project Makefile
#

PYTHON=python3
PIP=pip3

all:
	@echo "Possible options: init, test"

init:
	$(PIP) install -r requirements.txt

subtask11_dev:
	$(PYTHON) script1.py

subtask11_test:
	$(PYTHON) script2.py

subtask11_split:
	$(PYTHON) script3.py

subtask11_kcv:
	$(PYTHON) script4.py

clean:
	find . -name '*.pyc' -exec rm -f {} \;