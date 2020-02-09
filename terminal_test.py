import random
from flask import Flask, request
#from pymessenger.bot import Bot
import re
#from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import numpy as np
import pickle
import scipy
#-from chatbot import *




"""
****************************************************************
PREPROCESSING & SIMILARITY MEASUREMENT
****************************************************************
"""

#stuff I need for chatbot:
#glove model
#with open('glovedic.pickle', 'rb') as handle:
    #model_glove = pickle.load(handle)

with open('new_dic.pickle', 'rb') as handle:
    model_glove = pickle.load(handle)

# stopwords and preprocessing step
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
    #lemmatizer = WordNetLemmatizer()
    stopword_set = stop_words_lisa # my stopwords
    for word in words:
        #word = lemmatizer.lemmatize(word)
        if word not in stop_words:
            cleaned_words.append(word)
    #cleaned_words = list(set([lemmatizer.lemmatize(w) for w in words if w not in stopword_set]))
    #print(len(stopword_set))


    return cleaned_words


def cos_sim(a,b):
    dot = np.dot(a, b)
    norma = np.linalg.norm(a)
    normb = np.linalg.norm(b)
    cos = dot / (norma * normb)
    #print(cos)
    return(cos)


def cosine_distance_wordembedding_method(s1, s2):

    try:

        vector_1 = np.mean([model_glove[word] for word in preprocess(s1)],axis=0)


        vector_2 = np.mean([model_glove[word] for word in s2],axis=0)
        cosine = cos_sim(vector_1, vector_2)
        #cos_sim = dot(vector_1, vector_2)/(norm(vector_1)*norm(vector_2))
        #print("COS SIM", cos_sim)
        print("cosine", cosine)
        #return(cosine*100)
        return round((cosine)*100,2)
    except:
        #print("something went wrong")
        return 0


"""
****************************************************************
NEEDED DFS & DICS (of pro and con args from graph)
****************************************************************
"""

with open('con_dic.pickle', 'rb') as handle:
    con_dic = pickle.load(handle)
with open('pro_dic.pickle', 'rb') as handle:
    pro_dic = pickle.load(handle)
with open('con_arguments.pickle', 'rb') as handle:
    con_arguments = pickle.load(handle)



"""
****************************************************************
SIMILARITY MEASUREMENT AND ARGUMENT RETURN
****************************************************************
"""
def most_similar(argument, argument_list=con_arguments):
    for arg in argument_list:

        sim = cosine_distance_wordembedding_method(arg[0], argument)
        #print(sim)
        if sim < 100 and sim >= 95:
            #print('most sim: ', arg[0])
            print(sim)
            return arg[1]


    #second iteration if no match found
    for arg in argument_list:
        #print(arg[0])
        sim = cosine_distance_wordembedding_method(arg[0], argument)
        #print(sim)
        if sim >= 90:
            #print('most sim: ', arg[0])
            print(sim)
            return arg[1]
    return "no arg"


def return_arg(user_mes):

    message_prep = preprocess(user_mes)
    message_model = []

    for word in message_prep:
        try:

            vecs =  model_glove[word]
            message_model.append(word)
        except:
            print(word)
            #continue
    most_sim_id = most_similar(message_model)
    if most_sim_id == "no arg":
        #print('chatbot: ', "no arg")
        return("no counter argument")
    else:

        possible_responses = con_dic[most_sim_id]
        con_dic[most_sim_id] = con_dic[most_sim_id][1:]
        response_id = possible_responses[0]
        chatbot_reply = pro_dic[response_id]

    return(chatbot_reply)




#testing in terminal

message = input('you: ')
chatbot_reply = return_arg(message)
print('chatbot: ', chatbot_reply)
