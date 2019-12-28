import os
import pandas as pd
import time
import numpy as np

start=time.time()
#folder_location
cwd=os.getcwd()
lookup_data=os.path.join(cwd+'/lookup_data/')
icsd_4A=os.path.join(cwd+'/shell_icsd_4A/')
os.chdir(icsd_4A)
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
for i in range(1,9):
    for filename in os.listdir(lookup_data):
        desname_c.append(filename.strip().split('.')[0] + '_c_' + str(i))
        desname_e.append(filename.strip().split('.')[0] + '_e_' + str(i))
        cnum_tot += 1
print('desname_c:'+str(desname_c))
print('desname_e:'+str(desname_e))
#print(len(desname_c)+len(desname_e))
print('cnum_tot:'+str(cnum_tot))

df_c = pd.DataFrame()
df_c_new = pd.DataFrame()
df_e = pd.DataFrame()
df_e_new = pd.DataFrame()
count=0

for file in file_order:
    ele=[]
    C=[]
    E=[]
    des_c=[]
    des_e=[]

    #get_shell_info
    with open(os.path.join(icsd_4A+file+'.txt')) as f:
        lines = f.readlines()
    f.close()
    print('filename: '+file)

    ######################  C  ###################
    # lenth of file
    with open(os.path.join(icsd_4A + file + '.txt')) as f:
        len_file = len(f.readlines())
    #obtain_loc_C
    loc_C=[]
    for i, line in enumerate(lines,1):
        if 'Shells' in line:
            loc_C.append(i)
    num_C = len(loc_C)
    #print('loc_C: '+str(loc_C))
    #print('num_C: '+str(num_C))

    #obtain_loc_E
    loc_E=[]
    for i, line in enumerate(lines,1):
        if 'Shells' in line:
            loc_E.append(i)
    num_E = len(loc_E)
    #print('loc_E: ' + str(loc_E))
    #print('num_E: ' + str(num_E))

    #obtain_C
    for i in loc_C:
        C.append(open(icsd_4A+file+'.txt').readlines()[i-1].strip().split(' (')[1].split(')')[0])
    #print('C: '+str(C))

    #obtain_E
    for i in loc_E:
        E.append(open(icsd_4A + file + '.txt').readlines()[i - 1].strip().split(' (')[1].split(')')[0])
    #print('E: ' + str(E))

    #obtain sep:
    sep=[]
    for i in range(1,num_E):
        sep.append(loc_E[i]-loc_E[i-1]-2)
    sep.append(len_file-loc_E[-1])

    loc_shell = []
    for i, line in enumerate(lines, 1):
        if 'Shell ' in line:
            loc_shell.append(i)
    num_shell = len(loc_shell)
    #print('num_shell: '+str(num_shell))

    # obtain dist:
    dist = []
    for i in loc_shell:
        dist.append(
            open(os.path.join(icsd_4A + file + '.txt')).readlines()[i - 1].strip().split(' (')[1].split(' Ang')[0])
    #print('dist: '+str(dist))

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
    #print('dup:')
    #print(dup)
    #print('E_num:')
    #print(E_num)
    #print('E_ele:')
    #print(E_ele)

    #1/dist_sum for each sep
    dist_inv_sum=[]
    dup_count=0
    sum=0
    s=0
    for i in range(0,len(E)):
        for j in range(0,sep[i]):
            if dup[j+s]==1:
                sum += (1/float(dist[j+s]))*float(E_num[j+s+dup_count])
            else:
                dup_count += dup[j + s]-1
                for k in range(0,dup[j+s]):
                    sum += (1/float(dist[j+s]))*float(E_num[j+s+dup_count-1+k])
        dist_inv_sum.append(sum)
        sum=0
        s += sep[i]
    count+=1
    #print('dist_inv_sum:'+str(dist_inv_sum))

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
        #print('len_des_c'+str(len(des_c)))
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


######################  E  ###################
Start Here!
    ######obtain weights && des_e#####
    dup_count = 0
    sum = 0
    s=0
    weights=[]
    ELE=[]
    des_ele=[]
    part=[]
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
        #print('weights:'+str(weights))
        #print('ELE:'+str(ELE))

        for filename in os.listdir(lookup_data):
            #print('tablename:' + str(filename))
            with open(lookup_data + filename) as f:
                lines = f.readlines()
            f.close()
            for element in ELE:
                linenum_e=dic[element]
                des_ele.append(lines[linenum_e-1].strip())
            #print('des_ele:'+str(des_ele))
            #print('weights:'+str(weights))
            for i in range(0,len(weights)):
                part.append(weights[i]*float(des_ele[i]))
            #print('part:'+str(part))
            des_e.append(np.sum(part))
            part=[]
            #print('des_e:'+str(des_e))
            des_ele=[]
        weights=[]
        ELE=[]
    des_e=np.reshape(des_e,(len(E),com_des_num))
    print('des_e: '+str())

    df_e_new = pd.DataFrame([des_e], columns=desname_e, index=None)
    df_e = df_e.append(df_e_new)
    count+=1
    #print(count)

df_e.to_csv(os.path.join(cwd + '/ce_e.csv'), index=False)
end_e=time.time()
time_elapsed = end_e - start
print('Descriptors for the center atoms are generated: '+str(time_elapsed)+'s')
