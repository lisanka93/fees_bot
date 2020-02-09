import random
from flask import Flask, request
from pymessenger.bot import Bot
import re
#from nltk.corpus import stopwords
#from nltk.stem import WordNetLemmatizer
import numpy as np
import pickle
#import scipy
#-from chatbot import *


"""
****************************************************************
FLASK AP
****************************************************************
"""
app = Flask(__name__)       # Initializing our Flask application
ACCESS_TOKEN = 'EAACJjQRK0ucBAF9qkG4eRfBMe1G9wt8UZCfi5RtFbE0J2EyjE2fqjzLodlAMHRLjbFUnZACtp5YLcJstKtlmevgSdgS8vkO5aodhCazkhrf1OKgZA3EQ9VLdprUdkxlX3cuQhA73fkyOeFcDN7lHy5ZApNJJFyUU6RcKFPTPfBgh1tF5IGti'
VERIFY_TOKEN = 'UNIQE_TOKEN'
bot = Bot(ACCESS_TOKEN)

user_ids = []
prolific_ids = []


"""
****************************************************************
PREPROCESSING & SIMILARITY MEASUREMENT
****************************************************************
"""

#stuff I need for chatbot:
#glove model
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
        #print("cosine", cosine)
        #return(cosine*100)
        return round((cosine)*100,2)
    except:
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

pro_args_depth1_ = [
"But don't you think that if someone decides to go into higher education, the general public should not be expected to pay for it via taxes.",
"Ok but I think university fees make students take the university seriously. If it would be free, it wouldn't have the same value.",
"I believe the fee is a way of selecting people that really want to get in the better universities and invest in their future.",
"I think the fee is a good incentive for students to finish the degree. We see models in several european countries where university is free, and the result is that many either never finish their studies , or take an obscene number of years to finish.",
"I stll think fees should be kept as it ensures that only people who really want to attend university do so, if it is free people would take spaces just because it is an easy thing to do",
"But most students will be able to claim a student loan to pay the fees. Student loans do not count towards debt eg if you are getting a mortgage and they do not have to be paid until the graduate is earning over a certain amount.",
"Without the fees universities would have to ask for government funding to run (not going to happen, and if it did it would impact on other services such as funding for the NHS) or sponsorship or donations. Sponsorship could influence the courses which have to be taught."
]

used_args_depth1 = []


"""
****************************************************************
SIMILARITY MEASUREMENT AND ARGUMENT RETURN
****************************************************************
"""
def most_similar(argument, argument_list=con_arguments):

    for arg in argument_list:
        #print(arg[0])
        sim = cosine_distance_wordembedding_method(arg[0], argument)

        if sim < 100 and sim >= 95:
            print('most sim: ', arg[0])
            return arg[1]


    #second iteration if no match found
    for arg in argument_list:
        #print(arg[0])
        sim = cosine_distance_wordembedding_method(arg[0], argument)
        #print(sim)
        if sim >= 90:
            print('most sim: ', arg[0])
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
    if most_sim_id == "no arg" and len(user_mes.split()) < 6:
        chatbot_reply = "Why? Please expand"
        return(chatbot_reply)

    if most_sim_id == "no arg":
        chatbot_reply = "no arg"
        return(chatbot_reply)
    else:
        try:
            possible_responses = con_dic[most_sim_id]
            con_dic[most_sim_id] = con_dic[most_sim_id][1:]
            response_id = possible_responses[0]
            chatbot_reply = pro_dic[response_id]
        except:
            chatbot_reply = "no arg"
            return(chatbot_reply)


    return(chatbot_reply)






""" ***************************************************+

                THE APP

**************************************************** """



# Importing standard route and two requst types: GET and POST.
# We will receive messages that Facebook sends our bot at this endpoint
@app.route('/', methods=['GET', 'POST'])
def receive_message():
    if request.method == 'GET':
        print("hello")
        # Before allowing people to message your bot Facebook has implemented a verify token
        # that confirms all requests that your bot receives came from Facebook.
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)
    # If the request was not GET, it  must be POSTand we can just proceed with sending a message
    # back to user
    else:
        print("hello2")
        pro_args_depth1 = []
        for arg in pro_args_depth1_:
            if arg not in used_args_depth1:
                pro_args_depth1.append(arg)
            # get whatever message a user sent the bot
        output = request.get_json()

        recipient_id = output['entry'][0]['messaging'][0]['sender']['id']  #unicode, should i typecast it into string or int? lets see...
        if len(pro_args_depth1) == 0:
            response_sent_text = "I ran out of arguments :) Please go to the google form to complete the study"
            send_message(recipient_id, response_sent_text)
            return "ok"

        try:
            user_mes = output['entry'][0]['messaging'][0]['message']['text']
        except:
            response_sent_text = "Please send a reply in text format :)"
            send_message(recipient_id, response_sent_text)
            return "ok"

        if recipient_id not in user_ids:
            response_sent_text = "Hey! Before we start, please provide your prolific ID." #" and click on the following link (it contains the google form to fill out after the chat)."

            user_ids.append(recipient_id)
            send_message(recipient_id, response_sent_text)
            return "oK"
        elif recipient_id not in prolific_ids:
            print("went in here")
            response_sent_text = "Great, thanks. So tell me, why do you think university fees in the UK should be abolished?"
            send_message(recipient_id, response_sent_text)
            prolific_ids.append(recipient_id)
            return "ok"
        else:
            response_sent_text = return_arg(user_mes)
            if response_sent_text == "no arg":
                try:
                    response_sent_text=pro_args_depth1[0]
                    used_args_depth1.append(response_sent_text)

                except Exception as e:
                    print("EXCEPTION occurred here")
                    print(e)
                    response_sent_text = "I ran out of arguments :) Please go to the google form to complete the study"
            send_message(recipient_id, response_sent_text)
            return "ok"


        # if user send us a GIF, photo, video or any other non-text item




    return "Message Processed"


def verify_fb_token(token_sent):
    # take token sent by Facebook and verify it matches the verify token you sent
    # if they match, allow the request, else return an error
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'


# Uses PyMessenger to send response to the user
def send_message(recipient_id, response):
    # sends user the text message provided via input response parameter
    bot.send_text_message(recipient_id, response)
    #return "success"


# Add description here about this if statement.
if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0', port=5000, threaded=True)
    #app.run()



"""



#testing in terminal

while True:
    message = input('you: ')
    message_prep = preprocess(message)
    message_model = []

    for word in message_prep:
        try:
            vecs =  model_glove[word]
            message_model.append(word)
        except:
            print(word)



    most_sim_id = most_similar(message_model)
    #print(most_sim_id)
    if most_sim_id == "no arg":
        print('chatbot: ', "no arg")
    else:

        possible_responses = con_dic[most_sim_id]
        con_dic[most_sim_id] = con_dic[most_sim_id][1:]
        response_id = possible_responses[0]
        chatbot_reply = pro_dic[response_id]

        print('chatbot: ', chatbot_reply)
"""
