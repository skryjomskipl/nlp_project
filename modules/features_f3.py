# Features #3
#
import nltk
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize

class FeaturesF3:
    utils = None
    dataset = None

    def __init__(self, utils, dataset):
        self.utils = utils
        self.dataset = dataset
        
    def __feature (self, abstract, rel):
        #word before E1 with lematization
        stop_words=['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours',
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
            if '.' in abstract.obj[i].value and abstract.obj[i].value not in stop_words:
                word_list.append(abstract.obj[i].value)                
                word_count=+1
                break 
            #if abstract.obj[i].value in stop_words:
                #stop_word_count+=1;
            #if  abstract.obj[i].value not in stop_words:
            if abstract.obj[i].value not in stop_words: 
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
    
    def __featurevo1 (self, abstract, rel):
        #word before E1
        a = abstract.get_word_beforeE1(rel.a) 
        ps = PorterStemmer()
        #print("-> ", a)
        word_no=min(a)-1;
        word="";        
        count=0;
        for obj in abstract.obj:
            
            if((count)==word_no):
                word=obj.value
            count+=1
        
        return int.from_bytes(word.encode(), 'little')
        
    def __noOf_words_beforeE1(self,abstract,rel):
         #Number of words before E1 in the full sentance.
        noOfWords=0;
        delimeter=['.']
        stop_words=['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours',
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
            if abstract.obj[i].value in stop_words:
                stop_word_count+=1;
                #break   
            i=i-1    
        return (min(a)-str_id)-stop_word_count    
    
    def __noOf_words_afterE2(self,abstract,rel):
         #Number of words before E1 in the full sentance.
        noOfWords=0;
        delimeter=['.']
        stop_words=['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours',
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
        
        stop_word_count=0
        
        b = abstract.get_entity_ids(rel.b) 
        
        i=max(b);
        str_id=max(b);
        while i<=len(abstract.obj):#??
            
            if abstract.obj[i].value=='.':
                str_id=i-1;
                break 
            if '.' in abstract.obj[i].value:
                str_id=i;
                break 
            if abstract.obj[i].value in stop_words or abstract.obj[i].value in [',',';']:
                stop_word_count+=1;                  
            i=i+1
            str_id=i   
        return (str_id-max(b))-stop_word_count
    
    def __feature6 (self, abstract, rel):
        
        abstract = self.dataset.get_abstract(rel.abstract)   
        #print("-> ", a)
        tokens = []
        for obj in abstract.obj:
            tokens.append(obj.value)
        
        tokens_pos = nltk.pos_tag(tokens)        
        noOfWords=0;
        delimeter=['.']
        stop_words=['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours',
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
                word_count=+1
                break 
            #if abstract.obj[i].value in stop_words:
                #stop_word_count+=1;
            #if  abstract.obj[i].value not in stop_words:
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
        
       
        #b = abstract.get_entity_ids(rel.b)
        return out
    
    def get_features(self, rel):
        X = []
        # Prepare stuff
        abstract = self.dataset.get_abstract(rel.abstract)
        Unique_no=self.__featurevo1(abstract,rel)        
        #X.append(  Unique_no)
        # TODO
            
        
       
        #a = 
        out=self.__feature6(abstract,rel) 
        noOfWordsBeforeE1=self.__noOf_words_beforeE1(abstract,rel)
        noOfWordsAfterE2=self.__noOf_words_afterE2(abstract,rel)
        lemVal=self.__feature(abstract,rel)
        #print("out-> ", lemVal)
        X.append(  noOfWordsBeforeE1)
        X.append(  noOfWordsAfterE2)
        #X.append(lemVal)
        #X.append(out[0])
        #X.append(out[1])
        return X
