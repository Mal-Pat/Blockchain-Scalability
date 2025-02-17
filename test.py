import numpy as np
import matplotlib.pyplot as plt


d = {}
print(d)

d[1] = 3
print(d)

d[1] = 4
print(d)

d[0] = 2
print(d)

d[2] = {}
d[2][0] = 9
print(d)

print(max(list(d)))

'''
l = [1,2,3,4]

for _ in range(len(l)):
    i = l.pop(0)
    print(i)
    l.append(5)

print(l)
'''
'''
data = []
for i in range(100):
    a = 5000*np.random.beta(10,2.5)
    print(f"a = {a}")
    print(f"a' = {round(a)}")
    data.append(round(a))

plt.hist(data, 100)
plt.show()
'''