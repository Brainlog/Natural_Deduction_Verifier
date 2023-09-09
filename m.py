dic = {"1":[1,2,[3]]}

def f(dic):
    dic["1"] = "hh"
    return

f(dic)

print(dic["1"])
l = frozenset([[1],2,3])
dic = {l:1}
print(dic)
dd = [1,2,3]
dd.pop()
print(dd)
# dd = [[1],[2]]
# dd = (frozenset(dd))

a = [[1,2,3],[4,5,6],[[["gg"]]]]
b = [[1,2,3],[4,5,6],[["gg"]]]
print(a==b)