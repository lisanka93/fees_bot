from argdics import *
from load_data import *
#rom text_preprocessing import *


def most_similar(argument, argument_list=con_arguments):
    for arg in argument_list:
        #print(arg[0])
        sim = cosine_distance_wordembedding_method(arg[0], argument)
        #print(sim)
        if sim < 100 and sim >= 95:
            #print('most sim: ', arg[0])
            return arg[1]


    #second iteration if no match found
    for arg in argument_list:
        #print(arg[0])
        sim = cosine_distance_wordembedding_method(arg[0], argument)
        #print(sim)
        if sim >= 90:
            print('most sim: ', arg[0])
            return arg[1]

    #just checking whether there is an argument of the opposite stance with a lot of similarity
    #then this could potentially be used as counterargument
    """
    for arg in pro_arguments:
        sim = cosine_distance_wordembedding_method(arg[0], argument)

        if sim >= 85:
            print('most sim: ', arg[0])
            #return arg[1]
    """
    return "no arg"

def most_similar_a(argument, argument_list):
    most_similar = []
    for arg in argument_list:
        #print(arg[0])
        sim = cosine_distance_wordembedding_method(arg[0], argument)
        #print(sim)
        if sim < 100 and sim >= 87:
            #print('most sim: ', arg[0])
            most_similar.append(arg[0])

    return most_similar
"""
for arg in tony_args:

    a = arg[0]
    similar_args = most_similar_a(a, all_arguments_list)  #pro_argumentsS
    if similar_args == []:
        print('not found:', arg[1])
    else:
        print(a)
        print(similar_args)
    print()
"""

def return_arg(user_mes):
    most_sim_id = most_similar(user_mes)
    if most_sim_id == "no arg":
        #print('chatbot: ', "no arg")
        return("no argument")
    else:

        possible_responses = con_dic[most_sim_id]
        con_dic[most_sim_id] = con_dic[most_sim_id][1:]
        response_id = possible_responses[0]
        chatbot_reply = pro_dic[response_id]

    return(chatbot_reply)

#loans are a big burden for students and put pressure on them. they graduate with high debt even before starting a job
