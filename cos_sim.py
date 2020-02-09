import numpy as np
#from sklearn.metrics.pairwise import cosine_similarity

# vectors
a = np.array([1,2,3])
b = np.array([1,1,4])

# manually compute cosine similarity
dot = np.dot(a, b)
norma = np.linalg.norm(a)
normb = np.linalg.norm(b)
cos = dot / (norma * normb)
print(cos)
