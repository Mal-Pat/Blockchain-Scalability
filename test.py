'''
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
'''

l = [1,2,3,4]

for _ in range(len(l)):
    i = l.pop(0)
    print(i)
    l.append(5)

print(l)
