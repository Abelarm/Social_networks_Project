from HITS import HITS2

simple = [[0, 1, 1, 1, 0], [1, 0, 0, 1, 0], [0, 0, 0, 0, 1], [0, 1, 1, 0, 0], [0, 0, 0, 0, 0]]

'''
time , a, h = HITS1(simple,1000)
print("Time:" + str(time))
print ("A: " + str(a))
print ("H: "+ str(h))
'''


# Graph is represented with its adjacency lists
simple = dict()
simple['x'] = {'y','z','w'}
simple['y'] = {'x','w'}
simple['z'] = {'k'}
simple['w'] = {'y','z'}
simple['k'] = {}


time , a, h = HITS2(simple,1000)
print("Time:" + str(time))
print ("A: " + str(a))
print ("H: "+ str(h))