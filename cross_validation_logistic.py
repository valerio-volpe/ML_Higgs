import numpy as np
from regression_tools import * 
from preprocessing import *
from implementations import *

def build_k_indices(y, k_fold, seed):
    """build k indices for k-fold."""
    num_row = y.shape[0]
    interval = int(num_row / k_fold)
    np.random.seed(seed)
    indices = np.random.permutation(num_row)
    k_indices = [indices[k * interval: (k + 1) * interval]
                 for k in range(k_fold)]
    return np.array(k_indices)

def logistic_cross_validation(y, phi, k_indices, k, param_, degree, nmc , interactions, logistic_type, max_iter, threshold):
    """
    Return the loss of logistic regression.
    """
    
    # Create the test and train samples
    train_indices = np.delete(k_indices , k , 0).reshape((k_indices.shape[0]-1) * k_indices.shape[1])
    x_test = phi[k_indices[k],:]
    x_train = phi[train_indices,:]
    y_test = y[k_indices[k]]
    y_train = y[train_indices]
    
    # Create the initial solution
    initial_w=np.zeros(x_train.shape[1],)
    
    if logistic_type==0:
        # In this case the parameter is GAMMA
        w, loss = logistic_regression(y_train, x_train, initial_w, max_iter, param_)
    elif logistic_type==2:
        # In this case the parameter is LAMBDA
        initial_w = 5 * np.ones(x_train.shape[1])
        gamma = 1e-5
        w , loss = reg_logistic_regression(y_train, x_train,param_,initial_w,max_iter,gamma)
    
    # Calculate the result
    w = w.reshape(-1,)
    result=(y_test==(sigmoid(x_test.dot(w))>0.5)).sum()/y_test.shape[0]
    return result

def cross_validation_logistic_demo(y_train_input,x_train,degrees,k_fold,parameters,seed,logistic_type, max_iter=1000, threshold=1e-8):
    """
    Performs cross validation.
    logistic_type:
        0: gradient descent                     
        2: penalised gradient descent
    """
    
    # Clean data 
    x_train_cleaned,nmc_tr=cleaning_function(x_train,-999)
    
    # Feature augmentation
    x_train_cleaned,noaf=features_augmentation(x_train_cleaned,not_augm_features=nmc_tr+1)

    # Matrix to store the mean result (over k quantities) at each step
    mean_nb_err_te=np.zeros((parameters.size,degrees.size))
    
    for ind_param,param_ in enumerate(parameters):
        for ind_deg, degree_ in enumerate(degrees):
            # Vector to store the result for each k-fold
            nb_err_te = np.zeros(k_fold) 
            
            # Build the polinomial to train
            phi_train = build_polinomial(x_train_cleaned,degree_,not_poly_features=noaf+nmc_tr+1,nm=999,already_cleaned=True)

            # Standardize the data
            phi_train=norm_data(phi_train,not_norm_features=nmc_tr+1,skip_first_col=True)

            # Normalize with the maximum value
            phi_train = norm_max(phi_train)
                
            y_train = y_train_input
            
            # Select pseudo-randomly a subset
            y_train, phi_train = retrieve_subset(y_train,phi_train,int(phi_train.shape[0]/25), seed)
            
            # split data in k fold
            k_indices = build_k_indices(y_train, k_fold, seed)
                
            for k in range (k_fold):
                # Retrieve the loss
                result = logistic_cross_validation(y_train, phi_train, k_indices, k , param_, degree_, nmc_tr+1,noaf,logistic_type,max_iter, threshold)
                
                #Store the result
                nb_err_te[k]= result

            mean_nb_err_te[ind_param,ind_deg]=nb_err_te.mean()
    
    return mean_nb_err_te