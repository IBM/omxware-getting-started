# utils for ml model training

import pandas as pd
import numpy as np
import sklearn
from sklearn.metrics import classification_report
from sklearn.model_selection import LearningCurveDisplay, learning_curve
from sklearn.metrics import RocCurveDisplay, confusion_matrix
import matplotlib.pyplot as plt
from sklearn.svm import SVC, LinearSVC
from sklearn import svm
from joblib import dump, load
import sys
import csv
from sklearn.decomposition import PCA
import os
from skopt.space import Real, Categorical, Integer
import xgboost as xgb
from sklearn.pipeline import Pipeline
from skopt import BayesSearchCV
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import StandardScaler
import copy
from sklearn.metrics import roc_auc_score
from sklearn.metrics import roc_curve
from sys import exit

DATA_PATH = os.getenv('DATA_PATH')
MODEL_PATH = os.getenv('MODEL_PATH')
RESULTS_PATH = os.getenv('RESULTS_PATH')
DRY_RUN = os.getenv('DRY_RUN')
if DRY_RUN == 'True':
    DRY_RUN = True
elif DRY_RUN == 'False':
    DRY_RUN = False
else:
    raise RuntimeError("Incorrect value for DRY_RUN")
NUM_JOBS = int(os.getenv('NUM_JOBS'))

TYPES_OF_MODELS = ['SVM', 'XGBoost', 'Baseline', 'Baseline_tuned']
TYPES_SCALING_STRATEGY = ['standard', 'minmax']

RANDOM_STATE_NUMBER = 42
XGBOOST_MAX_TREE_DEPTH = 25
BASELINE_MAX_TREE_DEPTH = 10
BAYES_SEARCH_CV = 5

XGBOOST_DRY_RUN_PARAM_GRID = [
                {

                'xgb__alpha': Real(1e-1, 1e+1, prior='log-uniform'),   # L1 regularization (alpha)
                'xgb__lambda': Real(1e-1, 1e+1, prior='log-uniform'),  # L2 regularization (lambda)
                'xgb__n_estimators': (50, 60),                  # Number of boosting rounds (trees)
                'xgb__learning_rate': Real(0.1, 0.2, prior='log-uniform'),  # Step size shrinkage during boosting

                }  
                ]

XGBOOST_PARAM_GRID = [
                {

                'xgb__alpha': Real(1e-6, 1e+3, prior='log-uniform'),   # L1 regularization (alpha)
                'xgb__lambda': Real(1e-6, 1e+3, prior='log-uniform'),  # L2 regularization (lambda)
                'xgb__n_estimators': (50, 100, 200, 300, 500),                  # Number of boosting rounds (trees)
                'xgb__learning_rate': Real(0.01, 1.0, prior='log-uniform'),  # Step size shrinkage during boosting

                }  
                ]

XGBOOST_BASELINE_TUNED_PARAM_GRID = [
                {

                'xgb__alpha': Real(1e-3, 1e+3, prior='log-uniform'),   # L1 regularization (alpha)
                'xgb__lambda': Real(1e-3, 1e+3, prior='log-uniform'),  # L2 regularization (lambda)
                'xgb__n_estimators': (50, 60, 100, 200),                  # Number of boosting rounds (trees)
                'xgb__learning_rate': Real(0.1, 0.7, prior='log-uniform'),  # Step size shrinkage during boosting

                }  
                ]

SVM_DRY_RUN_PARAM_GRID = [
                            {

                            'pca__n_components':[0.99999],    
                            'svc__C': [1],
                            'svc__gamma': [0.1],
                            'svc__max_iter':[5000], 
                            'svc__kernel':['linear']

                            }  
                        ]

SVM_PARAM_GRID = [
                {

                'pca__n_components':[0.9, 0.95, 0.98, 0.99, 0.99999],    
                'svc__C': (1e-6, 1e+6, 'log-uniform'),
                'svc__gamma': (1e-6, 1e+3, 'log-uniform'),
                'svc__max_iter':[1000000], 
                'svc__kernel':['linear']

                }  
                ]

# ALL MODEL DEISNG AND HYPER PARAMS ARE LISTED IN THE CLASS FUNCTIONS

sys.path.append(os.getenv('SOURCE_PATH'))



class MachineLearning:

    def __init__(self, feature_selection_pipeline, train_X, train_Y, test_X, test_Y, save_path = MODEL_PATH, \
                 run_model = 'SVM', scaling_strategy = 'standard', dry_run = DRY_RUN , number_of_jobs = NUM_JOBS):
        
        self.pipeline_steps = copy.deepcopy(feature_selection_pipeline)
        self.dry_run = dry_run
        self.n_jobs = number_of_jobs
        if scaling_strategy in TYPES_SCALING_STRATEGY:
            self.scaling_strategy = scaling_strategy
        else:
            raise Exception("Invalid scaling strategy.")
        
        self.train_X = copy.deepcopy(train_X)
        self.test_X = copy.deepcopy(test_X)
        
        if isinstance(train_Y, np.ndarray):
            self.train_Y = copy.deepcopy(train_Y)
        else:
            self.train_Y = np.ravel(copy.deepcopy(train_Y))

        
        if isinstance(test_Y, np.ndarray):
            self.test_Y = copy.deepcopy(test_Y)
        else:
            self.test_Y = np.ravel(copy.deepcopy(test_Y))
        
        if run_model in TYPES_OF_MODELS:
            self.model_algorithm = run_model
        else:
            print(run_model)
            raise Exception("Incorrect model")
        
        #if developing new model type, add here
        if self.model_algorithm == 'XGBoost':
            self.run_xgboost()
        elif self.model_algorithm == 'SVM':
            self.run_svm()
        elif self.model_algorithm == 'Baseline':
            self.run_baseline()
        elif self.model_algorithm == 'Baseline_tuned':
            self.run_baseline_tuned()
        else:
            raise Exception("Model algo not recognized.")
        
        self.save_path = copy.deepcopy(save_path)
        self.model_save_path = os.path.join(self.save_path, self.model_algorithm)
        
        
        # self.run_pipeline()
        # self.save_model()
        # self.analyze_output(display_learning_curves = True, save_only = True)

    def run_baseline(self):

        self.param_grid = []
    
    def run_baseline_tuned(self):
        
        self.param_grid = XGBOOST_BASELINE_TUNED_PARAM_GRID
        
        xgb_ = xgb.XGBClassifier(objective="binary:logistic", random_state=RANDOM_STATE_NUMBER, \
                                      max_depth = XGBOOST_MAX_TREE_DEPTH, sampling_method = 'gradient_based')
        
        self.pipeline_steps.append(("xgb", xgb_))
        
    def run_xgboost(self):
        
        if self.dry_run:
            self.param_grid = XGBOOST_DRY_RUN_PARAM_GRID
        else: 
            self.param_grid = XGBOOST_PARAM_GRID
        
        xgb_ = xgb.XGBClassifier(objective="binary:logistic", random_state=RANDOM_STATE_NUMBER, \
                                      max_depth = XGBOOST_MAX_TREE_DEPTH, sampling_method = 'gradient_based')
        
        self.pipeline_steps.append(("xgb", xgb_))
    
    def run_svm(self):
        
        if self.dry_run:
            self.param_grid = SVM_DRY_RUN_PARAM_GRID

        else:
            self.param_grid = SVM_PARAM_GRID

        scaler = StandardScaler()
        svm_ = svm.SVC(probability = True,)
        pca_ = PCA()
        
        self.pipeline_steps.append(("scaler", scaler))
        self.pipeline_steps.append(("pca", pca_))
        self.pipeline_steps.append(("svc", svm_))

    
    def run_pipeline(self):
        
        self.pipeline_ = Pipeline(self.pipeline_steps)
        if self.dry_run:
            self.n_iter = 1
        else:
            self.n_iter = 50

        if self.model_algorithm == 'Baseline':

            self.model = xgb.XGBClassifier(n_estimators = 100, objective="binary:logistic", random_state=42, \
                                           max_depth = BASELINE_MAX_TREE_DEPTH, sampling_method = 'gradient_based', \
                                           n_jobs = self.n_jobs, reg_alpha = 0.1)
            
            self.model.fit(self.train_X, self.train_Y)
            
        else:
            
            
            self.bayes_search = BayesSearchCV(
                            estimator=self.pipeline_,
                            search_spaces=self.param_grid,
                            scoring='accuracy',
                            cv=BAYES_SEARCH_CV,
                            n_points = 10,
                            n_jobs=self.n_jobs,
                            n_iter=self.n_iter,  # Number of iterations (function evaluations) for Bayesian optimization
                            refit=True,
                            random_state=RANDOM_STATE_NUMBER
                        )
            print("Total Iterations for bayes search:", self.bayes_search.total_iterations, flush = True)
            
            try:
                self.bayes_search.fit(self.train_X, self.train_Y)
            
            except Exception as e:
                print("Exception Occurred in run_pipeline", flush = True)
                print(str(e))
                print(self.train_X)
                print(self.train_Y)
            
            # xgb_params = self.bayes_search.best_params_ 
            # self.model = xgb.XGBClassifier(**xgb_params)
            self.model = self.bayes_search.best_estimator_
  
    def load_model_from_file(self):
        self.model = load(self.model_save_path)
                            
    def save_model(self):
        print(self.save_path, flush = True)          
        os.makedirs(self.save_path, exist_ok = True)
        dump(self.model, self.model_save_path)
        print("Saved Model to: {}".format(self.save_path))
    
    def get_model_metrics(self):
        
        return self.auc, self.f_1, self.classification_score
    
    def analyze_output(self, display_learning_curves = False, save_metrics = True, save_only = True):
        
        self.ml_output_metrics(save_metrics)
        
        if display_learning_curves:
            self.output_learning_curves(save_only)
    
    def ml_output_metrics(self, save = True):
        
        if sklearn.__version__ < '1.3.1':
            raise RuntimeError("Incorrect sklearn version {}. For testing/inferencing it needs to be 1.3.1 or greater".format(sklearn.__version__))
            exit()
        elif np.__version__ < "1.26.1":
            raise RuntimeError("Incorrect numpy version {}. For testing/inferencing it needs to be 1.26.1 or greater".format(np.__version__))   
            exit()
        else:
            pass 

        self.classification_score = self.model.score(self.test_X, np.ravel(self.test_Y))
        print(f"Classification Score: {self.classification_score}")
        testing_subset = copy.deepcopy(self.test_X[:10])
        print("Sample test set:",np.sum(testing_subset, axis = 1))
        print("Predicted Prob:", self.model.predict_proba(testing_subset))
        print("Actual Label:", self.test_Y[:10])
        print("Predicted Label:", self.model.predict(testing_subset))
        # print("Sample output predicted probabilities:",format(self.model.predict_proba(self.test_X)[:10], self.test_Y[:10], self.model.predict(self.test_X)[:10]))

        if isinstance(self.test_Y, np.ndarray):
            df_test_Y = pd.DataFrame(self.test_Y, columns = ['LABEL'])
        else:
            df_test_Y = self.test_Y     
        
        self.class_report = classification_report(\
                                                  np.ravel(self.test_Y), \
                                                  self.model.predict(self.test_X), \
                                                  output_dict = True, \
                                                  labels = [0,1], \
                                                  zero_division = 0)
        
        self.df_class = pd.DataFrame(self.class_report).transpose()
        
        if save:
            self.df_class.to_csv(\
                                 os.path.join(\
                                  self.save_path,\
                                  f'{self.model_algorithm}_classification_matrix.csv'))
        
        print(self.df_class)
        
        self.f_1 = classification_report(self.test_Y, \
                                        self.model.predict(self.test_X), \
                                         output_dict = True, \
                                         labels = [0,1], \
                                         zero_division=0)['macro avg']['f1-score']
        try:
            self.auc = roc_auc_score(self.model.predict(self.test_X), self.test_Y)
        except ValueError:
            print("UNABLE TO CALCULATE AUC SINCE ONLY ONE CLASS IN OUTPUT")
            self.auc = -1
        
    def output_learning_curves(save_only = True):
        
        if isinstance(self.test_Y, np.ndarray):
            df_test_Y = pd.DataFrame(self.test_Y, columns = ['LABEL'])
        else:
            df_test_Y = self.test_Y
        
        if df_test_Y.LABEL.value_counts().shape[0] == 2:
            roc_curve = RocCurveDisplay.from_estimator(self.model, self.test_X, self.test_Y)
        
        if display_learning_curves:
            learning_curve = LearningCurveDisplay.from_estimator(\
                                                     self.model, \
                                                     self.train_X, \
                                                     self.train_Y, \
                                                     score_type = 'both')
        
        if save_only:
            # Create a figure and plot the ROC curve
            plt.figure(figsize=(80, 80))  # Can adjust the figure size if needed
            roc_curve.plot()

            # Save the figure to a file (e.g., 'roc_curve.png')
            plt.savefig(os.path.join(RESULTS_PATH, 'roc_curve.png'))

            # Close the figure to release resources (optional)
            plt.close()
            
            # Create a figure and plot the ROC curve
            plt.figure(figsize=(800,800))  # You can adjust the figure size if needed
            learning_curve.plot()

            # Save the figure to a file (e.g., 'roc_curve.png')
            plt.savefig(os.path.join(RESULTS_PATH, 'learning_curve.png'))

            # Close the figure to release resources (optional)
            plt.close()

    
    
    def get_calculate_confusion_matrix_scores(self):
        
        self.tn, self.fp, self.fn, self.tp = confusion_matrix(\
                                                              self.test_Y,\
                                                              self.model.predict(self.test_X)).ravel()
        
        return self.tn, self.fp, self.fn, self.tp

    def get_precision_recall(self):

        return self.df_class['precision'].loc['0'], \
                self.df_class['recall'].loc['0'], \
                self.df_class['precision'].loc['1'], \
                self.df_class['recall'].loc['1']
        
    def get_precision_recalls_from_file(self):

        df_pr = pd.read_csv(os.path.join(\
                             self.save_path, \
                             f'{self.model_algorithm}_classification_matrix.csv'), \
                             index_col = 0, header = 0)
        
        print(df_pr.index)
        return df_pr['precision'].loc['0'], \
                df_pr['recall'].loc['0'], \
                df_pr['precision'].loc['1'], \
                df_pr['recall'].loc['1']

    
    

             
