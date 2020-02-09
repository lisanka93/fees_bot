
import pickle
from argdics import *

#con dic
with open('con_dic.pickle', 'wb') as handle:
    pickle.dump(con_dic, handle, protocol=pickle.HIGHEST_PROTOCOL)



#pro dic

with open('pro_df.pickle', 'rb') as handle:
    pro_df = pickle.load(handle)

pro_argument = list(pro_df['Argument'])
pro_ids = pro_df['arg_id']
pro_ids_prev = pro_df['prev_arg_id']
pro_arguments = list(zip(pro_argument, pro_ids, pro_ids_prev))

pro_dic = dict(zip(pro_ids, pro_argument))

with open('pro_dic.pickle', 'wb') as handle:
    pickle.dump(pro_dic, handle, protocol=pickle.HIGHEST_PROTOCOL)



#con arguments

with open('con_df.pickle', 'rb') as handle:
    con_df = pickle.load(handle)

con_argument = list(con_df['Argument'])
con_ids = con_df['arg_id']
con_ids_prev = con_df['prev_arg_id']
con_arguments = list(zip(con_argument, con_ids, con_ids_prev))

with open('con_arguments.pickle', 'wb') as handle:
    pickle.dump(con_arguments, handle, protocol=pickle.HIGHEST_PROTOCOL)
