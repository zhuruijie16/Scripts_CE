import os
import pandas as pd
import time

start=time.time()

#folder_location
lookup_data='./SHU-descriptors/'
icsd_shell_5A='./perovskite_shell_10A/'
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
for file in sorted(os.listdir(icsd_shell_5A)):
    file_order.append(file)
#print(file_order)


desname_c = []

for i in range(1,4): #change
    list = sorted(os.listdir(lookup_data))
    for filename in list:
        desname_c.append(filename.strip().split('.')[0] + '_c_' + str(i))
#print('desname_c:'+str(desname_c))

df_c_new = pd.DataFrame()
count=0

for file in file_order:
    count+=1
    df_c = pd.DataFrame()
    des_c=[]

    #get_shell_info
    lines = open(icsd_shell_5A+file).readlines()
    print('filename:',file,"count:",count)

    ######################  C  ###################
    C=[]
    #obtain_loc_C
    loc_C=[]
    for i, line in enumerate(lines,1):
        if 'Shells' in line:
            loc_C.append(i)
    num_C = len(loc_C)


    #obtain_C
    for i in loc_C:
        C.append(open(icsd_shell_5A+file).readlines()[i-1].strip().split(' (')[1].split(')')[0])

    # obtain_C_diff - put O at last
    C_diff = []
    for c in C:
        if c not in C_diff:
            C_diff.append(c)

    if len(C_diff) ==2:
        for c in C_diff:
            if c != 'O':
                ele_dup = c
                C_diff.insert(0,ele_dup)
                break


    for i,c in enumerate(C_diff):
        if c == 'O' and i != 2:
            C_diff[i] = C_diff[2]
            C_diff[2] = 'O'

    #print(C_diff)

    ######obtain des_c######
    if len(C_diff) <= 3:
        for c in C_diff:
            linenum_c = dic[c]
            list = sorted(os.listdir(lookup_data))
            for filename in list:
                lines = open(lookup_data+filename).readlines()
                if lines[linenum_c - 1].strip() in ['Missing','None','#VALUE!','Missing["NotAvailable"]','Missing["Unknown"]','NA']:
                    des_c.append('NaN')
                else:
                    des_c.append(lines[linenum_c - 1].strip())
        '''
        for i in range(0,cnum_tot-len(des_c)):
            des_c.append('NaN')
        '''
        #print('des_c:'+str(des_c))
    else:
        print('error')
        '''
        first_eight=[]
        for i in range(0,5):
            first_eight.append(C[i])
        for c in first_eight:
            linenum_c = dic[c]
            list = os.listdir(lookup_data)
            list.sort()
            for filename in list:
                with open(lookup_data + filename) as f:
                    lines = f.readlines()
                f.close()
                if lines[linenum_c - 1].strip() in ['Missing', 'None', '#VALUE!', 'Missing["NotAvailable"]',
                                                    'Missing["Unknown"]', 'NA']:
                    des_c.append('NaN')
                else:
                    des_c.append(lines[linenum_c - 1].strip())
        '''
    for i in range(len(des_c)):
        if des_c[i] == 'NaN':
            continue
        else:
            des_c[i] = float(des_c[i])
    df_c=pd.DataFrame([des_c], columns=desname_c, index=None)
    df_c_new=df_c_new.append(df_c)
df_c_new.to_csv('ce_c.csv', index=False)
end_c=time.time()
time_elapsed=end_c-start
print('Descriptors for the center atoms are generated: '+str(time_elapsed)+'s')
