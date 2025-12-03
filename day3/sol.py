
def load(fname):
    with open(fname,'rt') as f:
        return [x.strip() for x in f.readlines() ]

#inp = load('test-input.txt')
inp = load('input.txt')
print(inp)

def find2digsNum(line):
    line = [int(x) for x in list(line)]
    first = max(line[:-1])
    first_i = line[:-1].index(first)
    second = max(line[first_i+1:])
    return first*10 + second

res = 0
for line in inp:
    res += find2digsNum(line)

print(f'solution1 {res}')

def findNdigsNum(line,n):
    line = [int(x) for x in list(line)]
    num = 0
    index = 0
    for i in range(n-1,-1,-1):
        sublist = line[index:-i] if i>0 else line[index:]
        digit = max(sublist)
        index += sublist.index(digit) + 1
        num *= 10
        num += digit
    return num

res2 = 0
for line in inp:
    res2 += findNdigsNum(line,12)
    
print(f'solution2 {res2}')
    
