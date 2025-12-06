from functools import reduce

def read(fname):
    with open(fname,'rt') as f:
        data = f.readlines()
    data = [x.strip().split() for x in data ]
    print(data)
    return data
    
def rotateandreverse(matrix):
    newm = []
    for c in range(len(matrix[0])):
        tmp = []
        for r in range(len(matrix)):
            tmp += [ matrix[r][c] ]
        tmp.reverse()
        newm.append(tmp)
    return newm

mathproblem = read('test-input.txt')
mathproblem = read('input.txt')

def evaluate(mathline):
    op = mathline[0]
    mathline = [ int(x) for x in mathline[1:] ]
    oper = (lambda x,y: x+y) if op=='+' else (lambda x,y:x*y)
    zeropoint = 0 if op=='+' else 1
    return reduce(oper,mathline,zeropoint)

def evaluateall(problem):
    return sum([evaluate(x) for x in problem])

print('solution1',evaluateall(rotateandreverse(mathproblem)))