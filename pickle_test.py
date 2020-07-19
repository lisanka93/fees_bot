import pickle


file = '/home/lisanka/fees_bot/chatlogs2/2056442987813807.pickle'

with open(file, 'rb') as handle:
    model_glove = pickle.load(handle)


print(model_glove)
