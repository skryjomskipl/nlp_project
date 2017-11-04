#written by chathuri 
# this file calculates the if_idf values and store them in dictinaries so that we can access them using abstract>if_idf variable
from dataset import *
import math
from textblob import TextBlob as tb


class TfIdfCalculator:
    dataset = None
    utils = None

    def __init__(self, utils):
        self.utils = utils
    
    def set_dataset(self, dataset):
        self.dataset = dataset
    
    
    def tf(self,word, blob):
        return blob.words.count(word) / len(blob.words)
    def n_containing(self,word, bloblist):
        return sum(1 for blob in bloblist if word in blob)
    def idf(self,word, bloblist):
        return math.log(len(bloblist) / (1 + self.n_containing(word, bloblist)))
    def tfidf(self,word, blob, bloblist):
        return self.tf(word, blob) * self.idf(word, bloblist)
    def __checkFun(self):
        return 0
    

    def calc_ifidf_data(self, test_dataset = False):
       
        bloblist=[]
        #store all abstrac for processing      

        for abstr in self.dataset.abstract:           
            bloblist.append(tb(abstr.text.lower()))
        
        if_idf_Values=[]
        case={}
        #calc it_idf values for each abstract seperately
        for i, blob in enumerate(bloblist):
            
            scores = {word: self.tfidf(word, blob, bloblist) for word in blob.words}
            sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)
            temp_list=[]
            for word, score in sorted_words[::]:
                if_idf_Values.append(round(score, 5))
                case[word]=round(score, 5)
                
            temp_list=case
            case={}            
            self.dataset.abstract[i].set_tf_idf(temp_list)
            
            temp_list=[]

        return 0
    #return X, Y
    
