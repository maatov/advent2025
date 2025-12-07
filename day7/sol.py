def read(fname):
    with open(fname,'rt') as f:
        data = f.readlines()
    tmap = [ x.strip() for x in data ]
    return tmap

tmap = read('test-input.txt')
tmap = read('input.txt')
    
#find manifold entry point
startl = 0
for i in tmap:
    startl += 1
    s = i.find('S')
    if s!=-1:
        entry = s
        break

tmap = tmap[startl:]
beampositions = { entry }
dimension_x = len(tmap[0])

def step(beampositions,nextline,splits):
    newbeampositions = []
    for b in beampositions:
        if nextline[b]=='.':
            newbeampositions += [b]
        elif nextline[b]=='^':
            newbeampositions += [b-1,b+1]
            splits += 1
    newbeampositions = set(newbeampositions)
    try:
        newbeampositions.remove(-1)
    except:
        pass
    try:
        newbeampositions.remove(dimension_x)
    except:
        pass
    return newbeampositions, splits

splits = 0
for maniline in tmap:
    beampositions, splits = step(beampositions,maniline,splits)

print('solution1',splits,len(beampositions))

def updateInMap(m,entry,value):
    if entry>=0 and entry<dimension_x:
        try:
            m[entry] += value
        except:
            m[entry] = value

def stepq(beamquants,nextline):
    #print(type(beamquants),beamquants)
    newbeamquants = beamquants.copy() #set of pairs
    for pos in beamquants:
        if nextline[pos]=='.':
            pass
        elif nextline[pos]=='^':
            q = beamquants[pos]
            updateInMap(newbeamquants,pos-1,q)
            updateInMap(newbeamquants,pos+1,q)
            newbeamquants[pos] = 0            
    return newbeamquants

beamquants = { entry:1 }
for maniline in tmap:
    beamquants = stepq(beamquants,maniline)
    
#print(beamquants)
sol = sum([ beamquants[m] for m in beamquants ])
#numofrays = sum([1 if beamquants[x]>0 else 0 for x in beamquants])
print('solution2',sol)
