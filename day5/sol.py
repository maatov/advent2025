import re
from functools import reduce

def readinput(fname):
    freshranges = []
    ingredients = []
    with open(fname,'rt') as f:
        for l in f:
            res = re.match("(\\d+)-(\\d+)",l)
            if res:
                freshranges.append(range(int(res[1]),int(res[2])+1))
            res = re.match("^(\\d+)$",l)
            if res:
                ingredients.append(int(res[1]))
    return freshranges,ingredients

#freshs, ingreds = readinput('test-input.txt')
freshs, ingreds = readinput('input.txt')

def countFreshIngreds(freshdef,ingreds):
    tots = 0
    for ing in ingreds:
        for fdef in freshdef:
            if ing in fdef:
                tots += 1
                break
    return tots

res = countFreshIngreds(freshs,ingreds)
print('solution1',res)

def unionoftwo(r1,r2):
    s1,e1 = min(r1,r2)
    s2,e2 = max(r1,r2)
    if s2<=e1+1:
        #intersects or 'touch'
        return [(s1,max(e1,e2))]
    else:
        #othwise
        return [(s1,e1),(s2,e2)]

class SetCust:
    def __init__(self):
        self.subsets = []
    def unionwith(self,rset):
        pass
    def append(self,interval):
        #print(f"adding new interval [{interval}]")
        for item in self.subsets:
            if self.joinable(item,interval):
                #print('joining with existing int:',item)
                self.joinwith(item,interval)
                break
        else:
            #print('adding new int:',interval)
            self.subsets.append(interval)
            self.subsets.sort()
        pass
    def joinwith(self,originalitem,newone):
        self.subsets.remove(originalitem)
        self.subsets.append(unionoftwo(originalitem,newone)[0])
        self.subsets.sort()
    def joinable(self,i1,i2):
        s1,e1 = i1
        s2,e2 = i2
        return s2>=s1 and s2<=e1+1 or s1>=s2 and s1<=e2+1    
    def size(self):
        return sum([ e-s+1 for (s,e) in self.subsets ])
  

def rerange(freshdef):
    fdcopy = [(x.start,x.stop-1) for x in freshdef]
    fdcopy.sort()
    intervals = []
    setint = SetCust()    
    for r in fdcopy:
        setint.append(r)
    #print(intervals)
    return setint
    
res = rerange(freshs).size()
print('solution2',res)
