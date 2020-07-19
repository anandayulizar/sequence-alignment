from anytree import Node, RenderTree, AsciiStyle, PreOrderIter

f = Node((0,0))
b = Node((1, 1), parent=f)
a = Node((2, 2), parent=b)
d = Node((2, 1), parent=b)
c = Node((3, 1), parent=d)
e = Node((3, 2), parent=d)
g = Node((1, 2), parent=f)
i = Node((2, 3), parent=g)
h = Node((3, 1), parent=i)
print(RenderTree(f, style=AsciiStyle()))

for pre, _, node in RenderTree(f):
  print("%s%s" % (pre, node.name))