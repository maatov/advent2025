import re

with open('input.txt','rt') as f:
    data = f.readlines()
    #print(data)

L = -1
R = 1

lastrotation = (L,0)
realpos = 50
counter = 0

def rotate(pos,counter,rot):
    drct,length = rot
    #if pos==0 and lastrotation[0]==R and drct==L:
    #    counter += 1
    newpos = drct * length + pos
    if newpos<0:
        newpos = newpos % 100
    if newpos>99:
        newpos = newpos % 100
    #if newpos==0 and drct==L:
    #    counter += 1
    if newpos==0:
        counter += 1
    #print(newpos,rot)
    return newpos,counter,rot

def rotate_method_0x434C49434B(pos,counter,rot):
    drct,length = rot
    newpos = drct * length + pos
    #order of if's is of most importance here!
    if newpos<0 and pos==0:
        newpos += 100
    while newpos<0:
        newpos += 100
        counter += 1
    if newpos==0:
        counter += 1
    while newpos>99:
        newpos -= 100
        counter += 1
    return newpos,counter,rot

for l in data:
    res = re.match("([LR])(\d+)",l)
    rotation = (L if res.group(1)=="L" else R,int(res.group(2)))
    realpos,counter,lastrotation = rotate_method_0x434C49434B(realpos,counter,rotation)

print('solution2',counter)
