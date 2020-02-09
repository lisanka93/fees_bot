import pandas as pd
import pickle
"""
depth1_file = 'graph_depth1.csv'
depth1_df = pd.read_csv(depth1_file,encoding='latin-1')

depth2_file = 'graph_depth2.csv'
depth2_df = pd.read_csv(depth2_file,encoding='latin-1')

depth3_file = 'graph_depth3.csv'
depth3_df = pd.read_csv(depth3_file, encoding='latin-1')

depth4_file = 'graph_depth4.csv'
depth4_df = pd.read_csv(depth4_file,encoding='latin-1')

depth5_file = 'graph_depth5.csv'
depth5_df = pd.read_csv(depth5_file,encoding='latin-1')
"""


#print(tony_args)
#frames = [depth1_df, depth2_df, depth3_df, depth4_df, depth5_df]
#for prodepth - not needed for chatbot
pro_depth1_file = 'pro_depth1_labeledconcerns.csv'
pro_depth1_df = pd.read_csv(pro_depth1_file,encoding='latin-1')
pro_depth1_arguments = list(pro_depth1_df['arg'])
pro_depth1_ids = pro_depth1_df['arg_id']
pro_depth1_prev = pro_depth1_df['prev_arg_id']
pro_depth1_all = list(zip(pro_depth1_arguments,pro_depth1_ids, pro_depth1_prev))
pro_depth1_dic = dict(zip(pro_depth1_ids, pro_depth1_arguments))


#con_frames = [depth1_df, depth3_df]
#pro_frames = [depth2_df, depth4_df]
#all_frames= pd.concat([depth1_df, depth3_df, depth2_df, depth4_df, depth5_df])
#print(all_frames)

with open('con_df.pickle', 'rb') as handle:
    con_df = pickle.load(handle)
with open('pro_df.pickle', 'rb') as handle:
    pro_df = pickle.load(handle)

with open('all_frames.pickle', 'rb') as handle:
    all_frames = pickle.load(handle)


all_arguments = list(all_frames['Argument'])
all_ids = list(all_frames['arg_id'])
all_arguments_list = list(zip(all_arguments, all_ids))


#need al frames!

#pro_df = pd.concat(pro_frames)
#con_df = pd.concat(con_frames)
"""
with open('con_df.pickle', 'wb') as handle:
    pickle.dump(con_df, handle, protocol=pickle.HIGHEST_PROTOCOL)

with open('pro_df.pickle', 'wb') as handle:
    pickle.dump(pro_df, handle, protocol=pickle.HIGHEST_PROTOCOL)

with open('all_frames.pickle', 'wb') as handle:
    pickle.dump(all_frames, handle, protocol=pickle.HIGHEST_PROTOCOL)

"""


pro_argument = list(pro_df['Argument'])
pro_ids = pro_df['arg_id']
pro_ids_prev = pro_df['prev_arg_id']
pro_arguments = list(zip(pro_argument, pro_ids, pro_ids_prev))

pro_dic = dict(zip(pro_ids, pro_argument))


con_argument = list(con_df['Argument'])
con_ids = con_df['arg_id']
con_ids_prev = con_df['prev_arg_id']
con_arguments = list(zip(con_argument, con_ids, con_ids_prev))
