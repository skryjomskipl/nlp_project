#written by Samantha
#this is not fully implemented
#it is written to test the abstract text file from a local directory
#rest will be implemented as the future work

import nltk.collocations
import nltk.corpus
import collections

class GenSim:
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    #load the abstracts in the text format from a local directory
    text = ''.join(open('/home/samantha/input2w2v_del.txt').readlines())
    sentences = re.split(r' *[\.\?!][\'"\)\]]* *', text)
    arr=[]
    gow=[]

    #pre-processing of the sentence 
    for sentence in sentences:
        tokenizer = RegexpTokenizer(r'\w+')
        s=tokenizer.tokenize(sentence)
        arr.append(s)

    #train the model with the parameters
    model = gensim.models.Word2Vec(arr, min_count=1, window=8, size =200, negative =25, workers=2 ) 
    #model = gensim.models.Word2Vec(gow, size=200, window=8, negative =25, workers=4 )
    model.init_sims(replace=True)

    # save the model for later use
    # for loading, call Word2Vec.load()
    model.save("Words.model")
    model = gensim.models.Word2Vec.load("Words.model")

    #calculate cosine similarity between entites that has one word
    model2.similarity('oral', 'important')
    #calculate cosine similarity between entites that has more than one word
    model.n_similarity(['oral','communication'], ['important','information'])
     