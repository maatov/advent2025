
def load(fname):
    with open(fname,'rt') as f:
        inp = []
        for line in f:
            inp += [ tuple([int(x) for x in line.split(',')]) ]
    return inp


#inp = load('test-input.txt')
inp = load('input.txt')

def squarearea(p,q):
    x,y = p
    xx,yy =  q
    return (abs(xx-x)+1)*(abs(yy-y)+1)

def getsquareareas(listofreds):
    size = len(listofreds)
    sqrarealist = []
    for r in range(size):
        for r2 in range(r,size):
            node1 = listofreds[r]
            node2 = listofreds[r2]
            sqrarealist += [ (squarearea(node1, node2),node1,node2) ]
    return sqrarealist    

def maxsquarearea(listofreds):
    return max([ x for x,y,z in getsquareareas(listofreds)])

def getsortedsquarearealist(listofreds):
    l = sorted([ (x,y,z) for x,y,z in getsquareareas(listofreds)])    
    return l

sortedsqareas = getsortedsquarearealist(inp)
print('solution1',sortedsqareas[-1][0])

def createPath(nodelist):
    path = []
    node1 = nodelist[0]
    for node in nodelist[1:]:
        path.append( (node1,node) )
        node1 = node
    path += [ (nodelist[-1], nodelist[0] ) ]
    return path

def getRelevantLineList(nodelist):
    return sorted([x for x,y in nodelist])

class LineDef:
    def __init__(self,linenum):
        self.line = linenum
        self.greendots = set() #Pairs from-to (included), 
        self.lines = set() #when filled
    def add(self,linepair):
        self.greendots.add(linepair)
    def fill(self,lfreference):
        #should be called from top. LineDef(green or no) will be consulted by line before
        #1st check if it was defined like line before just copy
        #print(self.line,' filling ', self.greendots, self.lines)
        if self.greendots==lfreference.greendots:
            self.lines = lfreference.lines
            #print('just copy',self.line,self.lines,[],lfreference.line)
            return
        dots = []
        self.lines = set()
        for item in self.greendots:
            if type(item)==type((0,0)):
                self.lines.add(item)
            else:
                dots.append(item)
        dots.sort()
        #print(dots)
        # no color -> anchor1 ? -> ? anchor2 -> ..
        dot1 = dots[0]
        for dot in dots[1:]:
            middlepoint = dot1+(dot-dot1)//2
            if lfreference.isIn(middlepoint):
                self.lines.add((dot1,dot))
            dot1 = dot
        #print('line defined:',self.line,self.lines,dots,lfreference.line)
        self.joinsetsifneeded()
        #print('afterjoin',self.line,self.lines,dots,lfreference.line)
        return
    def isIn(self,point):
        return any([x<=point <=y for x,y in self.lines])
    def isLineIn(self,s,e):
        ss = min(s,e)
        ee = max(s,e)
        for interval in self.lines:
            x,y = interval
            if ss>=x and ee<=y:
                return True
        return False
    def __repr__(self):
        return f"{self.line}:{len(self.greendots)}"
    def info(self):
        print(repr(self))
        for i in self.lines:
            print(i)
        print('--------------')
    def joinsetsifneeded(self):
        if len(self.lines)<2:
            return
        joined  = set()
        originallines = sorted(list(self.lines))
        lines = list(self.lines.copy())
        tmpint = lines[0]
        for intv in lines[1:]:
            x,y = tmpint
            xx,yy = intv
            if y==xx:
                tmpint = (x,yy)
            else:
                joined.add(tmpint)
                tmpint = intv
        joined.add(tmpint)
        self.lines = joined
        return
    
class FloorDef:
    def __init__(self):
        pass
        
def getHline(f,t):
    (x,y),(xx,yy) = f,t
    return (min(y,yy),max(y,yy))

def getVline(f,t):
    (x,y),(xx,yy) = f,t
    return (min(x,xx),max(x,xx))

def addHline(fdef,num,f,t):
    try:
        fdef[num].add(getHline(f,t))
    except:
         lf = LineDef(num)
         lf.add(getHline(f,t))
         fdef[num] = lf
    return fdef

def addVline(fdef,f,t,relevantLineSet):
    #asserting f[1]==t[1]
    if f[1]!=t[1]:
        raise Exception("assertion failed on points")
    pointy = f[1]
    linef,linet = getVline(f,t)
    indexes = set(range(linef,linet+1)).intersection(relevantLineSet)
    for i in indexes:
        try:
            fdef[i].add( pointy )
        except:
            tmp = LineDef(i)
            tmp.add(pointy)
            fdef[i] = tmp

def writefloordef(paths,relevantLineSet):
    floordef = dict()
    for path in paths:
        f,t = path
        x,y = f
        xx,yy = t
        if x==xx:
            #horizontal
            addHline(floordef,x,f,t)
        else:
            #vertical
            addVline(floordef,f,t,relevantLineSet)
    return floordef

def fillFloor(floordef):
    keys = sorted(floordef.keys())
    tmp = floordef[keys[0]] #should have only one interval
    #print(tmp)
    tmp.fill(LineDef(0)) #dummy line before
    #tmp.info()
    for key in keys[1:]:
        linedef = floordef[key]
        linedef.fill(tmp)
        tmp = linedef
    return floordef

def evaluate(floordef,square,lineSet):
    #print('evaluating',square)
    value,e1,e2 = square
    x,y = e1
    xx,yy = e2
    startx = min(x,xx)
    endx = max(x,xx)
    startd = min(y,yy)
    endd = max(y,yy)
    #print(square,len(indexes),indexes)
    #one from top one from down ...
    midp = (endx-startx) // 2
    for i in range(midp):
        i1 = startx+i
        if i1 in lineSet:
            if not fd[i1].isLineIn(startd,endd):
                #print(square,'false at',i)
                return False
        i2 = endx-i
        if i2 in lineSet:
            if not fd[i2].isLineIn(startd,endd):
                #print(square,'false at',-i-1)
                return False
    return True

def findSquareInFloordef(floordef,squarelist,lineSet):
    sl = squarelist[:]
    sl.sort()
    sl.reverse()
    for item in sl:
        #evaluate square in floordef
        if evaluate(floordef,item,lineSet):
            return item[0]
    return 0

#
outerpath = createPath(inp)
relevantLineSet = set(getRelevantLineList(inp))

fd = writefloordef(outerpath,relevantLineSet)
fillFloor(fd)

result = findSquareInFloordef(fd,sortedsqareas,relevantLineSet)
print('solution2',result)

