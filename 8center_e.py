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

desname_e = []

enum_tot = 0
for i in range(1,9): #change
    for filename in os.listdir(lookup_data):
        desname_e.append(filename.strip().split('.')[0] + '_e_' + str(i))
        enum_tot += 1
print('desname_e:'+str(desname_e))
print('enum_tot:'+str(enum_tot)) #number of elemental properties times # of envs

######################  E  ###################
df_e_new = pd.DataFrame()
for file in file_order:
    df_e=pd.DataFrame()
    E=[]
    des_e=[]

    # lenth of file
    with open(os.path.join(icsd_4A + file + '.txt')) as f:
        len_file = len(f.readlines())
    f.close()

    # get_shell_info
    with open(os.path.join(icsd_4A+file+'.txt')) as f:
        lines = f.readlines()
    f.close()
    print('filename: '+file)

    # obtain_loc_E
    loc_E = []
    for i, line in enumerate(lines, 1):
        if 'Shells' in line:
            loc_E.append(i)
    num_E = len(loc_E)

    #obtain_E
    for i in loc_E:
        E.append(open(icsd_4A + file + '.txt').readlines()[i - 1].strip().split(' (')[1].split(')')[0])

    #obtain sep:
    sep=[]
    for i in range(1,num_E):
        sep.append(loc_E[i]-loc_E[i-1]-2)
    sep.append(len_file-loc_E[-1])

    #obtian loc_shell
    loc_shell = []
    for i, line in enumerate(lines, 1):
        if 'Shell ' in line:
            loc_shell.append(i)
    num_shell = len(loc_shell)

    #obtain dist:
    dist = []
    for i in loc_shell:
        dist.append(
            open(os.path.join(icsd_4A + file + '.txt')).readlines()[i - 1].strip().split(' (')[1].split(' Ang')[0])

    #obtain_dup,E_num,E_ele
    dup = []
    E_num=[]
    E_ele=[]
    with open(icsd_4A+file+'.txt') as f:
        lines = f.readlines()
    f.close()
    for i in loc_shell:
        if len(lines[i-1].strip().split(',')) == 1:
            dup.append(1)
            E_num.append(lines[i-1].strip().split(': ')[1].split(' ')[0])
            E_ele.append(lines[i-1].strip().split(': ')[1].split(' ')[1])
        else:
            dup.append(len(lines[i-1].strip().split(',')))
            for num in range(0, len(lines[i-1].strip().split(','))):
                E_num.append(lines[i-1].strip().split(': ')[1].split(', ')[num].split(' ')[0])
                E_ele.append(lines[i-1].strip().split(': ')[1].split(', ')[num].split(' ')[1])

    #1/dist_sum for each sep
    dist_inv_sum=[]
    dup_count=0
    s=0
    for i in range(0,len(E)):
        sum = 0
        for j in range(0,sep[i]):
            if dup[j+s]==1:
                sum += (1/float(dist[j+s]))*float(E_num[j+s+dup_count])
            else:
                dup_count += dup[j + s]-1
                for k in range(0,dup[j+s]):
                    sum += (1/float(dist[j+s]))*float(E_num[j+s+dup_count-1+k])
        dist_inv_sum.append(sum)
        s += sep[i]
    dup_count = 0
    sum = 0
    s=0
    weights=[]
    ELE=[]
    des_ele=[]
    part=[]
    if len(E)<=8:
        for i in range(0,len(E)):
            for j in range(0,sep[i]):
                if dup[j+s]==1:
                    weight= (1/float(dist[j+s]))*float(E_num[j+s+dup_count])
                    weights.append(weight / float(dist_inv_sum[i]))
                    ELE.append(E_ele[j+s+dup_count])
                else:
                    dup_count += dup[j + s]-1
                    for k in range(0,dup[j+s]):
                        weight= (1/float(dist[j+s]))*float(E_num[j+s+dup_count-1+k])
                        weights.append(weight / float(dist_inv_sum[i]))
                        ELE.append(E_ele[j+s+dup_count-1+k])
            s += sep[i]
            for filename in os.listdir(lookup_data):
                with open(lookup_data + filename) as f:
                    lines = f.readlines()
                f.close()
                for element in ELE:
                    linenum_e=dic[element]
                    des_ele.append(lines[linenum_e-1].strip())
                if 'Missing' in des_ele:
                    des_e.append('NaN')
                elif 'None' in des_ele:
                    des_e.append('NaN')
                elif '#VALUE!' in des_ele:
                    des_e.append('NaN')
                elif 'Missing["NotAvailable"]' in des_ele:
                    des_e.append('NaN')
                elif 'Missing["Unknown"]' in des_ele:
                    des_e.append('NaN')
                elif 'NA' in des_ele:
                    des_e.append('NaN')
                else:
                    for i in range(0,len(weights)):
                        part.append(weights[i]*float(des_ele[i]))
                    des_e.append(np.sum(part))
                part=[]
                des_ele=[]
            weights=[]
            ELE=[]
        # fill the rest with NaN
        for i in range(0,enum_tot-len(des_e)):
            des_e.append('NaN')
    else:
        for i in range(0, len(E)):
            for j in range(0, sep[i]):
                if dup[j + s] == 1:
                    weight = (1 / float(dist[j + s])) * float(E_num[j + s + dup_count])
                    weights.append(weight / float(dist_inv_sum[i]))
                    ELE.append(E_ele[j + s + dup_count])
                else:
                    dup_count += dup[j + s] - 1
                    for k in range(0, dup[j + s]):
                        weight = (1 / float(dist[j + s])) * float(E_num[j + s + dup_count - 1 + k])
                        weights.append(weight / float(dist_inv_sum[i]))
                        ELE.append(E_ele[j + s + dup_count - 1 + k])
            s += sep[i]
            for filename in os.listdir(lookup_data):
                with open(lookup_data + filename) as f:
                    lines = f.readlines()
                f.close()
                for element in ELE:
                    linenum_e = dic[element]
                    des_ele.append(lines[linenum_e - 1].strip())
                if 'Missing' in des_ele:
                    des_e.append('NaN')
                elif 'None' in des_ele:
                    des_e.append('NaN')
                elif '#VALUE!' in des_ele:
                    des_e.append('NaN')
                elif 'Missing["NotAvailable"]' in des_ele:
                    des_e.append('NaN')
                elif 'Missing["Unknown"]' in des_ele:
                    des_e.append('NaN')
                elif 'NA' in des_ele:
                    des_e.append('NaN')
                else:
                    for i in range(0, len(weights)):
                        part.append(weights[i] * float(des_ele[i]))
                    des_e.append(np.sum(part))
                part = []
                des_ele = []
            weights = []
            ELE = []
    df_e = pd.DataFrame([des_e], columns=desname_e, index=None)
    df_e_new = df_e_new.append(df_e)

df_e_new.to_csv(os.path.join(cwd + '/ce_e.csv'), index=False)
end_e=time.time()
time_elapsed=end_e-start
print('Descriptors for the center atoms are generated: '+str(time_elapsed)+'s')
