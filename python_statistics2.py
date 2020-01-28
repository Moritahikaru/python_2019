import math
import statistics
import collections
L=[1,1,2,2,3,4,5,6,7,8,9,10,4,4,4,5,5,5]
i=collections.Counter(L).most_common()[0][0]
print(i)
