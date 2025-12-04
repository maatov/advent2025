
def load(fname):
    with open(fname,'rt') as f:
        return [x.strip() for x in f.readlines() ]

#inp = load('test-input.txt')
inp = load('input.txt')

len_x = len(inp[0])
len_y = len(inp)

def canAccess(r,c,matrix):
    if matrix[r][c]=='@':
        rdirs = [-1,0,1]
        cdirs = [-1,0,1]
        rollsaround = 0
        for rr in rdirs:
            nr = r+rr
            if nr<0 or nr>=len_y:
                continue
            for cc in cdirs:
                nc = c+cc
                if nc<0 or nc>=len_x or (rr==0 and cc==0):
                    continue
                elif matrix[nr][nc]=='@':
                    rollsaround += 1
        return rollsaround < 4                
    else:
        return False

forkliftable = 0
for r in range(len_y):
    for c in range(len_x):
        forkliftable += 1 if canAccess(r,c,inp) else 0

print('solution1',forkliftable)

def markAndRemove(inp):
    tmp = inp[:]
    removed = 0
    for i in range(len_y):
        for j in range(len_x):
            if canAccess(i,j,inp):
                tmp[i][j] = '.'
                removed += 1
            else:
                tmp[i][j] = inp[i][j]
    return tmp,removed

def removeAllYouCanRemove(inp):
    total = 0
    matrix = [list(x) for x in inp]
    while True:
        matrix,newrolls = markAndRemove(matrix)
        if newrolls==0:
            break
        else:
            total += newrolls
    return total

total = removeAllYouCanRemove(inp)
print('solution2',total)