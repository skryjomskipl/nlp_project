# Features #3
# This file is create by Chathuri 
import nltk
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize

class FeaturesF3:
    utils = None
    dataset = None    
    stop_words=None
    
    def __init__(self, utils, dataset):
        self.utils = utils
        self.dataset = dataset
        self.stop_words=['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours',
        'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers',
        'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves',
        'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are',
        'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does',
        'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until',
        'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into',
        'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down',
        'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here',
        'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more',
        'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so',
        'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now']

    def __feature (self, abstract, rel):
        #word before E1 with lematization        
        ps = PorterStemmer()
        abstract = self.dataset.get_abstract(rel.abstract)   
        
        #print("rel.abstract-> ", rel.abstract)
        tokens = []
        tokens2 = []
        for obj in abstract.obj:
            tokens.append(obj.value)
                   
        a = abstract.get_entity_ids(rel.a) 
        
        word_list=[];
        word_count=0;
        i=min(a)-1;
        while i>=0:            
            if abstract.obj[i].value=='.':
                break 
            if '.' in abstract.obj[i].value and abstract.obj[i].value not in self.stop_words:
                word_list.append(abstract.obj[i].value)                
                word_count=+1
                break 
            #if abstract.obj[i].value in stop_words:
                #stop_word_count+=1;
            #if  abstract.obj[i].value not in stop_words:
            if abstract.obj[i].value not in self.stop_words: 
                word_list.append(abstract.obj[i].value)             
                word_count=word_count+1
            if word_count==1:
                break
            i=i-1
            
        if len(word_list)==1:
            return int.from_bytes(word_list[0].encode(), 'little')
            #print("-> ", word_list[0])
        if len(word_list)!=1:
            return 0
        
    def __noOf_words_beforeE1(self,abstract,rel,flag):
         #Number of words before E1 in the full sentance. (Feature2)
            #Calc if-idf val
        noOfWords=0;
        delimeter=['.']
        ps = PorterStemmer()       
        str_id=0
        stop_word_count=0        
        a = abstract.get_entity_ids(rel.a)         
        i=min(a)-1;
        while i>=0:
            if abstract.obj[i].value=='.':
                str_id=i+1;
                break
            if '.' in abstract.obj[i].value:                
                str_id=i;
                break 
            if  abstract.obj[i].value.lower() in abstract.tf_idf.keys():
                if flag==1:
                    if abstract.tf_idf[abstract.obj[i].value.lower()]<0.02:
                        stop_word_count+=1;
                        i=i-1
                        continue
            if (abstract.obj[i].value.lower()) in self.stop_words:
                stop_word_count+=1;
            
                #break   
            i=i-1    
        return (min(a)-str_id)-stop_word_count  
    
    
    def __noOf_words_afterE2(self,abstract,rel,flag):
         #Number of words after E2 in the full sentance.(Feature3)
        #print("rel>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>");
        noOfWords=0;
        delimeter=['.']
        ps = PorterStemmer()
        stop_word_count=0
        
        b = abstract.get_entity_ids(rel.b) 
        #print("rel=",abstract.id)
        #print("rel.b=",rel.b)
        i=max(b)+1;
        str_id=max(b)+1;
        #print("i=",i)
        while i<len(abstract.obj):#??
            #print("abstract.obj[i].value=",abstract.obj[i].value)
            if abstract.obj[i].value=='.':
                str_id=i-1;
                break 
            if '.' in abstract.obj[i].value:
                str_id=i;
                break
            if  abstract.obj[i].value.lower() in abstract.tf_idf.keys():
                if flag==1:
                    if abstract.tf_idf[abstract.obj[i].value.lower()]<0.02:
                        stop_word_count+=1;
                        i=i+1
                        continue
            if (abstract.obj[i].value.lower()) in self.stop_words or abstract.obj[i].value in [',',';']:
                stop_word_count+=1;                  
            i=i+1
            str_id=i 
        #print("value= ",(str_id-max(b))-stop_word_count)
        return (str_id-max(b))-stop_word_count
    
    
    def __wordBeforE1 (self, abstract, rel):
        #word before E1 (featur 6)
        a = abstract.get_word_beforeE1(rel.a) 
        ps = PorterStemmer()
        
        word_no=min(a)-1
        word=""       
        count=0
        i=min(a)-1
        word=0
        
        while i>=0:
            if abstract.obj[i].value :
                if abstract.obj[i].value=='.':                    
                    break 
                if ps.stem(abstract.obj[i].value.lower()) not in self.stop_words and abstract.obj[i].value not in [',','-',';']: #add the list
                    
                    word=ps.stem(abstract.obj[i].value.lower())
                    word=int.from_bytes(word.encode(), 'little')
                    break
                else:
                    i=i-1
       
        return word
        #return 0
    
    def __wordAfterE2(self, abstract, rel):
        #word before E1 (featur 6)
        b = abstract.get_word_beforeE1(rel.b) 
        ps = PorterStemmer()
        
        word=0
        i=max(b)+1;
        str_id=max(b)+1;
        #print("i=",i)
        while i<len(abstract.obj):#
            if abstract.obj[i].value :
                if abstract.obj[i].value=='.':                    
                    break 
                if ps.stem(abstract.obj[i].value.lower()) not in self.stop_words and abstract.obj[i].value not in [',','-',';']: #add the list
                    word=abstract.obj[i].value
                    word=int.from_bytes(word.encode(), 'little')
                    break
                else:
                    i=i+1
       
        return word  
    
    def __POS_beforeE1(self, abstract, rel,flag):
        # checking pos tag of words before E1 , window size=2
        abstract = self.dataset.get_abstract(rel.abstract)   
        ps = PorterStemmer()
        tokens = []
        for obj in abstract.obj:
            tokens.append(obj.value)
        
        tokens_pos = nltk.pos_tag(tokens)        
        noOfWords=0;
        delimeter=['.']
        
        str_id=0
        stop_word_count=0
        out = [];
        
        a = abstract.get_entity_ids(rel.a) 
        
        word_list=[];
        word_count=0;
        i=min(a)-1;
        while i>=0:            
            if abstract.obj[i].value=='.':
                break 
            if '.' in abstract.obj[i].value:
                word_list.append(i)                
                word_count=word_count+1
                break 
            if  abstract.obj[i].value.lower() in abstract.tf_idf.keys():
                if flag==1:
                    if abstract.tf_idf[abstract.obj[i].value.lower()]<0.02:
                        stop_word_count+=1;
                        i=i-1
                        continue    
            word_list.append(i);            
            word_count=word_count+1
            if word_count==2:
                break
            i=i-1
        #self.utils.get_feature_from_pos_tagger(tokens_pos[word_list[0]][1])
        if len(word_list)==2:
            out.append(self.utils.get_feature_from_pos_tagger(tokens_pos[word_list[0]][1]))
            out.append(self.utils.get_feature_from_pos_tagger(tokens_pos[word_list[1]][1]))
        if len(word_list)==1:
            out.append(self.utils.get_feature_from_pos_tagger(tokens_pos[word_list[0]][1]))
            out.append(0)
        if len(word_list)==0:
            out.append(0)
            out.append(0)
        
       
       
        return out
    
    def __POS_AfterE2(self, abstract, rel,flag):
        # checking pos tag of words before E1 , window size=2
        
        abstract = self.dataset.get_abstract(rel.abstract)   
        ps = PorterStemmer()
        tokens = []
        for obj in abstract.obj:
            tokens.append(obj.value)
        
        tokens_pos = nltk.pos_tag(tokens)        
        noOfWords=0;
        delimeter=['.']
        
        str_id=0
        stop_word_count=0
        out = [];
        
        b = abstract.get_entity_ids(rel.b) 
        
        word_list=[]
        word_count=0
        i=max(b)+1
        while i<len(abstract.obj):#
            #print("bstract.obj[i].value=",abstract.obj[i].value)
            if abstract.obj[i].value=='.':                
                break 
            if '.' in abstract.obj[i].value:                    
                word_list.append(i)                
                word_count=word_count+1
                #print("added")
                break  
            if (abstract.obj[i].value.lower()) not in self.stop_words and abstract.obj[i].value not in [',','-',';']: #add the list
                if flag==1:
                    if  abstract.obj[i].value.lower() in abstract.tf_idf.keys():
                        if abstract.tf_idf[abstract.obj[i].value.lower()]<0.02:
                            stop_word_count+=1;
                            i=i+1
                            continue    
                word_list.append(i)                
                word_count=word_count+1
                #print("added")
            if word_count==2:
                break
                
            i=i+1
        #self.utils.get_feature_from_pos_tagger(tokens_pos[word_list[0]][1])
        #print("loop ok")
        #print("len(word_list)=",len(word_list))
        if len(word_list)!=0:
            
            
            if len(word_list)==2:
                
                out.append(self.utils.get_feature_from_pos_tagger(tokens_pos[word_list[0]][1]))
                out.append(self.utils.get_feature_from_pos_tagger(tokens_pos[word_list[1]][1]))
                
            if len(word_list)==1:
                
                out.append(self.utils.get_feature_from_pos_tagger(tokens_pos[word_list[0]][1]))
                out.append(0)
                
        if len(word_list)==0:
            out.append(0)
            out.append(0)
            
        return out
                
    def __POS_AfterE1(self, abstract, rel,flag):
        # checking pos tag of words before E1 , window size=2
        abstract = self.dataset.get_abstract(rel.abstract)   
        ps = PorterStemmer()
        tokens = []
        for obj in abstract.obj:
            tokens.append(obj.value)
        
        tokens_pos = nltk.pos_tag(tokens)        
       
        wordIndex = 0; 
        pos=0;
        b = abstract.get_entity_ids(rel.b) 
        a = abstract.get_entity_ids(rel.a) 
       
        i=max(a)+1;
        while i<len(abstract.obj):
            
            if abstract.obj[i].value :
                if abstract.obj[i].value=='.':                    
                    break 
                if '.' in abstract.obj[i].value:                    
                    wordIndex=i 
                    break  
                if abstract.obj[i].value.lower() not in self.stop_words and abstract.obj[i].value not in [',','-',';']: #add the list                
                    if flag==1:
                        if  abstract.obj[i].value.lower() in abstract.tf_idf.keys():
                            if abstract.tf_idf[abstract.obj[i].value.lower()]<0.02:                        
                                i=i+1
                                continue 
                    wordIndex=i 
                    break                  
                i=i+1
        
        if wordIndex!=0:            
            pos=(self.utils.get_feature_from_pos_tagger(tokens_pos[wordIndex][1]))
        return pos
    
    def __POS_BeforeE2(self, abstract, rel,flag):
        # checking pos tag of words before E1 , window size=2
        abstract = self.dataset.get_abstract(rel.abstract)   
        ps = PorterStemmer()
        tokens = []
        for obj in abstract.obj:
            tokens.append(obj.value)
        
        tokens_pos = nltk.pos_tag(tokens)        
       
        wordIndex = 0; 
        pos=0;
        b = abstract.get_entity_ids(rel.b) 
        a = abstract.get_entity_ids(rel.a) 
       
        i=min(b)-1;
        while i<len(abstract.obj):
            
            if abstract.obj[i].value :
                if abstract.obj[i].value=='.':                    
                    break 
                if '.' in abstract.obj[i].value:
                    #if  abstract.obj[i].value in abstract.tf_idf.keys():
                        #if abstract.tf_idf[abstract.obj[i].value]<0.02:
                            #i=i-1
                            #continue                        
                    wordIndex=i 
                    break  
                if abstract.obj[i].value.lower() not in self.stop_words and abstract.obj[i].value not in [',','-',';']: #add the list
                    if flag==1:
                        if  abstract.obj[i].value.lower() in abstract.tf_idf.keys():
                            if abstract.tf_idf[abstract.obj[i].value.lower()]<0.02:                        
                                i=i-1
                                continue
                    wordIndex=i 
                    break                  
                i=i-1
        if wordIndex!=0:            
            pos=(self.utils.get_feature_from_pos_tagger(tokens_pos[wordIndex][1]))
            
        return pos
    
    def get_features(self, rel):
        X = []
        # Prepare stuff
        abstract = self.dataset.get_abstract(rel.abstract)
        
       
        #out=self.__POS_beforeE1(abstract,rel) 
        """
        noOfWordsBeforeE1=self.__noOf_words_beforeE1(abstract,rel,0)
        X.append(noOfWordsBeforeE1)
        noOfWordsBeforeE1=self.__noOf_words_beforeE1(abstract,rel,1)
        X.append(noOfWordsBeforeE1)
        noOfWordsAfterE2=self.__noOf_words_afterE2(abstract,rel,0)
        X.append(noOfWordsAfterE2) 
        noOfWordsAfterE2=self.__noOf_words_afterE2(abstract,rel,1)
        X.append(noOfWordsAfterE2)
        wordBeforeE1=self.__wordBeforE1(abstract,rel)
        X.append(wordBeforeE1) 
        wordAfterE2=self.__wordAfterE2(abstract,rel)
        X.append(wordAfterE2) 
        posAfterE2=self.__POS_AfterE2(abstract,rel,0)
        X.append(posAfterE2[0])
        X.append(posAfterE2[1])
        posAfterE2=self.__POS_AfterE2(abstract,rel,1)
        X.append(posAfterE2[0])
        X.append(posAfterE2[1])
        posBeforeE1=self.__POS_beforeE1(abstract,rel,0)
        X.append(posBeforeE1[0])
        X.append(posBeforeE1[1])
        posBeforeE1=self.__POS_beforeE1(abstract,rel,1)
        X.append(posBeforeE1[0])
        X.append(posBeforeE1[1])
        posAfterE1=self.__POS_AfterE1(abstract,rel,0)
        X.append(posAfterE1)
        """
        posAfterE1=self.__POS_AfterE1(abstract,rel,1)
        X.append(posAfterE1)
        #posBeforeE2=self.__POS_BeforeE2(abstract,rel,0)        
        #X.append(posBeforeE2)
        #posBeforeE2=self.__POS_BeforeE2(abstract,rel,1)        
        #X.append(posBeforeE2)
        
        #choose posAfterE1 posBeforeE2
        #note : change functions to on and off if idf , can hurt accuracy if tf idf use , sometimes
        return X