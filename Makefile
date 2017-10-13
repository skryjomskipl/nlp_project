# Written by: Przemyslaw Skryjomski

# NLP Project Makefile
#

PYTHON=python
PIP=pip

all:
	@echo "Possible actions:"
	@echo " init"
	@echo " release"
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

release:
	find . -name '*.pyc' -exec rm -f {} \;
	echo "# nlp_project" > README.md
	cat INSTALL >> README.md
	echo "# Dependencies" >> README.md
	cat ORIGIN >> README.md
