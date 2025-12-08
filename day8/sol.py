from math import sqrt
import pickle
from functools import reduce

def load(fname):
    with open(fname,'rt') as f:
        data = f.readlines()
        data = [ tuple(x.split(',')) for x in data ]
        data = [ (int(x),int(y),int(z.strip())) for x,y,z in data ]
        return data

#boxlist = load('test-input.txt')
boxlist = load('input.txt')
boxlist.sort()

def dist(p,q):
    return sqrt( sum([ (x-y)**2 for x,y in zip(p,q) ]) )

def getdistmatrix(boxes):
    res = {}
    for p in boxes:
        tmp = {}
        for q in boxes:
            try:
                tmp[q] = (res[q][p][0],p)
            except:
                if p!=q:
                    tmp[q] = (dist(p,q),p)
        res[p] = tmp
    return res

def getboxesbydist(distmatrix):
    dists = []
    registered = set()
    for p in distmatrix:
        for q in distmatrix[p]:
            d,pp = distmatrix[p][q]
            if p!=pp:
                raise Exception("very very wrong")
            if (p,q) not in registered and (q,p) not in registered:
                #print(f'add boxes: sz:{d}, boxes: {p}, {q}')
                dists += [ (d,p,q) ]
                registered.add((p,q))
    return dists

#connection management
def isInConnection(conset,p):
    for subset in conset:
        if p in subset:
            return True
    return False

def addconnection(connections,p,q):
    pass

boxdists = getdistmatrix(boxlist)   
distances = getboxesbydist(boxdists)
distances.sort()
distances.reverse()

connections = set()
boxes = set(boxlist)

class Connections:
    def __init__(self):
        self.connections = []
        self.subsettable = dict()
    def add(self,p,q):
        s1 = self.findsubset(p)
        s2 = self.findsubset(q)
        if s1==s2:
            pass
        else:
            #print(self.connections,s1,self.connections.count(s1),s2,self.connections.count(s2))
            try:
                self.connections.remove(s1)
            except: pass
            try:
                self.connections.remove(s2)
            except: pass
            s = s1.union(s2)
            self.connections.append(s)
            for item in s:
                self.subsettable[item] = s
        return
    def findsubset(self,p):
        try:
            return self.subsettable[p]
        except:
            ss = {p}
            self.subsettable[p] = ss
            self.connections.append(ss)
            return ss
    def info(self):
        print('connections')
        for conset in self.connections:
            print(conset)
        print('per item')
        for p in self.subsettable:
            print(p,'..',self.subsettable[p])
        print('---------------')
    def evaluate(self,n):
        consizes = [ len(x) for x in self.connections ]
        consizes.sort()
        consizes.reverse()
        consizes = consizes[:n]
        return reduce(lambda x,y:x*y,consizes[:n],1)
    def allinsamecircuit(self):
        return len(self.connections)==1

def connectNshortest(distances,n):
    connections = Connections()
    for i in range(n):
        dist,p,q = distances.pop()
        connections.add(p,q)            
    return connections

if False:
    conn = connectNshortest(distances,1000)
    print('solution1',conn.evaluate(3))

def connectAll(distances,boxset):
    res = 0#value of last connection (p_x * q_x)
    connections = Connections()
    for dist in distances:
        dist,p,q = distances.pop()
        connections.add(p,q)
        try:
            boxset.remove(p)
        except: pass
        try:
            boxset.remove(q)
        except: pass
        if len(boxset)==0 and connections.allinsamecircuit():
            res = p[0] * q[0]
            break
    return res    

result = connectAll(distances,boxes)
print('solution2',result)
