from functools import reduce

def read(fname):
    with open(fname,'rt') as f:
        lines = f.readlines()
    lastl = lines[-1]
    #extracting operands and number sizes o__..__o ...
    operands = []
    numsizes = []
    numsizetmp = 0
    for i in range(len(lastl)):
        if lastl[i] in {'+','*'}:
            operands += [lastl[i]]
            numsizes.append(numsizetmp) #1sp delimiter but operand takes 1space
            numsizetmp = 0
        else:
            numsizetmp += 1
    numsizes += [ numsizetmp+1 ]
    numsizes = numsizes[1:]
    nums = []
    for line in lines[:-1]:
        i = 0
        numline = []
        for numsize in numsizes:
            numline += [ line[i:i+numsize] ]
            i += numsize + 1            
        nums.append(numline)
    return nums,operands,numsizes

nums, ops, numsizes = read('test-input.txt')
nums, ops, numsizes = read('input.txt')

def rotate(matrix):
    newm = []
    for c in range(len(matrix[0])):
        tmp = []
        for r in range(len(matrix)):
            tmp += [ matrix[r][c] ]
        newm.append(tmp)
    return newm

def translatenums(numline):
    numlist = []
    size = len(numline[0])
    for i in range(1,size+1):
        newnum = 0
        for num in numline:
            tmp = num[-i]
            if tmp!=' ':
                newnum *= 10
                newnum += int(tmp)
        numlist += [ newnum ]        
    return numlist

def getop(operand_s):
    if operand_s=='*':
        return lambda x,y:x*y
    elif operand_s=='+':
        return lambda x,y:x+y
    else:
        raise Exception(f"something very wrong happend operand:{operand_s}")

def getneutralpoint(operand_s):
    return 0 if operand_s=='+' else 1

def evaluateline(numline,operand_s):
    op = getop(operand_s)
    neutral = getneutralpoint(operand_s)
    lr = reduce(op,numline,neutral)
    #print(operand_s,numline,lr)
    return lr

#nums, ops, numsizes
def evaluateall(numlines,operands):
    #lines of nums and operands per line
    return sum( [ evaluateline(x,o) for x,o in zip(numlines,operands) ] )

nums = rotate(nums)
nums = [ translatenums(nlist) for nlist in nums ]

res = evaluateall(nums,ops)
print('solution2',res)
