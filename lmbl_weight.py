import os
import pandas as pd
import numpy as np
import shutil
cwd = os.getcwd()
sysname = os.path.basename(cwd)
print(sysname)
if os.path.isdir(cwd+'/lmbl/'):
    shutil.rmtree(cwd+'/lmbl/')
os.mkdir('lmbl')
coor = os.path.join(cwd+ '/coordinates/')
lmbl = os.path.join(cwd+ '/lmbl/')
os.chdir(lmbl)
for filename in os.listdir(coor):
    other_name=[]
    other_X = []
    other_Y = []
    other_Z = []
    C_X = []
    C_Y = []
    C_Z = []
    count_C = 0
    pos_C = []
    print(filename)
    with open(os.path.join(coor+filename)) as f:
        lines=f.readlines()
    f.close()
    #obtian the number of C atoms and the coordinates of other atoms
    for i in range(1,len(lines)):
        lines_ele = lines[i].strip().split(',')
        ele = lines_ele[0]
        if ele == sysname:
            count_C+=1
            pos_C.append(i)
            continue
        else:
            other_name.append(lines_ele[0])
            other_X.append(lines_ele[1])
            other_Y.append(lines_ele[2])
            other_Z.append(lines_ele[3])

    len_others=len(lines)-1-count_C
    #obtain coordinates of
    for j in range(0,count_C):
        lines_C = lines[pos_C[j]].strip().split(',')
        C_X.append(lines_C[1])
        C_Y.append(lines_C[2])
        C_Z.append(lines_C[3])
    #calculate dist between C and other atoms
    #dist between first C and other atoms
    print(C_X)
    CX = C_X[0]
    CY = C_Y[0]
    CZ = C_Z[0]
    pair=[]
    dist=[]
    for k in range(0,len_others):
        Xdiff = float(other_X[k]) - float(CX)
        Ydiff = float(other_Y[k]) - float(CY)
        Zdiff = float(other_Z[k]) - float(CZ)
        d = np.sqrt(np.square(Xdiff)+np.square(Ydiff)+np.square(Zdiff))
        pair.append(sysname + '-' + other_name[k])
        dist.append(d)
    if count_C > 1:
        for l in range(1,count_C):
            Xdiff = float(C_X[l]) - float(CX)
            Ydiff = float(C_Y[l]) - float(CY)
            Zdiff = float(C_Z[l]) - float(CZ)
            d = np.sqrt(np.square(Xdiff) + np.square(Ydiff) + np.square(Zdiff))
            pair.append(sysname + '-' + sysname)
            dist.append(d)
    weight=[]
    for dis in dist:
        w = 1 / dis
        weight.append(w)
    weight_sum=sum(weight)
    frac = [ w / weight_sum for w in weight]
    df = pd.DataFrame({'pair':pair,'dist':dist,'weight':weight,'weight_sum':weight_sum,'frac':frac})
    df.to_csv(filename,index=False)


