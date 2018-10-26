import numpy as np
from regression_tools import * 
from preprocessing import *

def build_k_indices(y, k_fold, seed):
    """build k indices for k-fold."""
    num_row = y.shape[0]
    interval = int(num_row / k_fold)
    np.random.seed(seed)
    indices = np.random.permutation(num_row)
    k_indices = [indices[k * interval: (k + 1) * interval]
                 for k in range(k_fold)]
    return np.array(k_indices)

def logistic_cross_validation(y, phi, k_indices, k, gamma, degree, nmc , interactions, logistic_type, max_iter, threshold):
    """return the loss of logistic regression."""
    """Probabilmente conviene implementare una per la regressione normale, in modo da capire 
    quale sia il grado massimo oltre il quale non ha senso andare e poi lavorare con lambda 
    per capire come eliminare feature"""
      
    train_indices = np.delete(k_indices , k , 0).reshape((k_indices.shape[0]-1) * k_indices.shape[1])
    x_test = phi[k_indices[k],:]
    x_train = phi[train_indices,:]
    y_test = y[k_indices[k]]
    y_train = y[train_indices]
    
    tx_train = build_polinomial(x_train, degree, nmc+interactions)
    tx_train = norm_data(tx_train, not_norm_features=nmc, skip_first_col=True)
    tx_test = build_polinomial(x_test, degree, nmc+interactions)
    tx_test = norm_data(tx_train, not_norm_features=nmc, skip_first_col=True)
    
    if logistic_type==0:
        loss , w = logistic_regression_gradient_descent_demo(y_train, tx_train, gamma, max_iter, threshold)
    elif logistic_type==1:
        logistic_regression_newton_method_demo(y_train, tx_train)
    elif logistic_type==2:
        logistic_regression_penalized_gradient_descent_demo(y_train, tx_train)
    #elif logistic_type==3
            
    result=(y_test==(sigmoid(tx_test.dot(w))>0.5)).sum()/y_test.shape[0]
    return result

def cross_validation_logistic_demo(y_train,x_train,degrees,k_fold,lambdas,seed,logistic_type, max_iter=1000, threshold=1e-8):
    """
    Performs cross validation.
    logistic_type:
        0: gradient descent
        1: Netwon
        2: penalised gradient descent
        3: stochastic gradient descent
    """
    # split data in k fold
    k_indices = build_k_indices(y_train, k_fold, seed)

    # Clean data 
    x_train_cleaned,nmc_tr=cleaning_function(x_train,-999)
    #feature augmentation
    x_train_cleaned,noaf=features_augmentation(x_train_cleaned,not_augm_features=nmc_tr+1)

    # cross validation
    mean_nb_err_te=np.zeros((lambdas.size,degrees.size))
    for ind_lamb,lambda_ in enumerate(lambdas):
        #print(lambda_)
        for ind_deg, degree_ in enumerate(degrees):
            #print('DEGREE IS: ')
            #print(degree_)
            nb_err_te = np.zeros(k_fold)
            for k in range (k_fold):
                #print('K CONSIDERED IS: ')
                #print(k)
                result = logistic_cross_validation(y_train, x_train_cleaned, k_indices, k , lambda_, degree_, nmc_tr+1,noaf,logistic_type,max_iter, threshold)
                nb_err_te[k]= result

            mean_nb_err_te[ind_lamb,ind_deg]=nb_err_te.mean()
    return mean_nb_err_te