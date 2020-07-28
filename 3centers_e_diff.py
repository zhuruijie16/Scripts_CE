import os
import pandas as pd
import time
import numpy as np

start=time.time()

#folder_location
lookup_data='./lookup_data_shu/'
shell_file='./cubic_shell_10A/'
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
file_order = sorted(os.listdir(shell_file))
#print(file_order)

desname_e = []
enum_tot = 0

for i in range(1,4): #change
    for ele_prop in sorted(os.listdir(lookup_data)):
        desname_e.append(ele_prop.strip().split('.')[0] + '_e_' + str(i))
        enum_tot += 1

######################  E  ###################
df_e_new = pd.DataFrame()
count=0

for file in file_order:
    print(file, "count:", count)
    count += 1
    df_e=pd.DataFrame()
    des_e=[]

    # lenth of file
    len_file = len(open(shell_file+file).readlines())

    # shell_info
    lines = open(os.path.join(shell_file+file)).readlines()

    # loc_E
    loc_E = []
    for i, line in enumerate(lines):
        if 'Shells' in line:
            loc_E.append(i)
    num_E = len(loc_E)
    #print('loc_E:',loc_E)

    # E
    E=[]
    for i in loc_E:
        E.append(lines[i].strip().split(' (')[1].split(')')[0])
    #print('E:',E)

    # sep:
    sep=[]
    for i in range(1,num_E):
        sep.append(loc_E[i]-loc_E[i-1]-2)
    sep.append(len_file-loc_E[-1]-1)
    #print('sep:',sep)

    ## E_diff,sep_diff:
    E_diff = []
    sep_diff = []
    for i,e in enumerate(E):
        if e not in E_diff:
            E_diff.append(e)
            sep_diff.append(sep[i])

    # Put O at last
    for i,e in enumerate(E_diff):
        if e == 'O' and i != 2:
            E_diff[i] = E_diff[2]
            E_diff[2] = 'O'
            tmp = sep_diff[i]
            sep_diff[i] = sep_diff[2]
            sep_diff[2] = tmp
    #print(f'E_diff:{E_diff}')
    #print(f'sep_diff:{sep_diff}')

    ## loc_E_diff
    loc_E_diff = []
    for e_df in E_diff:
        loc_E_diff.append(loc_E[E_diff.index(e_df)])
    #print('loc_E_diff',loc_E_diff)

    ## loc_shell
    loc_shell = []
    for i, line in enumerate(lines):
        if 'Shell ' in line:
            loc_shell.append(i)
    #print('loc_shell',loc_shell)

    #obtain dist:
    dist = []
    for i in loc_shell:
        dist.append(lines[i].strip().split(' (')[1].split(' Ang')[0])
    #print(f'dist:{dist}')

    # dup,E_num,E_ele
    dup=[]
    E_num=[]
    E_ele=[]
    for i in loc_shell:
        if len(lines[i].strip().split(',')) == 1:
            dup.append(1)
            E_num.append(lines[i].strip().split(': ')[1].split(' ')[0])
            E_ele.append(lines[i].strip().split(': ')[1].split(' ')[1])
        else:
            dup.append(len(lines[i].strip().split(',')))
            for num in range(len(lines[i].strip().split(','))):
                E_num.append(lines[i].strip().split(': ')[1].split(', ')[num].split(' ')[0])
                E_ele.append(lines[i].strip().split(': ')[1].split(', ')[num].split(' ')[1])
    #print(f'dup:{dup}')
    #print(f'E_num:{E_num}')
    #print(f'E_ele:{E_ele}')

    #1/dist_sum for each sep_diff
    dist_inv_sum=[]
    for i,e_diff in enumerate(E_diff):
        sum=0
        lag = 0
        for j in range(sep_diff[i]):
            index = E_diff.index(E_diff[i])
            #print(f'sep:{sep}')
            #print(f'sep_diff[i]:{sep_diff[i]}')
            #print(f'index:{index}')
            sep_sum_before=0
            for m in range(index):
                sep_sum_before += sep[m]
            #print(f'sep_sum_before:{sep_sum_before}')
            if dup[sep_sum_before+j]==1:
                #print(f'E_num:{E_num}')
                #print(f'j:{j}')
                #print(f'k:{k}')
                sum += (1 / float(dist[sep_sum_before+j])) * float(E_num[sep_sum_before+j+lag])
                #print(f'dist[sep_sum_before+j]:{dist[sep_sum_before+j]}')
                #print(f'E_num[sep_sum_before+j+lag]:{E_num[sep_sum_before+j+lag]}')
                #print(f'sum:{sum}')
            else:
                #print('************ dup *************')
                for k in range(dup[sep_sum_before+j]):
                    #print(f'E_num:{E_num}')
                    #print(f'j:{j}')
                    #print(f'k:{k}')
                    sum += (1 / float(dist[sep_sum_before+j])) * float(E_num[sep_sum_before+j+k+lag])
                    #print(f'dist[sep_sum_before+j]:{dist[sep_sum_before+j]}')
                    #print(f'E_num[sep_sum_before+j+k+lag]:{E_num[sep_sum_before+j+k+lag]}')
                    #print(f'sum:{sum}')
                lag+=dup[sep_sum_before+j]-1

        dist_inv_sum.append(sum)
        #print('dist_inv_sum:',dist_inv_sum)

    dup_count = 0
    for i,e_diff in enumerate(E_diff):
        weights=[]
        ELE=[]
        lag = 0
        for j in range(sep_diff[i]):
            index = E_diff.index(E_diff[i])
            sep_sum_before = 0
            for m in range(index):
                sep_sum_before += sep[m]
            if dup[sep_sum_before+j]==1:
                weight= (1/float(dist[sep_sum_before+j]))*float(E_num[sep_sum_before+j+lag])
                weights.append(weight / float(dist_inv_sum[i]))
                ELE.append(E_ele[sep_sum_before+j+lag])
            else:
                for k in range(dup[sep_sum_before+j]):
                    weight= (1/float(dist[sep_sum_before+j]))*float(E_num[sep_sum_before+j+k+lag])
                    weights.append(weight / float(dist_inv_sum[i]))
                    ELE.append(E_ele[sep_sum_before+j+k+lag])
                lag+=dup[sep_sum_before+j]-1
        #print(f'weights:{weights}')
        #print(f'ELE:{ELE}')

        list = sorted(os.listdir(lookup_data))

        for ele_prop in list:
            #print(ele_prop)
            part=[]
            des_ele=[]
            lines = open(lookup_data + ele_prop).readlines()
            for element in ELE:
                linenum_e=dic[element]-1
                des_ele.append(lines[linenum_e].strip())
            #print(des_ele)
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
                for i in range(len(weights)):
                    part.append(weights[i]*float(des_ele[i]))
                    #print(f'part:{part}')
                des_e.append(np.sum(part))
                #print(f'des_e:{des_e}')



    # fill the rest with NaN
    '''
    for i in range(0,enum_tot-len(des_e)):
        des_e.append('NaN')
    '''

    df_e = pd.DataFrame([des_e], columns=desname_e, index=None)
    df_e_new = df_e_new.append(df_e)

df_e_new.to_csv(os.path.join('./ce_e.csv'), index=False)
end_e=time.time()
time_elapsed=end_e-start
print('Descriptors for the environment atoms generated: '+str(time_elapsed)+'s')
