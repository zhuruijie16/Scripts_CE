import os
import pandas as pd
import numpy as np
import glob
import shutil
from shutil import copy
cwd = os.getcwd()
sysname = os.path.basename(cwd)
if os.path.isdir(cwd+'/new_descriptors/'):
    shutil.rmtree(cwd+'/new_descriptors/')
os.mkdir(cwd+'/new_descriptors/')
new_descriptors = os.path.join(cwd+'/new_descriptors/')
copy(os.path.join(cwd+'/magpie/postprocessing/out.csv'), new_descriptors)
lmbl = os.path.join(cwd+'/lmbl/')
lookup_data = os.path.join(cwd+'/lookup_data/')
sysname = os.path.basename(cwd)
dic = {
    'H': 1,
    'He': 2,
    'Li': 3,
    'Be': 4,
    'B': 5,
    'C': 6,
    'N': 7,
    'O': 8,
    'F': 9,
    'Ne': 10,
    'Na': 11,
    'Mg': 12,
    'Al': 13,
    'Si': 14,
    'P': 15,
    'S': 16,
    'Cl': 17,
    'Ar': 18,
    'K': 19,
    'Ca': 20,
    'Sc': 21,
    'Ti': 22,
    'V': 23,
    'Cr': 24,
    'Mn': 25,
    'Fe': 26,
    'Co': 27,
    'Ni': 28,
    'Cu': 29,
    'Zn': 30,
    'Ga': 31,
    'Ge': 32,
    'As': 33,
    'Se': 34,
    'Br': 35,
    'Kr': 36,
    'Rb': 37,
    'Sr': 38,
    'Y': 39,
    'Zr': 40,
    'Nb': 41,
    'Mo': 42,
    'Tc': 43,
    'Ru': 44,
    'Rh': 45,
    'Pd': 46,
    'Ag': 47,
    'Cd': 48,
    'In': 49,
    'Sn': 50,
    'Sb': 51,
    'Te': 52,
    'I': 53,
    'Xe': 54,
    'Cs': 55,
    'Ba': 56,
    'La': 57,
    'Ce': 58,
    'Pr': 59,
    'Nd': 60,
    'Pm': 61,
    'Sm': 62,
    'Eu': 63,
    'Gd': 64,
    'Tb': 65,
    'Dy': 66,
    'Ho': 67,
    'Er': 68,
    'Tm': 69,
    'Yb': 70,
    'Lu': 71,
    'Hf': 72,
    'Ta': 73,
    'W': 74,
    'Re': 75,
    'Os': 76,
    'Ir': 77,
    'Pt': 78,
    'Au': 79,
    'Hg': 80,
    'Tl': 81,
    'Pb': 82,
    'Bi': 83,
    'Po': 84,
    'At': 85,
    'Rn': 86,
    'Fr': 87,
    'Ra': 88,
    'Ac': 89,
    'Th': 90,
    'Pa': 91,
    'U': 92,
    'Np': 93,
    'Pu': 94
}

#generating descriptor for the center atom
linenum_c=dic[sysname]
des_c=[]
desname_c=[]
for filename in os.listdir(lookup_data):
    with open(lookup_data+filename) as f:
        lines = f.readlines()
    f.close()
    desname_c.append(filename.strip().split('.')[0]+'_c')
    des_c.append(lines[linenum_c-1].strip())

#getting the sys order of out.csv -get file_order
file_order = []
with open(os.path.join(new_descriptors+'out.csv')) as o:
    lines = o.readlines()
o.close()
for i in range(1,len(lines)):
    file_order.append(lines[i].strip().split(',')[0])

#write out descriptors to csv - get des_c
des_c = des_c * len(file_order)
des_c = np.reshape(des_c,(len(file_order),len(desname_c)))
df = pd.DataFrame(des_c, columns=desname_c)

df.to_csv(os.path.join(new_descriptors+'/des_c.csv'),index=False)

#generating descriptor for the environment atoms - get eles & fracs
des_e = []
for i in range(0,len(file_order)):
    eles = []
    fracs = []
    desname_e = []
    with open(lmbl+file_order[i]+'.csv') as f:
        lines = f.readlines()
    f.close()
    print(file_order[i]+'.csv')

    for k in range(1,len(lines)):
        split = lines[k].strip().split(',')
        ele = split[0].split('-')[1]
        frac = split[4]
        eles.append(ele)
        fracs.append(frac)
    print(eles)
    print(fracs)
    #obtian desname_e
    for filename in os.listdir(lookup_data):
        desname_e.append(filename.strip().split('.')[0] + '_e')

    for filename in os.listdir(lookup_data):
        des_e_raw = []
        with open(lookup_data+filename) as f:
            lines = f.readlines()
        f.close()
        for i in range(0,len(eles)):
            pos = dic[eles[i]]
            print(filename)
            print(lines[pos-1].strip())
            print(fracs[i])
            des_e_raw.append(float(lines[pos-1].strip()) * float(fracs[i]))
        des_e.append(sum(des_e_raw))

des_e_new = np.reshape(des_e,(len(file_order),len(desname_e)))

df = pd.DataFrame(des_e_new, columns=desname_e)

df.to_csv(os.path.join(new_descriptors+'/des_e.csv'), index=False)

df_out = pd.read_csv(os.path.join(new_descriptors+"out.csv"))
df_c = pd.read_csv(os.path.join(new_descriptors+"des_c.csv"))
df_e = pd.read_csv(os.path.join(new_descriptors+"des_e.csv"))
df_ce = pd.concat([df_out, df_c, df_e],axis=1)
df_ce.to_csv(os.path.join(new_descriptors+'des_ce.csv'),index=False)
df = pd.read_csv(os.path.join(new_descriptors+'des_ce.csv'))

if os.path.isdir(os.path.join(cwd+'/ML/')):
    shutil.rmtree(os.path.join(cwd+'/ML/'))
os.mkdir('ML')
copy(os.path.join(cwd+'/new_descriptors/des_ce.csv'),os.path.join(cwd+'/ML'))
copy(os.path.join(cwd+'ML.py'),os.path.join(cwd+'/ML'))




