#written by chathuri 
# this file creates for feature extraction /subtask two , calculate w2v (Clint) for pair of entities annotated by SemEval
from dataset import *
import math
import subprocess
from textblob import TextBlob as tb
from nltk.tokenize import RegexpTokenizer

class W2V_Calculator:
    dataset = None
    utils = None
    file1= None
    def __init__(self, utils,fileName):
        self.utils = utils
        self.file1 = fileName
        
    def set_dataset(self, dataset):
        self.dataset = dataset
    
    
    def calc_w2v(self, test_dataset = False):
        
        flag=6 #early stopping criteria
        cond=1 #condition check where to break the iteration
        #for each abstract
        out = open(self.file1, 'w')
        for abstr in self.dataset.abstract:
            if cond==flag:
                break
            
            total=len(abstr.entities)
            #for each annotated entity
            for idx,val in enumerate(abstr.entities):                
                E1=val[1]
               
                str1=""
            
                tokenizer = RegexpTokenizer(r'\w+')
                tok=tokenizer.tokenize(E1[0])
                str1= ':'.join(tok)
                
            
                lenth1=len(E1)
                
                #convert multuword entity in a way that it can feed into w2v for ex: word1:word2 2words combined with ':'
                for i,val in enumerate(E1):
                    if i==0:
                        continue
                    tok=tokenizer.tokenize(E1[i])
                    tok= ':'.join(tok)
                    str1=str1+":"+tok           
                set1=str1.lower()
                #print("set1= ",set1)
                
                
                #window size 5, which entities are we ging to compare E1 with
                if idx<5:
                    startIdx=0;
                else:
                    startIdx=idx-5;
                if idx+6>total:
                    endIdx=total;
                else:
                    endIdx=idx+6;
                
                indexes =list(range(startIdx,idx))                    
                indexes1 =list(range(idx+1,endIdx)) 
                allidx=indexes+indexes1
               
                #compare E1 with possible E2s within a give window 
                for E in [abstr.entities[x] for x in allidx]:
                    #print("E2 =",E[1])
                    
                    E2=E[1]
                    str1=""
            
                    tokenizer = RegexpTokenizer(r'\w+')
                    tok=tokenizer.tokenize(E2[0])
                    str1= ':'.join(tok)
                    #print("str1= ",str1)
            
                    lenth1=len(E1)
                
                    for i,val in enumerate(E2):
                        if i==0:
                            continue
                        tok=tokenizer.tokenize(E2[i])
                        tok= ':'.join(tok)
                        str1=str1+":"+tok           
                    set2=str1.lower()
                    
                    #calc w2v value
                    #store result in a text file
                    set3= '>resultLog.txt'
                    #cmd = "perl Word2vec-Interface.pl --cosmulti vecNLP2.bin lr:parser cf:grammars >resultzzz2.txt"#+set1+set2+set3
                    cmd = "perl Word2vec-Interface.pl --cosmulti vecNLP4.bin "+set1+" "+set2+" "+set3
                    subprocess.call(cmd, shell=True)
                    cos=0
                    flag=0
                    #access the text file
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
                    
                    
                    out.write('%s;' % set1)
                    out.write('%s;' % set2)
                    out.write('%s;' % cos)
                    
   
                    out.write('\n')
                    
            cond=cond+1               
              
        print('chathu testting')
        return 0
    
