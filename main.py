import sys
from grammar import Lark_StandAlone,Transformer,v_args
from types import ModuleType
from typing import (
    TypeVar, Generic, Type, Tuple, List, Dict, Iterator, Collection, Callable, Optional, FrozenSet, Any,
    Union, Iterable, IO, TYPE_CHECKING, overload,
    Pattern as REPattern, ClassVar, Set, Mapping
)

inline_args = v_args(inline=True)

# Use json.lark to create the functions
class TreeToJson(Transformer):
    def __init__(self) -> None:
        self.premises = {}
        self.statement = {}
        self.conclusion = {}
        
    def natded(self, *args):
        (seq,proof) = args[0]
        return (seq,proof) # [[],__] First is list of premises, second is conclusion
    
    def sequent(self, *args):
        print("Sequent Started")
        print(args[0])
        print("Sequent Ended")
        return args[0]
    
    def formulaset(self, *args):
        print("Formula")
        print(args[0])
        print("Formula ended")
        return args[0]
    
    def proof(self, *args):
        print("Proof")
        print(args[0])
        print("Proof ended")
        return args[0]
    
    def proof_line(self, *args):
        print("Proof Line")
        l = args[0][0]
        r = args[0][1]
        l.append(r)
        print(l)
        print("Proof Line ended")
        return l
    
    def premise(self, *args):
        return ["premise"]
    
    def assumption(self, *args):
        return ["assumption"]
    
    def copy_op(self, *args):
        print("copy")
        print(args[0][0].value)
        print("copy ended")
        return ['copy',int(args[0][0].value)]
    
    def modus_ponens(self, *args):
        print("modus ponens")
        print(args)
        print("modus ponens ended")
        return ['modus ponens',int(args[0][0].value),int(args[0][1].value)]
        
    
    def and_intro(self, *args):
        print("and intro")
        print(args)
        print("and intro ended")
        return ['and intro',int(args[0][0].value),int(args[0][1].value)]
        
    
    def and_elim1(self, *args):
        print("and elim1")
        print(args)
        print("and elim1 ended")
        return ['and elim1',int(args[0][0].value)]
    
    def and_elim2(self, *args):
        print("and elim2")
        print(args)
        print("and elim2 ended")
        return ['and elim2',int(args[0][0].value)]
    
    def or_intro1(self, *args):
        print("or intro1")
        print(args)
        print("or intro1 ended")
        return ['or intro1',int(args[0][0].value)]
    
    def or_intro2(self, *args):
        print("or intro2")
        print(args)
        print("or intro2 ended")
        return ['or intro2',int(args[0][0].value)]
    
    def or_elim(self, *args):
        print("or elim")
        print(['or elim',int(args[0][0].value),args[0][1],args[0][2]])
        print("or elim ended")
        return ['or elim',int(args[0][0].value),args[0][1],args[0][2]]
    
    def impl_intro(self, *args):
        print("impl intro")
        print(['impl intro',args[0][0]])
        print("impl intro ended")
        return ['impl intro',args[0][0]]
    
    def neg_intro(self, *args):
        print("neg intro")
        print(['neg intro',args[0][0]])
        print("neg intro ended")
        return ['neg intro',args[0][0]]
    
    def neg_elim(self, *args):
        print("neg elim")
        print(['neg elim',int(args[0][0].value),int(args[0][1].value)])
        print("neg elim ended")
        return ['neg elim',int(args[0][0].value),int(args[0][1].value)]
    
    def bot_elim(self, *args):
        print("bot elim")
        print(['bot elim',int(args[0][0].value)])
        print("bot elim ended")
        return ['bot elim',int(args[0][0].value)]
    
    def d_neg_intro(self, *args):
        print("d neg intro")
        print(['d neg intro',int(args[0][0].value)])
        print("d neg intro ended")
        return ['d neg intro',int(args[0][0].value)]
    
    def d_neg_elim(self, *args):
        print("d neg elim")
        print(['d neg elim',int(args[0][0].value)])
        print("d neg elim ended")
        return ['d neg elim',int(args[0][0].value)]
    
    def proof_by_contra(self, *args):
        print("proof by contra")
        print(['proof by contra',args[0][0]])
        print("proof by contra ended")
        return ['proof by contra',args[0][0]]
    
    def lem(self, *args):
        return ['lem']
    
    def num_range(self, *args):
        print("num range")
        print([int(args[0][0].value),int(args[0][1].value)])
        print("num range ended")
        return [int(args[0][0].value),int(args[0][1].value)]
        
    
    def atomic_prop(self, *args):
        return [args[0][0].value]
    
    def and_op(self, *args):
        l = ['A']
        l.append(args[0][0])
        l.append(args[0][1])
        return l
    
    def or_op(self, *args):
        l = ['O']
        l.append(args[0][0])
        l.append(args[0][1])
        return l
    
    def implies_op(self, *args):
        l = ['I']
        l.append(args[0][0])
        l.append(args[0][1])
        print(l)
        return l
    
    def not_op(self, *args):
        l = ['N']
        l.append(args[0][0])
        return l
    
    def bottom(self, *args):
        l = ['B']
        return l

parser = Lark_StandAlone(transformer=TreeToJson())

def orel(proofs,scopesend,prooflist):
    # [__,__,[],[]]
    scopestarts = []
    for i in range(len(proofs)):
        if(proofs[i][0]=='or elim'):
            range1 = proofs[i][2][0]
            range1end = proofs[i][2][1]
            range2 = proofs[i][3][0]
            range2end = proofs[i][3][1]
            if prooflist[int(range1)][0]!='assumption' or prooflist[int(range2)][0]!='assumption':
                return None
            scopestarts.append(range1)
            scopestarts.append(range2)
            if range1 in scopesend:
                scopesend[range1].append(range1end)
            else:
                scopesend[range1] = [range1end]
            if range2 in scopesend:
                scopesend[range2].append(range2end)
            else:
                scopesend[range2] = [range2end]
    return scopestarts
            

def implin(proofs, scopesend,prooflist):
    # [__,[]]
    scopesstarts = []
    for i in range(len(proofs)):
        if(proofs[i][0]=='impl intro'):
            range1 = proofs[i][1][0]
            range1end = proofs[i][1][1]
            if prooflist[int(range1)][0]!='assumption':
                return None
            scopesstarts.append(range1)
            if range1 in scopesend:
                scopesend[range1].append(range1end)
            else:
                scopesend[range1] = [range1end]
    return scopesstarts
            
    

def negin(proofs, scopesend,prooflist):
    scopesstarts = []
    for i in range(len(proofs)):
        if(proofs[i][0]=='neg intro'):
            range1 = proofs[i][1][0]
            range1end = proofs[i][1][1]
            if prooflist[int(range1)][0]!='assumption':
                return None
            scopesstarts.append(range1)
            if range1 in scopesend:
                scopesend[range1].append(range1end)
            else:
                scopesend[range1] = [range1end]
    return scopesstarts

def pbc(proofs, scopesend,prooflist):
    scopesstarts = []
    for i in range(len(proofs)):
        if(proofs[i][0]=='proof by contra'):
            range1 = proofs[i][1][0]
            range1end = proofs[i][1][1]
            if prooflist[int(range1)][0]!='assumption':
                return None
            scopesstarts.append(range1)
            if range1 in scopesend:
                scopesend[range1].append(range1end)
            else:
                scopesend[range1] = [range1end]
    return scopesstarts  

def assume(proofs):
    scopestarts = []
    for i in range(len(proofs)):
        if(proofs[i][0]=='assumption'):
            scopestarts.append(i+3)
    return scopestarts
            

def scopesending(scopes_end):
    temp = []
    for (key,value) in scopes_end.items():
        value = list(set(value))
        value.sort()
        if(len(value)>1):
            return 0
        temp.append([key,value[0]])
    print(temp)
    for i in range(len(temp)):
        for j in range(len(temp)):
            if(i!=j):
                chk1 = (temp[i][0]==temp[j][0] and temp[i][1] > temp[j][1])
                chk2 = (temp[i][0]==temp[j][0] and temp[i][1] < temp[j][1])
                chk3 = (temp[i][0]>temp[j][0] and temp[i][1] == temp[j][1])
                chk4 = (temp[i][0]<temp[j][0] and temp[i][1] == temp[j][1])
                chk5 = (temp[i][0]<temp[j][0] and temp[j][0] < temp[i][1] and temp[j][1]>temp[i][1])
                chk6 = (temp[i][0]>temp[j][0] and temp[i][0] < temp[j][1] and temp[i][1]>temp[j][1])
                if chk1 or chk2 or chk3 or chk4 or chk5 or chk6:
                    return 0
    # chking dictionary, every element length shuould be one (First do stable sort)
    return 1

def scopechking(scopes_got,actual_scopes):
    scopes_got.sort()
    actual_scopes.sort()
    print(scopes_got)
    print(actual_scopes)
    if(scopes_got!=actual_scopes):
        return 0
    # chking list same 
    return 1

## Need all proof checkers
## Run a stack (whenever start a scope (when reach assumption statement))
def listfind(elem,stk):
    for i in range(len(stk)):
        if(stk[i]==elem):
            return 1
    return 0

def listequalcheck(l1,l2):
    if(l1==l2):
        return 1
    else:
        return 0
    
def premisecheck(prooflist,proof,verifstack,premises):
    for i in range(len(premises)):
        if(premises[i]==proof[1]):
            return 1
    return 0

def assumptioncheck(prooflist,proof,verifstack):
    pass

def copycheck(prooflist,proof,verifstack):
    chk1 = 0
    chk2 = 0
    linenum = int(proof[1])
    chk2 = (listfind(linenum,verifstack))
    if chk2 == 1:
        formulacopied = prooflist[linenum][-1]
        formulamy = proof[-1]
        try:
            chk2 = (formulamy==formulacopied)
        except:
            return 0
    return chk1 and chk2        

def modusponenscheck(prooflist,proof,verifstack):
    chk1 = 0
    chk2 = 0
    linenum1 = int(proof[1])
    linenum2 = int(proof[2])
    chk1 = (listfind(linenum1,verifstack)) and (listfind(linenum2,verifstack))
    if chk1 == 1:
        formula1 = prooflist[linenum1][-1] ## a
        formula2 = prooflist[linenum2][-1] ## a -> b
        formula3 = proof[-1] ## b
        try:
            chk2 = (formula2[0]=='I') and (formula1 == formula2[1]) and (formula3 == formula2[2])
        except:
            return 0
    return chk1 and chk2
    
def andintrocheck(prooflist,proof,verifstack):
    chk1 = 0
    chk2 = 0
    linenum1 = int(proof[1])
    linenum2 = int(proof[2])
    chk1 = (listfind(linenum1,verifstack)) and ((listfind(linenum2,verifstack)))
    if chk1 == 1:
        formula1 = prooflist[linenum1][-1] ## a
        formula2 = prooflist[linenum2][-1] ## b
        formula3 = proof[-1] ## 'A' a b
        try:
            chk2 = (formula3[0]=='A') and (formula1 == formula3[0]) and (formula2 == formula3[1])
        except:
            return 0
    return chk1 and chk2
    

def andelim1check(prooflist,proof,verifstack):
    chk1 = 0
    chk2 = 0
    linenum1 = int(proof[1])
    chk1 = (listfind(linenum1,verifstack))
    if chk1 == 1:
        formula1 = prooflist[linenum1][-1] ## a /\ b
        formula2 = proof[-1] ## a
        try:
            chk2 = (formula1[0]=='A') and (formula2 == formula1[1])
        except:
            return 0
    return chk1 and chk2

def andelim2check(prooflist,proof,verifstack):
    chk1 = 0
    chk2 = 0
    linenum1 = int(proof[1])
    chk1 = (listfind(linenum1,verifstack))
    if chk1 == 1:
        formula1 = prooflist[linenum1][-1] ## a /\ b
        formula2 = proof[-1] ## b
        try:
            chk2 = (formula1[0]=='A') and (formula2 == formula1[2])
        except:
            return 0
    return chk1 and chk2

def orintro1check(prooflist,proof,verifstack):
    chk1 = 0
    chk2 = 0
    linenum1 = int(proof[1])
    chk1 = (listfind(linenum1,verifstack))
    if chk1 == 1:
        formula1 = prooflist[linenum1][-1] ## a
        formula2 = proof[-1] ## a \/ b
        try:
            chk2 = (formula2[0]=='O') and (formula2[1]==formula1)
        except:
            return 0
    print("chk1 : ",chk1)
    print("chk2 : ",chk2)
    return chk1 and chk2
    

def orintro2check(prooflist,proof,verifstack):
    chk1 = 0
    chk2 = 0
    linenum1 = int(proof[1])
    chk1 = (listfind(linenum1,verifstack))
    if chk1 == 1:
        formula1 = prooflist[linenum1][-1] ## b
        formula2 = proof[-1] ## a \/ b => 'O' a b
        try:
            chk2 = (formula2[0]=='O') and (formula2[2]==formula1)
        except:
            return 0
    return chk1 and chk2

def orelimcheck(prooflist,proof,verifstack):    
    chk1 = 0
    chk2 = 0
    range1 = proof[2] ## p ---> q
    range2 = proof[3] ## r ---> q
    linenum1 = proof[1] ## p \/ r => 'O' p r
    linenum2 = range1[0] ## p
    linenum3 = range1[1] ## q
    linenum4 = range2[0] ## r
    linenum5 = range2[1] ## q
    chk1 = (listfind(range1,verifstack)) and (listfind(range2,verifstack)) and (listfind(linenum1,verifstack))
    if chk1 == 1:
        formula1 = prooflist[linenum1][-1]
        formula2 = prooflist[linenum2][-1]
        formula3 = prooflist[linenum3][-1]
        formula4 = prooflist[linenum4][-1]
        formula5 = prooflist[linenum5][-1]
        formula6 = proof[-1] ## q
        try:
            chk2 = (formula1[0]=='O') and (formula1[1]==formula2) and (formula1[2]==formula4) and (formula3 == formula6) and (formula5 == formula6)
        except:
            return 0
    return chk1 and chk2     
    

def implintrocheck(prooflist,proof,verifstack):
    chk1 = 0
    chk2 = 0
    range1 = proof[1]  ## p --> q
    linenum1 = range1[0] ## p
    linenum2 = range1[1] ## q
    chk1 = (listfind(range1,verifstack))
    if chk1 == 1:
        formula1 = prooflist[linenum1][-1] ##p
        formula2 = prooflist[linenum2][-1] ##q
        formula3 = proof[-1] ## p -> q => 'I' p q
        try:
            chk2 = (formula3[0]=='I') and (formula1==formula3[1]) and (formula2==formula3[2])
        except:
            return 0
    print("implication intro : chk1 : ",chk1)
    print("implication intro : chk2 : ",chk2)
    return chk1 and chk2
        

def negintrocheck(prooflist,proof,verifstack):
    chk1 = 0
    chk2 = 0
    range1 = proof[1] ## p --> B 
    linenum1 = range1[0] ## p
    linenum2 = range1[1] ## Bottom
    chk1 = (listfind(range1,verifstack))
    if chk1 == 1:
        formula1 = prooflist[linenum1][-1] ## p
        formula2 = prooflist[linenum2][-1] ## B
        formula3 = proof[-1] ## !p => 'N' p
        try:
            chk2 = (formula3[0]=='N') and formula3[0]==formula1 and formula3[1] == formula2 and formula2 == ['B']
        except:
            return 0
    return chk1 and chk2

def negelimcheck(prooflist,proof,verifstack):
    chk1 = 0
    chk2= 0
    linenum1 = proof[1]
    linenum2 = proof[2]
    chk1 = (listfind(linenum1,verifstack)) and (listfind(linenum2,verifstack))
    if chk1 == 1:
        formula1 = prooflist[linenum1][-1] ## p
        formula2 = prooflist[linenum2][-1] ## !p => N p
        formula3 = proof[-1] ## ['B']
        try:
            chk2 = (formula3 == ['B']) and (formula2[1]==formula1) and (formula2[0]=='N')
        except:
            return 0
    return chk1 and chk2

def botelimcheck(prooflist,proof,verifstack):
    chk1 = 0
    chk2 = 0
    linenum1 = proof[1]
    chk1 = listfind(linenum1,verifstack)
    if chk1 == 1:
        formula1 = prooflist[linenum1][-1] ## ['B']
        try:
            chk2 = (formula1 == ['B'])
        except:
            return 0
    return chk1 and chk2

def dnegintrocheck(prooflist,proof,verifstack):
    chk1 = 0
    chk2 = 0
    linenum1 = proof[1]
    chk1 = listfind(linenum1,verifstack)
    if chk1 == 1:
        formula1 = prooflist[linenum1][-1] ## p
        formula2 = proof[-1] ## ! (! p) => N,[N,p]
        try:
            chk2 = (formula2[0]=='N') and (formula2[1][0]=='N') and (formula2[1][1]==formula1)
        except:
            return 0
    return chk1 and chk2

def dnegelimcheck(prooflist,proof,verifstack):
    chk1 = 0
    chk2 = 0
    linenum1 = proof[1]
    chk1 = listfind(linenum1,verifstack)
    if chk1 == 1:
        formula1 = proof[-1] ## ! (! p) => N,[N,p]
        formula2 = prooflist[linenum1][-1] ## p
        try:
            chk2 = (formula1[0]=='N') and (formula1[1][0]=='N') and (formula1[1][1]==formula2)
        except:
            return 0
    return chk1 and chk2

def proofbycontracheck(prooflist,proof,verifstack):
    chk1 = 0
    chk2 = 0
    range1 = proof[1] ## p --> bottom
    linenum1 = range1[0] ## p
    linenum2 = range1[1] ## ['B']
    chk1 = listfind(range1,verifstack)
    if chk1 == 1:
        formula1 = prooflist[linenum1][-1] ## p
        formula2 = prooflist[linenum2][-1] ## ['B']
        formula3 = proof[-1] ## ! p => N p
        try:
            chk2 = (formula1 == formula3[1]) and (formula3[0]=='N') and (formula2 == ['B']) 
        except:
            return 0
    return chk1 and chk2
        

def lemcheck(prooflist,proof,verifstack):
    chk1 = 0
    formula1 = proof[-1] ## \/ p [N p] 
    try:
        chk1 = (formula1[0]=='O') and (formula1[1]==formula1[2][1]) and (formula1[2][0]=='N')
    except:
        return 0
    return chk1
    
    

def verifier():
    debug = False
    if len(sys.argv)==3:
        debug = True
    with open(sys.argv[1]) as f:
        s = f.read()
        (seq,proofs) =(parser.parse(s))
        premises = seq[0]
        conclusion = seq[1]
        if(debug):
            print("premises : ",premises)
            print("conclusion : ",conclusion)
            print("proofs : ",proofs)
        prooflist = [0,0,0]
        prooflist.extend(proofs)
        scopes_end = {}
        scopes_got = orel(proofs,scopes_end,prooflist)
        scopes_got += implin(proofs,scopes_end,prooflist)
        scopes_got += negin(proofs,scopes_end,prooflist)
        scopes_got += pbc(proofs,scopes_end,prooflist)
        scopes = assume(proofs)
        if(scopesending(scopes_end)==0):
            if debug:
                print("Scope are not completely overlapping")
            print("incorrect")
            return
        else:
            scopes_got.sort()
            scopes.sort()
            if(scopechking(scopes_got,scopes)==0):
                if debug:
                    print("Assumption Box is not ended")
                print("incorrect")
                return
            else:
                ## Use this prooflist now
                verifstack = []
                scopeendstack = []
                for i in range(3,len(prooflist)):
                    myproof = prooflist[i]
                    if(myproof[0]=='premise'):
                        chk =premisecheck(prooflist,myproof,verifstack,premises)
                        if(chk == 0):
                            if debug:
                                print(f"Premise Line no. {i} not found")
                            print("incorrect")
                            return
                        else:
                            verifstack.append(i)
                            
                    if(myproof[0]=='assumption'):
                        verifstack.append("|") ## To mark scope start
                        scopeendstack.append(int(scopes_end[i][0])) ## To mark scope end => (key,[ending])
                        verifstack.append(i)
                        
                    
                    if(myproof[0]=='copy'):
                        chk = copycheck(prooflist,myproof,verifstack)
                        if(chk == 0):
                            if debug:
                                print(f"Copying Line no. {i} is wrong")
                            print("incorrect")
                            return
                        else:
                            verifstack.append(i)
                    
                    if(myproof[0]=='modus ponens'):
                        chk = modusponenscheck(prooflist,myproof,verifstack)
                        if(chk == 0):
                            if debug:
                                print(f"Copying Line no. {i} is wrong")
                            print("incorrect")
                            return
                        else:
                            verifstack.append(i)
                    
                    
                    if(myproof[0]=='and intro'):
                        chk = andintrocheck(prooflist,myproof,verifstack)
                        if(chk == 0):
                            if debug:
                                print(f"Copying Line no. {i} is wrong")
                            print("incorrect")
                            return
                        else:
                            verifstack.append(i)
                    
                    
                    if(myproof[0]=='and elim1'):
                        chk = andelim1check(prooflist,myproof,verifstack)
                        if(chk == 0):
                            if debug:
                                print(f"Copying Line no. {i} is wrong")
                            print("incorrect")
                            return
                        else:
                            verifstack.append(i)
                    
                    
                    if(myproof[0]=='and elim2'):
                        chk = andelim2check(prooflist,myproof,verifstack)
                        if(chk == 0):
                            if debug:
                                print(f"Copying Line no. {i} is wrong")
                            print("incorrect")
                            return
                        else:
                            verifstack.append(i)
                    
                    
                    if(myproof[0]=='or intro1'):
                        print("This is stack : ",verifstack)
                        chk = orintro1check(prooflist,myproof,verifstack)
                        if(chk == 0):
                            if debug:
                                print(f"Copying Line no. {i} is wrong")
                            print("incorrect")
                            return
                        else:
                            verifstack.append(i)
                    
                    
                    if(myproof[0]=='or intro2'):
                        chk = orintro2check(prooflist,myproof,verifstack)
                        if(chk == 0):
                            if debug:
                                print(f"Copying Line no. {i} is wrong")
                            print("incorrect")
                            return
                        else:
                            verifstack.append(i)
                    
                    
                    if(myproof[0]=='or elim'):
                        chk = orelimcheck(prooflist,myproof,verifstack)
                        if(chk == 0):
                            if debug:
                                print(f"Copying Line no. {i} is wrong")
                            print("incorrect")
                            return
                        else:
                            verifstack.append(i)
                    
                    
                    if(myproof[0]=='impl intro'):
                        print("This is stack : ",verifstack)
                        chk = implintrocheck(prooflist,myproof,verifstack)
                        if(chk == 0):
                            if debug:
                                print(f"Copying Line no. {i} is wrong")
                            print("incorrect")
                            return
                        else:
                            verifstack.append(i)
                    
                    
                    if(myproof[0]=='neg intro'):
                        chk = negintrocheck(prooflist,myproof,verifstack)
                        if(chk == 0):
                            if debug:
                                print(f"Copying Line no. {i} is wrong")
                            print("incorrect")
                            return
                        else:
                            verifstack.append(i)
                    
                    
                    if(myproof[0]=='neg elim'):
                        chk = negelimcheck(prooflist,myproof,verifstack)
                        if(chk == 0):
                            if debug:
                                print(f"Copying Line no. {i} is wrong")
                            print("incorrect")
                            return
                        else:
                            verifstack.append(i)
                    
                    
                    if(myproof[0]=='bot elim'):
                        chk = botelimcheck(prooflist,myproof,verifstack)
                        if(chk == 0):
                            if debug:
                                print(f"Copying Line no. {i} is wrong")
                            print("incorrect")
                            return
                        else:
                            verifstack.append(i)
                    
                    
                    if(myproof[0]=='d neg intro'):
                        chk = dnegintrocheck(prooflist,myproof,verifstack)
                        if(chk == 0):
                            if debug:
                                print(f"Copying Line no. {i} is wrong")
                            print("incorrect")
                            return
                        else:
                            verifstack.append(i)
                    
                    
                    if(myproof[0]=='d neg elim'):
                        chk = dnegelimcheck(prooflist,myproof,verifstack)
                        if(chk == 0):
                            if debug:
                                print(f"Copying Line no. {i} is wrong")
                            print("incorrect")
                            return
                        else:
                            verifstack.append(i)
                    
                    
                    if(myproof[0]=='proof by contra'):
                        chk = proofbycontracheck(prooflist,myproof,verifstack)
                        if(chk == 0):
                            if debug:
                                print(f"Copying Line no. {i} is wrong")
                            print("incorrect")
                            return
                        else:
                            verifstack.append(i)
                    
                    
                    if(myproof[0]=='lem'):
                        chk = lemcheck(prooflist,myproof,verifstack)
                        if(chk == 0):
                            if debug:
                                print(f"Copying Line no. {i} is wrong")
                            print("incorrect")
                            return
                        else:
                            verifstack.append(i)
                    
                    
                    if(len(scopeendstack)>0):
                        if(i == scopeendstack[-1]):
                            tempstack = []
                            while(verifstack[-1]!='|'):
                                tempstack.append(verifstack[-1])
                                verifstack.pop()
                            verifstack.pop()
                            verifstack.append([tempstack[-1],i])
                            scopeendstack.pop()
                    
                    print("Current Stack After Action : ",verifstack)
                    print("Current Scope ending : ",scopeendstack)
                    
                print("correct")
verifier()     
