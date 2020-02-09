import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import numpy as np
import pickle


stop_words_file = 'SmartStoplist.txt'

stop_words = []

with open(stop_words_file, "r") as f:
    for line in f:
        stop_words.extend(line.split())
#print(stop_words)
stop_words_lisa= stop_words #+ ['education', 'university', 'uni', 'universities', 'fee', 'fees', 'abolish', 'abolished', 'people', 'students', 'student', 'degree', 'tuition']
#df_lisa

def preprocess(raw_text):

    # keep only words
    letters_only_text = re.sub("[^a-zA-Z]", " ", raw_text)

    # convert to lower case and split
    words = letters_only_text.lower().split()

    # remove stopwords
    cleaned_words = []
    #stopword_set = set(stopwords.words("english"))   #nltk stopwords
    lemmatizer = WordNetLemmatizer()
    stopword_set = stop_words_lisa # my stopwords
    for word in words:
        word = lemmatizer.lemmatize(word)
        if word not in stop_words:
            cleaned_words.append(word)
    #cleaned_words = list(set([lemmatizer.lemmatize(w) for w in words if w not in stopword_set]))
    #print(len(stopword_set))

    return cleaned_words

#gloveFile = "glove.6B.50d.txt"

def loadGloveModel(gloveFile):
    print ("Loading Glove Model")
    with open(gloveFile, encoding="utf8" ) as f:
        content = f.readlines()
    model = {}
    for line in content:
        splitLine = line.split()
        word = splitLine[0]
        embedding = np.array([float(val) for val in splitLine[1:]])
        model[word] = embedding
    print ("Done.",len(model)," words loaded!")
    #print(model)
    return model

#model_glove = loadGloveModel(gloveFile)
#with open('glovedic.pickle', 'wb') as handle:
    #pickle.dump(model_glove, handle, protocol=pickle.HIGHEST_PROTOCOL)

with open('glovedic.pickle', 'rb') as handle:
    model_glove = pickle.load(handle)


def cosine_distance_wordembedding_method(s1, s2):
    import scipy
    try:
        vector_1 = np.mean([model_glove[word] for word in preprocess(s1)],axis=0)
        vector_2 = np.mean([model_glove[word] for word in preprocess(s2)],axis=0)
        cosine = scipy.spatial.distance.cosine(vector_1, vector_2)
        return round((1-cosine)*100,2)
    except:
        return 0
