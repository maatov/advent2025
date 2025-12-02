def load(fname):
    with open(fname,'rt') as f:
        return [ tuple(x.split('-')) for x in f.read().split(',') ]

def evaluate_number(num):
    if len(num) % 2 != 0:
        return 0
    else:
        sz = len(num)
        if num[:sz//2]==num[sz//2:]:
            return int(num)
        else:
            return 0

def evaluate_range(rng,evaluation_method):
    s,e = rng
    s,e = int(s),int(e)
    range_sum = 0
    for i in range(s,e+1):
        range_sum += evaluation_method(str(i))
    #print(f'range of {s} - {e} : {range_sum}')
    return range_sum
    

#inp = load('test-input.txt')
inp = load('input.txt')
#print(inp)
solution1 = 0
for t in inp:
    solution1 += evaluate_range(t,evaluate_number)

print('sol1:',solution1)

def evaluate_moresilly_number(num):
    l = len(num)
    if l<=1:
        return 0
    for s in range(1,l//2+1):
        if l % s != 0:
            continue
        if num==num[:s]*(l//s):
            return int(num)
    return 0

solution2 = 0
for t in inp:
    solution2 += evaluate_range(t,evaluate_moresilly_number)
print('sol2:',solution2)
