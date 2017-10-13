# nlp_project
1) Installation

In order to be able to run the package and see the results, a set of libraries on which this framework relies needs to be installed. List of libraries that were used can be seen in the ORIGIN file. All the packages, with extra dependencies can be installed by executing ONE of the following commands:

a) make init
b) pip install -r requirements.txt
c) pip install numpy nltk sklearn

Both of the above commands assumes that 'pip' is available in a known library path (directory). If the Python environment is used from another source on less known systems like macOS, it is a possibility that the PIP application will have different filename, although it is most common that the filename is in a 'pipX' pattern where X corresponds to the Python version. As for this project Python 3 was used, this tool might be available under 'pip3' command rather than 'pip'.

2) Usage

After installing dependencies, evaluation scripts provided within proposed environment can be used. As of now there are four scripts used for assessing performance of the solution. Please keep in mind that similarly to the PIP tool, the filename of the Python interpreter might be different from the 'python', which depends on the system but the same pattern remains. In order to execute one of the scripts which are mentioned below, type ONE of the following commands. To get list of possible actions please just type the 'make' command which will allow to list all of the implemented Makefile subroutines.

2.1) Subtask 1.1 - Development set evaluation on old dataset

a) make subtask11_dev
b) python script1.py

2.2) Subtask 1.1 - Test set evaluation on old dataset

a) make subtask11_test
b) python script2.py

2.3) Subtask 1.1 - Training set split 60/40 evaluation on new dataset

a) make subtask11_split
b) python script3.py

2.4) Subtask 1.1 - k-Fold Cross Validation evaluation on new dataset

a) make subtask11_kcv
b) python script4.py

3) Information

Each script makes use of the particular datasets provided in the 'data' subdirectory. The result can be in form of the relations formatted in the way proposed in the SemEval Task 7 i.e. RELATION(E1, E2, DIRECTION). Additionally, results for the Accuracy and F-measure with average macro are presented to the user.
# Dependencies
Proposed solution depends on the following off-the-shelf libraries:

- NLTK
 Website: http://www.nltk.org

- Scikit-Learn, website:
 Website: http://scikit-learn.org/stable/

Both of them can be installed by following the instructions provided in the INSTALL file.
