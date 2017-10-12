# NLP Project Makefile
#

PYTHON=python
PIP=pip

all:
	@echo "Possible actions:"
	@echo " init"
	@echo " clean"
	@echo " subtask11_dev"
	@echo " subtask11_test"
	@echo " subtask11_spit"
	@echo " subtask11_kcv"

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