# Written by: Chathuri
#this is used for future testing purposes, becouse this calculated w2v values only for annotated relations which were provided by task7
# but other than annotated once there can be relationships exist within annotated entities 
from dataset import *
import math
from textblob import TextBlob as tb
from .featureCollection import FeatureCollection
import subprocess
from nltk.tokenize import RegexpTokenizer


class W2Vtester:
    dataset = None
    utils = None

    def __init__(self, utils):
        self.utils = utils
        print('w2vtesterworking nice')
    
    def set_dataset(self, dataset):
        self.dataset = dataset
    
    def get_dataset_key(self):
        Y = []

        for rel in self.dataset.relation:
            type = self.utils.get_level_from_name(rel.type)
            Y.append(type)
        
        return Y
    
    def print_results(self, pred_Y):
        count = 0

        for rel in self.dataset.relation:
            type = self.utils.get_level_from_id(pred_Y[count])
            reverse = ""

            if rel.reverse:
                reverse = ",REVERSE"

            print(type, "(", rel.abstract, ".", rel.a, ",", rel.abstract, ".", rel.b, reverse, ")", sep = '')

            count += 1
    
    

    def prepare_data(self, test_dataset = False):
        X = []
        Y = []
        bloblist=[]
        # Prepare features
        fc = None
        fc = FeatureCollection(self.utils, self.dataset)  
        num=1
        out = open('w2v_for_all_rel.csv', 'w')
        #for each relation
        for rel in self.dataset.relation:
            num=num+1
            
            abstract = self.dataset.get_abstract(rel.abstract)
            a = abstract.get_entity_ids(rel.a) 
            #store E1
            str1=""
            
            tokenizer = RegexpTokenizer(r'\w+')
            tok=tokenizer.tokenize(abstract.obj[a[0]].value)
            str1= ':'.join(tok)
            
            
            
            for i in a:
                if i==a[0]:
                    continue
                tok=tokenizer.tokenize(abstract.obj[i].value)
                tok= ':'.join(tok)
                str1=str1+":"+tok           
            set1=str1.lower() 
            
            
            b = abstract.get_entity_ids(rel.b)
            str1=""  
            
            #store E2
            
            tok=tokenizer.tokenize(abstract.obj[b[0]].value)
            str1= ':'.join(tok)
            
            for i in b:
                if i==b[0]:
                    continue
                tok=tokenizer.tokenize(abstract.obj[i].value)
                tok= ':'.join(tok)
                str1=str1+":"+tok          
            set2=str1.lower() 
            
            y = self.utils.get_level_from_name(rel.type)
            
            
            set3= '>resultLog.txt'
            #run w2w with 2 (multiword )entities
            cmd = "perl Word2vec-Interface.pl --cosmulti vecNLP2.bin "+set1+" "+set2+" "+set3
            subprocess.call(cmd, shell=True)
            cos=0
            flag=0
            with open('resultLog.txt', 'r') as f:
                data = f.readlines()
                words=[]
                for line in data:
                    words=[]
                    words=(line.split())
                    if 'Similarity' in words and 'Error'  not in words:
                        #print(words[len(words)-1])
                        cos=words[len(words)-1]
                        flag=1
            try:
                val=float(cos)
                flag=1
                #print(val)
            except ValueError:
                flag=0
                va=-10
            #print result to csv
                

            
            out.write('%s;' % set1)
            out.write('%s;' % set2)
            out.write('%s;' % cos)
            out.write('%d;' % y)
   
            out.write('\n')
                
                
           
            

        return 0
