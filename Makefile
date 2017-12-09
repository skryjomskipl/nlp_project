# Written by: Przemyslaw Skryjomski

# NLP Project Makefile
#

PYTHON=python3
PIP=pip

all:
	@echo "Possible actions:"
	@echo " init"
	@echo " release"
	@echo " subtask11"
	@echo " subtask2"

init:
	$(PIP) install -r requirements.txt

subtask11:
	$(PYTHON) uberscript.py subtask11

subtask2:
	$(PYTHON) script2.py

release:
	find . -name '*.pyc' -exec rm -f {} \;
	echo "# nlp_project" > README.md
	cat INSTALL >> README.md
	echo "# Dependencies" >> README.md
	cat ORIGIN >> README.md
