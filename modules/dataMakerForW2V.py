#written by chathuri 
# this file creates a text file from all abstracts so that it can be use to run w2v program
from dataset import *
import math
import subprocess
from textblob import TextBlob as tb
from nltk.tokenize import RegexpTokenizer

class DataMakerForW2V:
    dataset = None
    utils = None
    file1= None
    def __init__(self, utils,fileName):
        self.utils = utils
        self.file1 = open(fileName,'w')
        
    def set_dataset(self, dataset):
        self.dataset = dataset
    
    
    def calc_w2v(self, test_dataset = False):
       
        bloblist=[]
        #store all abstrac for processing 
        for abstr in self.dataset.abstract: 
           
                        
            bloblist.append(tb(abstr.text.lower()))
            para=abstr.text.lower()
            tokenizer = RegexpTokenizer(r'\w+')
            para=tokenizer.tokenize(para)
            para = ' '.join(para)
            self.file1.write(para)
        self.file1.close() # this is needed to uncheck
         
        #print('chathu testting')
        return 0
    #return X, Y
    
