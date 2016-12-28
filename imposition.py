"""
Imposition example/test
"""
import pprint 

pp = pprint.PrettyPrinter()
nPages = 16

if nPages == 20:
    target = [
        [[20,1], [2,19]], #0
        [[18,3], [4,17]], #1
        [[16,5], [6,15]], #2
        [[14,7], [8,13]], #3
        [[12,9], [10,11]], #4
    ]
elif nPages == 8:
    target = [
        [[8,1], [2,7]], #0
        [[6,3], [4,5]], #1
    ]
else:
    target = ""

a = []
papers = nPages/4
for p in range(papers):
    p4 = nPages - (p * 2)
    p1 = p*2 + 1
    p2 = p1 + 1
    p3 = p4 - 1
    print(p, p1, p2, p3, p4)
    a.append([[p4, p1], [p2, p3]])
pp.pprint(target)
pp.pprint(a)

