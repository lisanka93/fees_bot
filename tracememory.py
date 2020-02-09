#import tracemalloc
#import os
#import psutil
import pickle
"""



pid = os.getpid()
py = psutil.Process(pid)
memoryUse = py.memory_info()[0]/2.**30  # memory use in GB...I think
print('memory use:', memoryUse)
"""


@profile
def my_func():
    with open('glovedic.pickle', 'rb') as handle:
        model_glove = pickle.load(handle)

if __name__ == '__main__':
    my_func()

#tracemalloc.start()



"""
snapshot = tracemalloc.take_snapshot()
top_stats = snapshot.statistics('lineno')

print("[ Top 10 ]")
for stat in top_stats[:10]:
    print(stat)
"""
