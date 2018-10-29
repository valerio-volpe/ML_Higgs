import numpy as np
from load_data import load_data
from preprocessing import *
from regression_tools import *
from implementations import *
from cross_validation_logistic import *

# Read the data and set parameters
x_train,y_train,x_test,ids_test=load_data('train.csv','test.csv')
seed = 1

#Set parameters values
max_iters = 1000
degrees=np.arange(3,15)
lambdas = np.logspace(-8,-3,15)
k_fold = 4

# Clean the x vector from incorrect values 
x_train_cleaned,nmc_tr=cleaning_function(x_train,-999)


# Cross Validation to find best degree and lambda
mean_nb_err_te = cross_validation_logistic_demo_prova(y_train,x_train_cleaned,degrees,k_fold,lambdas,seed,2,noaf,nmc_tr)


#ONCE FOUND THE BEST LAMBDA AND DEGREE, PUT THEM INTO TEST_LOGISTIC_PENALIZED