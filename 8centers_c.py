import os
import pandas as pd
import time
import numpy as np

start=time.time()

#folder_location
cwd=os.getcwd()
lookup_data=os.path.join(cwd+'/lookup_data/')
icsd_4A=os.path.join(cwd+'/shell_icsd_4A/')
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

#obtain_file_order
file_order = []
with open(os.path.join(cwd+'/out.csv')) as o:
    lines = o.readlines()
o.close()
for i in range(1,len(lines)):
    file_order.append(lines[i].strip().split(',')[0])
print(file_order)


desname_c = []
desname_e = []

cnum_tot = 0
for i in range(1,9): #change
    for filename in os.listdir(lookup_data):
        desname_c.append(filename.strip().split('.')[0] + '_c_' + str(i))
        cnum_tot += 1
print('desname_c:'+str(desname_c))
print('cnum_tot:'+str(cnum_tot)) #number of elemental properties times # of centers

df_c_new = pd.DataFrame()
count=0

for file in file_order:
    df_c = pd.DataFrame()
    C=[]
    des_c=[]

    #get_shell_info
    with open(os.path.join(icsd_4A+file+'.txt')) as f:
        lines = f.readlines()
    f.close()
    print('filename: '+file)

    ######################  C  ###################

    #obtain_loc_C
    loc_C=[]
    for i, line in enumerate(lines,1):
        if 'Shells' in line:
            loc_C.append(i)
    num_C = len(loc_C)


    #obtain_C
    for i in loc_C:
        C.append(open(icsd_4A+file+'.txt').readlines()[i-1].strip().split(' (')[1].split(')')[0])

    ######obtain des_c######
    if len(C) <= 8:
        for c in C:
            linenum_c = dic[c]
            for filename in os.listdir(lookup_data):
                with open(lookup_data + filename) as f:
                    lines = f.readlines()
                f.close()
                if lines[linenum_c - 1].strip() in ['Missing','None','#VALUE!','Missing["NotAvailable"]','Missing["Unknown"]','NA']:
                    des_c.append('NaN')
                else:
                    des_c.append(lines[linenum_c - 1].strip())
        for i in range(0,cnum_tot-len(des_c)):
            des_c.append('NaN')
    else:
        first_eight=[]
        for i in range(0,8):
            first_eight.append(des_c[i])
            for c in first_eight:
                linenum_c = dic[c]
                for filename in os.listdir(lookup_data):
                    with open(lookup_data + filename) as f:
                        lines = f.readlines()
                    f.close()
                    if lines[linenum_c - 1].strip() in ['Missing', 'None', '#VALUE!', 'Missing["NotAvailable"]',
                                                        'Missing["Unknown"]', 'NA']:
                        des_c.append('NaN')
                    else:
                        des_c.append(lines[linenum_c - 1].strip())
    for i in range(len(des_c)):
        if des_c[i] == 'NaN':
            continue
        else:
            des_c[i] = float(des_c[i])

    df_c=pd.DataFrame([des_c], columns=desname_c, index=None)
    df_c_new=df_c_new.append(df_c)
df_c_new.to_csv(os.path.join(cwd + '/ce_c.csv'), index=False)
end_c=time.time()
time_elapsed=end_c-start
print('Descriptors for the center atoms are generated: '+str(time_elapsed)+'s')
