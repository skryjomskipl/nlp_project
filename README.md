# nlp_project
1) Installation

In order to be able to run the package and see the results, a set of libraries on which this framework relies needs to be installed. List of libraries that were used can be seen in the ORIGIN file. All the packages, with extra dependencies can be installed by executing ONE of the following commands:

	a) make init
	b) pip install -r requirements.txt
	c) pip install numpy nltk sklearn imblearn

Both of the above commands assumes that 'pip' is available in a known library path (directory). If the Python environment is used from another source on less known systems like macOS, it is a possibility that the PIP application will have different filename, although it is most common that the filename is in a 'pipX' pattern where X corresponds to the Python version. As for this project Python 3 was used, this tool might be available under 'pip3' command rather than 'pip'.

2) Usage

After installing dependencies, evaluation scripts provided within proposed environment can be used. As of now there are four scripts used for assessing performance of the solution. Please keep in mind that similarly to the PIP tool, the filename of the Python interpreter might be different from the 'python', which depends on the system but the same pattern remains. In order to execute one of the scripts which are mentioned below, type ONE of the following commands. To get list of possible actions please just type the 'make' command which will allow to list all of the implemented Makefile subroutines.

	2.1) Subtask 1.1 - k-Fold Cross Validation on the new dataset
		a) make subtask11
		b) python uberscript.py subtask11
Allows to execute script with default parameters used for getting results for the Subtask 1.1. This front-end can be used for relation classification as well directionality on custom datasets. Provided CLI utility for the first subtask is able to take following arguments:
name of subtask (only subtask11 is supported), argument required
		-b, computes baseline
		-l, specifies classifier to be used for the classification task, default svm
		-k <integer>, sets the k value for k-Fold Cross Validation, default 5
		-n <integer>, sets the percentage of dataset to be included in training set, default 60
		-m <integer>, sets the percentage of dataset to be included in test set, default 40
		-f, enables custom feature extractor selection, otherwise all of them are used
		-p, enables feature extractor 1, requires ‘-f’ parameter
		-s, enables feature extractor 2, requires ‘-f’ parameter
		-c, enables feature extractor 3, requires ‘-f’ parameter
		-i <xml file> <txt file>, provides dataset for processing, default SemEval dataset is used
		-o <txt file>, output file for storing results in SemEval format, default stdout
		-r <txt file>, output file for storing results from the calculated metrics, default stdout
		-v, enables verbose mode for debugging purposes
		-h, prints help information with arguments list and description
For more information on usage and parameters please type “uberscript.py -h”.

3) Subtask 2
	3.1)Wor2Vec value calculation : TestingW2V.ipynb
		CPAN implementation of word2vec was used. And do the following steps 
		**Note : You don’t need to run step 1-3. I generated the text file of dataset and the .bin file .I placed them in correct place if you need to run them. Run and put the .bin file in main directory. And CSV file may contain a value as ‘computed’. It is because i didn't use whole dataset for creating the bin file. So some pairs doesn’t train to give a value. 
		**Note : Please use Jupyter Notebook to run code

		Install this via the usual terminal command "cpan Word2vec::Interface"
		run CreateDataFile.ipynb file to create a text file which can be feeded to word2vec training
		Feed word2vec (CPAN) and obtain .bin file needed for the dataset and copy the bin file in main directory
		Run TestingW2V.ipynb file . It will calculate W2V values for possible entity combinations and store them in featureExtraction.csv file

4)Finding best feature combinations : featureSelector.ipynb
		If you run this file it will create a FindFeatures.csv file which contains accuracy,F Measure, precision values with their relavent feature combination.
		**important : If you unable all the features in featureCollection.py class this will take days. So i basically commented most of them and kept 2,3 so it will run faster

		featureSelector.ipynb : this file create a FindFeatures.csv file which contains possible feature combinations and its accuracy , F measure, precision value for each combination. Number represent the enabled feature (from to to bottom in featureRoot.py . For example 1+3 means feature and and feature 3 were used)
5) Information

Each script makes use of the particular datasets provided in the 'data' subdirectory. The result can be in form of the relations formatted in the way proposed in the SemEval Task 7 i.e. RELATION(E1, E2, DIRECTION). Additionally, results for the Accuracy and F-measure with average macro are presented to the user.
# Dependencies
Proposed solution depends on the following off-the-shelf libraries:
	- NLTK
		Website: http://www.nltk.org
	- Scikit-Learn, website:
		Website: http://scikit-learn.org/stable/
	- Imbalanced-Learn (imblearn), website:
		Website: http://contrib.scikit-learn.org/imbalanced-learn/stable/

Both of them can be installed by following the instructions provided in the INSTALL file.
**Note :  You don't have to install W2V but if you want to create bin file then you must install word2vec and follow steps mentioned in install file.

	-word2vec
		Websites : 	http://search.cpan.org/~cuffyca/Word2vec-Interface/
					http://search.cpan.org/~cuffyca/Word2vec-Interface/lib/Word2vec/Interface.pm
					http://search.cpan.org/~cuffyca/Word2vec-Interface/utils/Word2vec-Interface.pl 

	- Gensim:
			https://rare-technologies.com/word2vec-tutorial/
			https://radimrehurek.com/gensim/models/word2vec.html
