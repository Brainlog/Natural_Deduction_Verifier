p = {"T","F"}
q = {"T","F"}
r = {"T","F"}
fil = open("q4a.txt",'w')
def change(p):
    if p == "T":
        return True
    else:
        return False
def c2(p):
    if p == True:
        return "T"
    else:
        return "F"
def f1(p,q,r):
    return r or (p or q)
def f2(p,q,r):
    return r and (not q)
def f3(p,q,r):
    return ((not r) or q)

fil.write("p q r 1 2 3\n")
for i in p:
    for j in q:
        for k in r:
            fil.write(i + " " + j + " " + k + " ")
            fil.write(c2(f1(change(i),change(j),change(k))) + " " + c2(f2(change(i),change(j),change(k))) + " " + c2(f3(change(i),change(j),change(k))) + "\n")