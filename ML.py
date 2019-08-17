import os
import shutil
from shutil import copy
import sklearn.svm
import numpy as np
from sklearn.ensemble import RandomForestRegressor
import pandas as pd
import pickle
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
import time
start_time = time.time()


#pd.set_option('display.width', 100)
#pd.set_option('display.max_columns', 100)
rf_r2_training_old = []
rf_mae_training_old = []
rf_rmse_training_old = []
rf_r2_testing_old = []
rf_mae_testing_old = []
rf_rmse_testing_old = []

rf_r2_training_new = []
rf_mae_training_new = []
rf_rmse_training_new = []
rf_r2_testing_new = []
rf_mae_testing_new = []
rf_rmse_testing_new = []

rf_r2_training_old_new = []
rf_mae_training_old_new = []
rf_rmse_training_old_new = []
rf_r2_testing_old_new = []
rf_mae_testing_old_new = []
rf_rmse_testing_old_new = []

for run in range (0,10):
    print('loop '+str(run)+' of :10')
    print('old descriptor')
# old data
    df_raw = pd.read_csv('des_ce.csv')
    df = df_raw.dropna()
    X = df.loc[:,'mean_EffectiveCoordination':'MeanIonicChar']
    y = df.loc[:,'delta_e']
#sns.set(style='whitegrid', context='notebook')
#cols = ['mean_EffectiveCoordination', 'mean_BondLengthVariation', 'mean_SpaceGroupNumber', 'mean_GSbandgap', 'MeanIonicChar']
#sns.pairplot(df[cols], size=2.5)
#plt.show()
    X_train, X_test, y_train, y_test = train_test_split(X.values,y.values,test_size=0.3, random_state=42)
    ssl = StandardScaler()
    X_train_ssd = ssl.fit_transform(X_train)
    X_test_ssd = ssl.transform(X_test)

#Random_Forest
#param_grid2 = {'n_estimators':[5,10,50,100]}

    plt.figure(2)
    model_2 = RandomForestRegressor(n_estimators=50,max_features='auto')
    #reg_rdf = GridSearchCV(estimator=model_2, param_grid=param_grid2, cv=5, 'n_estimators'=100, n_jobs=-1)
    model_2.fit(X_train_ssd, y_train)
    y2_train_predict = model_2.predict(X_train_ssd)
    y2_predict = model_2.predict(X_test_ssd)
    plt.scatter(y2_train_predict, y_train, color='r', label='training data')
    plt.scatter(y2_predict, y_test,label='testing data')
    plt.plot([-5,2],[-5,2],ls='--')
    plt.legend()
    plt.title('RF old descriptors')
    plt.xlabel('predicted_delta_e(eV/atom)')
    plt.ylabel('DFT_calculated_delta_e(eV/atom)')
    plt.savefig('rf_olddes.eps')
    plt.show()
    #print('Best score for data:', reg_rdf.best_score_)
    #print('Best n_estimators:',reg_rdf.best_estimator_.n_estimators)
    print("Random Forest Training R2 :%f" % r2_score(y_train,y2_train_predict))
    print("Random Forest Training MAE:%f" % mean_absolute_error(y_train,y2_train_predict))
    print("Random Forest Training RMSE:%f" % np.sqrt(mean_squared_error(y_train,y2_train_predict)))
    print('\n')
    print("Random Forest Testing R2 :%f" % r2_score(y_test,y2_predict))
    print("Random Forest Testing MAE:%f" % mean_absolute_error(y_test,y2_predict))
    print("Random Forest Testing RMSE:%f" % np.sqrt(mean_squared_error(y_test,y2_predict)))
    print('\n')
    rf_r2_training_old.append(r2_score(y_train,y2_train_predict))
    rf_mae_training_old.append(mean_absolute_error(y_train,y2_train_predict))
    rf_rmse_training_old.append(np.sqrt(mean_squared_error(y_train,y2_train_predict)))
    rf_r2_testing_old.append(r2_score(y_test,y2_predict))
    rf_mae_testing_old.append(mean_absolute_error(y_test,y2_predict))
    rf_rmse_testing_old.append(np.sqrt(mean_squared_error(y_test,y2_predict)))

    print('new descriptor')
    ##### new data ######
    X2 = df.loc[:,'MeltingT_c':'NValance_e']
    y2 = df.loc[:,'delta_e']
    #sns.set(style='whitegrid', context='notebook')
    #cols = ['mean_EffectiveCoordination', 'mean_BondLengthVariation', 'mean_SpaceGroupNumber', 'mean_GSbandgap', 'MeanIonicChar']
    #sns.pairplot(df[cols], size=2.5)
    #plt.show()
    X_train, X_test, y_train, y_test = train_test_split(X2.values,y2.values,test_size=0.3, random_state=42)
    ssl = StandardScaler()
    X_train_ssd = ssl.fit_transform(X_train)
    X_test_ssd = ssl.transform(X_test)

    #Random_Forest
    #param_grid2 = {'n_estimators':[5,10,50,100]}

    plt.figure(2)
    model_2 = RandomForestRegressor(n_estimators=50,max_features='auto')
    #reg_rdf = GridSearchCV(estimator=model_2, param_grid=param_grid2, cv=5, 'n_estimators'=100, n_jobs=-1)
    model_2.fit(X_train_ssd, y_train)
    y2_train_predict = model_2.predict(X_train_ssd)
    y2_predict = model_2.predict(X_test_ssd)
    plt.scatter(y2_train_predict, y_train, color='r',label='training data')
    plt.scatter(y2_predict, y_test,label='testing data')
    plt.plot([-5,2],[-5,2],ls='--')
    plt.legend()
    plt.title('RF new descriptors')
    plt.xlabel('predicted_delta_e(eV/atom)')
    plt.ylabel('DFT_calculated_delta_e(eV/atom)')
    plt.savefig('rf_newdes.eps')
    plt.show()
    #print('Best score for data:', reg_rdf.best_score_)
    #print('Best n_estimators:',reg_rdf.best_estimator_.n_estimators)
    print("Random Forest Training R2 :%f" % r2_score(y_train,y2_train_predict))
    print("Random Forest Training MAE:%f" % mean_absolute_error(y_train,y2_train_predict))
    print("Random Forest Training RMSE:%f" % np.sqrt(mean_squared_error(y_train,y2_train_predict)))
    print('\n')
    print("Random Forest Testing R2 :%f" % r2_score(y_test,y2_predict))
    print("Random Forest Testing MAE:%f" % mean_absolute_error(y_test,y2_predict))
    print("Random Forest Testing RMSE:%f" % np.sqrt(mean_squared_error(y_test,y2_predict)))
    print('\n')
    rf_r2_training_new.append(r2_score(y_train, y2_train_predict))
    rf_mae_training_new.append(mean_absolute_error(y_train, y2_train_predict))
    rf_rmse_training_new.append(np.sqrt(mean_squared_error(y_train, y2_train_predict)))
    rf_r2_testing_new.append(r2_score(y_test, y2_predict))
    rf_mae_testing_new.append(mean_absolute_error(y_test, y2_predict))
    rf_rmse_testing_new.append(np.sqrt(mean_squared_error(y_test, y2_predict)))

    print('old & new descriptor')
    ##### new data ######
    X3 = df.loc[:, 'mean_EffectiveCoordination':'NValance_e']
    y3 = df.loc[:, 'delta_e']
    # sns.set(style='whitegrid', context='notebook')
    # cols = ['mean_EffectiveCoordination', 'mean_BondLengthVariation', 'mean_SpaceGroupNumber', 'mean_GSbandgap', 'MeanIonicChar']
    # sns.pairplot(df[cols], size=2.5)
    # plt.show()
    X_train, X_test, y_train, y_test = train_test_split(X3.values, y3.values, test_size=0.3, random_state=42)
    ssl = StandardScaler()
    X_train_ssd = ssl.fit_transform(X_train)
    X_test_ssd = ssl.transform(X_test)

    # Random_Forest
    # param_grid2 = {'n_estimators':[5,10,50,100]}

    plt.figure(3)
    model_2 = RandomForestRegressor(n_estimators=50, max_features='auto')
    # reg_rdf = GridSearchCV(estimator=model_2, param_grid=param_grid2, cv=5, 'n_estimators'=100, n_jobs=-1)
    model_2.fit(X_train_ssd, y_train)
    y3_train_predict = model_2.predict(X_train_ssd)
    y3_predict = model_2.predict(X_test_ssd)
    plt.scatter(y3_train_predict, y_train, color='r', label='training data')
    plt.scatter(y3_predict, y_test, label='testing data')
    plt.plot([-5, 2], [-5, 2], ls='--')
    plt.legend()
    plt.title('RF old & new descriptors')
    plt.xlabel('predicted_delta_e(eV/atom)')
    plt.ylabel('DFT_calculated_delta_e(eV/atom)')
    plt.savefig('rf_old_newdes.eps')
    plt.show()
    # print('Best score for data:', reg_rdf.best_score_)
    # print('Best n_estimators:',reg_rdf.best_estimator_.n_estimators)
    print("Random Forest Training R2 :%f" % r2_score(y_train, y3_train_predict))
    print("Random Forest Training MAE:%f" % mean_absolute_error(y_train, y3_train_predict))
    print("Random Forest Training RMSE:%f" % np.sqrt(mean_squared_error(y_train, y3_train_predict)))
    print('\n')
    print("Random Forest Testing R2 :%f" % r2_score(y_test, y3_predict))
    print("Random Forest Testing MAE:%f" % mean_absolute_error(y_test, y3_predict))
    print("Random Forest Testing RMSE:%f" % np.sqrt(mean_squared_error(y_test, y3_predict)))
    print('\n')
    rf_r2_training_old_new.append(r2_score(y_train, y3_train_predict))
    rf_mae_training_old_new.append(mean_absolute_error(y_train, y3_train_predict))
    rf_rmse_training_old_new.append(np.sqrt(mean_squared_error(y_train, y3_train_predict)))
    rf_r2_testing_old_new.append(r2_score(y_test, y3_predict))
    rf_mae_testing_old_new.append(mean_absolute_error(y_test, y3_predict))
    rf_rmse_testing_old_new.append(np.sqrt(mean_squared_error(y_test, y3_predict)))

print('rf_r2_training_old new: '+str(sum(rf_r2_training_old)/10)+'\t'+str(sum(rf_r2_training_new)/10))
print('rf_mae_training_old new: '+str(sum(rf_mae_training_old)/10)+'\t'+str(sum(rf_mae_training_new)/10))
print('rf_rmse_training_old new: '+str(sum(rf_rmse_training_old)/10)+'\t'+str(sum(rf_rmse_training_new)/10))
print('rf_r2_testing_old new: '+str(sum(rf_r2_testing_old)/10)+'\t'+str(sum(rf_r2_testing_new)/10))
print('rf_mae_testing_old new: '+str(sum(rf_mae_testing_old)/10)+'\t'+str(sum(rf_mae_testing_new)/10))
print('rf_rmse_testing_old new: '+str(sum(rf_rmse_testing_old)/10)+'\t'+str(sum(rf_rmse_testing_new)/10))
print('\n')
print('rf_r2_training_old&new: '+str(sum(rf_r2_training_old_new)/10))
print('rf_mae_training_old&new: '+str(sum(rf_mae_training_old_new)/10))
print('rf_rmse_training_old&new: '+str(sum(rf_rmse_training_old_new)/10))
print('rf_r2_testing_old&new: '+str(sum(rf_r2_testing_old_new)/10))
print('rf_mae_testing_old&new: '+str(sum(rf_mae_testing_old_new)/10))
print('rf_rmse_testing_old&new: '+str(sum(rf_rmse_testing_old_new)/10))
print("--- %s seconds ---" % (time.time() - start_time))
