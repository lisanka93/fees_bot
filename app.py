import random
from flask import Flask, request
from pymessenger.bot import Bot
import re
from datetime import datetime
import numpy as np
import pickle
import os
cwd = os.getcwd()


"""
****************************************************************
FLASK AP
****************************************************************
"""

#initialising the flask application and connecting to facebook app
#no need to change anything unless assigned facebook page is changed (generate new access token)
app = Flask(__name__)
ACCESS_TOKEN = 'EAACJjQRK0ucBANlraAkl0AZCaDsVyQD71WUVEh0veGtTfSovkrWmUyciE50j0ZCKqtQVAeE1CA8TBU1RNfOif4Ja2zNeVnUTn4vPcrtdZA0vpSoRgseN0D8fZCt34jVJl4JIX4Fo5bIFzyZCb01N1FaL1N5jvQ8bZC00TdxIqSAAZDZD'
VERIFY_TOKEN = 'UNIQE_TOKEN'
bot = Bot(ACCESS_TOKEN)

#storing user IDs - needed to send welcomemessage
user_ids = []
#storing user IDs again to proceed with chat after they provided their prolific ID
prolific_ids = []
# stores the depth1 arguments for each user and deletes the ones used - once the list is empty - chat is ended
user_ids_dic = {}
# stores the chat logs for each user
chat_logs = {}
# stores start and end time for each user
timestamps = {}

pickle_path = cwd + "/chatlogs/"


"""
****************************************************************
PREPROCESSING & SIMILARITY MEASUREMENT
****************************************************************
"""


#glove model
with open('glovedic.pickle', 'rb') as handle:
    model_glove = pickle.load(handle)

# stopwords and preprocessing step
stop_words_file = 'SmartStoplist.txt'

stop_words = []

with open(stop_words_file, "r") as f:
    for line in f:
        stop_words.extend(line.split())
#print(stop_words)


def preprocess(raw_text):

    # keep only words
    letters_only_text = re.sub("[^a-zA-Z]", " ", raw_text)

    # convert to lower case and split
    words = letters_only_text.lower().split()

    # remove stopwords
    cleaned_words = []

    for word in words:
        #word = lemmatizer.lemmatize(word)
        if word not in stop_words:
            cleaned_words.append(word)

    return cleaned_words

def cos_sim(a,b):
    dot = np.dot(a, b)
    norma = np.linalg.norm(a)
    normb = np.linalg.norm(b)
    cos = dot / (norma * normb)

    return(cos)


def cosine_distance_wordembedding_method(s1, s2):


    try:
        #preprocessing the sentence in the knowledge base
        vector_1 = np.mean([model_glove[word] for word in preprocess(s1)],axis=0)
        # not preprocessing the user message because it was already preprocessed
        vector_2 = np.mean([model_glove[word] for word in s2],axis=0)


        cosine = cos_sim(vector_1, vector_2)

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
"I still think fees should be kept as it ensures that only people who really want to attend university do so, if it is free people would take spaces just because it is an easy thing to do",
"But most students will be able to claim a student loan to pay the fees. Student loans do not count towards debt eg if you are getting a mortgage and they do not have to be paid until the graduate is earning over a certain amount.",
"Without the fees universities would have to ask for government funding to run (not going to happen, and if it did it would impact on other services such as funding for the NHS) or sponsorship or donations. Sponsorship could influence the courses which have to be taught."
]



#pro_args_depth1_ = ["testing bot2", "testingbot1", "testingbot0"]
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
            print('most sim 95+: ', sim, arg[0])
            return arg[1]


    #second iteration if no match found
    for arg in argument_list:
        #print(arg[0])
        sim = cosine_distance_wordembedding_method(arg[0], argument)
        #print(sim)
        if sim >= 90:
            print('most sim 90: ',sim, arg[0])
            return arg[1]

    return "no arg"

def return_arg(user_mes):

    response_id = 0
    user_mes = user_mes.lower()

    # checking first whether person agrees - then no need to check for counterarg
    agree = ['agree', 'agreed']
    disagree = ['dont', "don't", "not"]

    bool_agree =  any(x in user_mes.split() for x in agree)
    bool_disagree = any(x in user_mes.split() for x in disagree)


    if bool_agree == True and bool_disagree == False and len(user_mes.split()) < 6:
        chatbot_reply = "no arg"
        return(response_id, chatbot_reply)

    #then checking whether message is very short - then ask to expand
    if len(user_mes.split()) < 6:
        chatbot_reply = "Why? Please expand"
        return(response_id, chatbot_reply)


    # now lets preprocess and look for a match in the KB
    message_prep = preprocess(user_mes)

    message_model = []

    for word in message_prep:
        try:

            vecs =  model_glove[word]
            message_model.append(word)
        except:
            print(word)
            #continue
    #id of most similar argument in KB
    most_sim_id = most_similar(message_model) # returns no arg if no match found where cosine similarity above 90


    if most_sim_id == "no arg":
        chatbot_reply = "no arg"
        return(response_id, chatbot_reply)
    else:
        try:
            #since an argument has several CAs in the KB eventually the list might be empty - hence exception
            # it would probably be smart to then go back and find another similar match but whatever - can fix that later
            possible_responses = con_dic[most_sim_id]
            con_dic[most_sim_id] = con_dic[most_sim_id][1:]
            response_id = possible_responses[0]
            chatbot_reply = pro_dic[response_id]
        except:
            chatbot_reply = "no arg"
            return(response_id, chatbot_reply)


    return(most_sim_id, chatbot_reply)






""" ***************************************************+

                THE APP

**************************************************** """



# Importing standard route and two requst types: GET and POST.
# We will receive messages that Facebook sends our bot at this endpoint
@app.route('/', methods=['GET', 'POST'])
def receive_message():
    if request.method == 'GET':
        # Before allowing people to message your bot Facebook has implemented a verify token
        # that confirms all requests that your bot receives came from Facebook.
        token_sent = request.args.get("hub.verify_token")

        return verify_fb_token(token_sent)
    # If the request was not GET, it  must be POSTand we can just proceed with sending a message
    # back to user
    else:

        output = request.get_json()


        recipient_id = output['entry'][0]['messaging'][0]['sender']['id']  #unicode, should i typecast it into string or int? lets see...
        timestamp_ = output['entry'][0]['messaging'][0]['timestamp']
        timestamp = int(timestamp_) /1000
        dt_object = datetime.fromtimestamp(timestamp)

        str_dt = str(dt_object)
        mes_time = str_dt.split()[1]


        try:
            user_mes = output['entry'][0]['messaging'][0]['message']['text']


        except Exception as e:
            print(e)
            response_sent_text = "Please send a reply in text format :)"
            send_message(recipient_id, response_sent_text)
            return "ok"

        stop = user_mes.lower()


        if recipient_id not in user_ids:
            user_ids_dic[recipient_id] = pro_args_depth1_
            chat_logs[recipient_id] = []
            timestamps[recipient_id] = [mes_time]
            response_sent_text = "Hey! Before we start, please provide your prolific ID." #" and click on the following link (it contains the google form to fill out after the chat)."

            user_ids.append(recipient_id)
            send_message(recipient_id, response_sent_text)
            return "oK"

        elif recipient_id not in prolific_ids:

            response_sent_text = "Great, thanks. So tell me, why do you think university fees in the UK should be abolished?"
            send_message(recipient_id, response_sent_text)
            prolific_ids.append(recipient_id)
            return "ok"

        elif stop == "stop":
            response_sent_text = "You are ending the chat. Please go to the google form to complete the study: https://forms.gle/aqDtpUKcd2Xrd3A69"
            send_message(recipient_id, response_sent_text)

            log_mes= "User: " + user_mes
            chat_logs[recipient_id].append(log_mes)

            timestamps[recipient_id].append(mes_time)
            recipient_logs = chat_logs[recipient_id]
            recipient_times = timestamps[recipient_id]

            data = recipient_logs + recipient_times

            pickle_file_name = pickle_path + recipient_id + ".pickle"
            with open(pickle_file_name, 'wb') as handle:
                pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)
            return "ok"


        else:
            response_id, response_sent_text = return_arg(user_mes)

            if response_sent_text == "no arg":
                try:
                    response_sent_text=user_ids_dic[recipient_id][0]
                    user_ids_dic[recipient_id] = user_ids_dic[recipient_id][1:]
                    #print(len(user_ids_dic[recipient_id]))

                except:

                    response_sent_text = "I ran out of arguments :) please go to the google form to complete the study: https://forms.gle/aqDtpUKcd2Xrd3A69"
                    send_message(recipient_id, response_sent_text)
                    timestamps[recipient_id].append(mes_time)
                    #adding last argument where no match was found to chatlog
                    log_mes= "User: " + user_mes
                    chat_logs[recipient_id].append(log_mes)

                    recipient_logs = chat_logs[recipient_id]
                    recipient_times = timestamps[recipient_id]

                    data = recipient_logs + recipient_times

                    pickle_file_name = pickle_path + recipient_id + ".pickle"
                    with open(pickle_file_name, 'wb') as handle:
                        pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)

                    return "ok"


            send_message(recipient_id, response_sent_text)
            log_mes= "User: " + user_mes
            chat_logs[recipient_id].append(log_mes)
            if response_id == 0:
                id_ = str(len(user_ids_dic[recipient_id]))
                rep_id = "Depth0_" + id_
                chatbot_response = "CB: " + rep_id
            else:
                chatbot_response = "CB: " + response_id
            chat_logs[recipient_id].append(chatbot_response)
            return "ok"




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
