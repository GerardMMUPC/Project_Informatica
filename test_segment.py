from Node import*
from Segment import*

n1 = Node('aaa', 0, 0)
n2 = Node('bbb', 3, 4)
n3 = Node('ccc', 6, 8)
seg1 = Segment('1-2', n1, n2)
seg2 = Segment('2-3', n2, n3)

print(seg1)
print(seg2)