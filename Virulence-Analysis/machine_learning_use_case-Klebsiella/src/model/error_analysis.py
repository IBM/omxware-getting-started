# file for error analysis

import pandas as pd
import numpy as np
from sklearn.metrics import classification_report
from sklearn.model_selection import LearningCurveDisplay, learning_curve
from sklearn.metrics import RocCurveDisplay
import matplotlib.pyplot as plt
from sklearn.svm import SVC, LinearSVC
from sklearn import svm
from joblib import dump, load
import csv
from sklearn.decomposition import PCA
import os, sys
from skopt.space import Real, Categorical, Integer
import xgboost as xgb
from sklearn.pipeline import Pipeline
from skopt import BayesSearchCV
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import StandardScaler
import copy
from sklearn.metrics import roc_auc_score
from sklearn.metrics import roc_curve
from typing import List, Dict

from os.path import join
from collections import defaultdict
import traceback

import unittest
import sys
import warnings
warnings.filterwarnings('ignore')

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

sys.path.append(os.getenv('SOURCE_PATH'))

from data_prep import Data, MLDataPrep, read_baseline_data, transform_baseline_data
from exploratory_data_analysis import EDA
from model.model_utils import FeatureSelection, MachineLearning



MODEL_RESULTS_FILE = None
MODEL_CONSOLIDATED_RESULTS_FILE = join(RESULTS_PATH, 'complete_ml_results.csv')

ALLOWED_FEATURE_TYPES = ['baseline','virulence++']

HOST_TYPE_LIST = ['human', 'all hosts']
MODEL_TYPE_LIST = ['hv_vs_lv', 'vir_vs_nvir']

def select_top_model(results_file : str = MODEL_RESULTS_FILE, group_by_columns: List[str] = ['HOST_TYPE', 'MODEL_TYPE'], filter_by: dict = {'ALGO':'XGBoost'}, sort_by_columns : List[str] = ['F-1'], get_top_n: int = 1):

    ml_results = pd.read_csv(results_file, header = 0)
    
    #filter by column and value
    for each_key in filter_by.keys():
        filt = ml_results[each_key] == filter_by[each_key]
        ml_results = ml_results.loc[filt]
    
    # now group by columns

    ml_results_groupby = ml_results.groupby(group_by_columns)

    ml_results_top_entry = ml_results_groupby.apply(lambda x:x.sort_values(sort_by_columns, \
                                                    ascending = False).head(1)).reset_index(drop = True)

    return ml_results_top_entry

def load_model(model_path):

    ml_model = load(model_path)
    return ml_model

def run_inference(ml_model, data):
    """
    return precision, recall and F-1 scores for each class
    """
    run_inference_single_group(ml_model, data)

def get_score(score_dict, label, score_type):
    
    score = score_dict[label][score_type]
    if np.isnan(score):
        return -1
    elif not np.isnan(score):
        return score
    else:
        raise Exception("assigned score from classification_report not integer >= 0. Score:", score)

def run_inference_single_group(X, ml_model, baseline = False, host = 'human', print_report = True, get_results_only = False):
    
    X_copy = copy.deepcopy(X)

    if baseline:
        
        if host == 'human':
            host_name = 'HUMAN'
        elif host == 'all hosts':
            host_name = 'ALL'
        
        X_new = X_copy.drop(columns = ['ACCESSION_NUMBER', f'TRAINING_SET_{host_name}_HOSTS',\
                                       f'TESTING_SET_{host_name}_HOSTS', 'Scheme', 'LABEL', 'Full_ST'])
    else:
        X_new = X_copy[[str(item) for item in range(3905)]]
    
    y = ml_model.predict(X_new)
    
    X_copy['predicted_label'] = y
    if get_results_only:
        return X_copy[['LABEL', 'predicted_label']]
    
    zero_division = np.nan
    class_report = classification_report(X_copy['LABEL'], X_copy['predicted_label'], \
                                         output_dict = True, zero_division=zero_division, labels=[0,1])
    try:
        precision_0 = get_score(class_report, '0', 'precision')
        if np.isnan(precision_0):
            precision_0 = -1
        
        precision_1 = get_score(class_report, '1', 'precision')
        if np.isnan(precision_1):
            precision_1 = -1
        
        recall_0 = get_score(class_report, '0', 'recall')
        if np.isnan(recall_0):
            recall_0 = -1
        
        recall_1 = get_score(class_report, '1', 'recall')
        if np.isnan(recall_1):
            recall_1 = -1
        
        f1 = get_score(class_report, 'macro avg', 'f1-score')
        if np.isnan(f1):
            f1 = -1

    except Exception as e:
        print(e)
        print(traceback.format_exc())
        print(class_report)
        exit()
    
    if print_report:
        print(X_copy['LABEL'])
        print(X_copy['predicted_label'])
        print(classification_report(X_copy['LABEL'], X_copy['predicted_label'], \
                                    output_dict = False, zero_division=zero_division, labels=[0,1]))
        print([precision_0, recall_0, precision_1, recall_1, f1])

    return precision_0, recall_0, precision_1, recall_1, f1
    

def load_test_set(host: str = 'human', model_type: str = 'hv_vs_lv', \
                  split_data: str = 'from metadata', baseline: bool = False, \
                  include_non_kp_in_testing = 'YES'):

    all_hosts_file = 'features_and_output/df_data_all_hosts.csv'
    human_hosts_file = 'features_and_output/df_data_humans.csv'
    genome_metadata_file = 'metadata/genome_complete_metadata.csv'
    mlst_metadata_file = 'metadata/IBM_virulence_mlst_revised.csv'

    data_obj = Data(DATA_PATH, all_hosts_file, human_hosts_file, genome_metadata_file, mlst_metadata_file)

    if baseline:
        df = read_baseline_data()
        df_baseline_human_hosts, df_baseline_all_hosts = transform_baseline_data(df)
        host_type = {
            'human': df_baseline_human_hosts,
            'all hosts': df_baseline_all_hosts
        }
    else:
        host_type = {
            'human': data_obj.df_data_human_hosts,
            'all hosts': data_obj.df_data_all_hosts
        }
    
    ml_data_prep_obj = MLDataPrep(df_input = host_type[host], \
                                                df_mlst_data = data_obj.df_mlst_metadata, \
                                                label_column = 'LABEL', host_type = host, \
                                                drop_labels = True, \
                                                label_encoding_scheme = model_type,\
                                                label_encoding_dict = None, \
                                                split_data = split_data, test_size = -1,\
                                                oversampling = False, \
                                                oversampling_method = 'ADASYN', random_weight = None, \
                                                reset_index = True, drop_columns = False, \
                                                include_non_kp_genomes = include_non_kp_in_testing)

    train_X, train_Y, test_X, test_Y = ml_data_prep_obj.return_train_test_sets()
    return test_X, test_Y

def join_test_set_with_ST_data(test_X):
    
    mlst_metadata_file = 'metadata/IBM_virulence_mlst_revised.csv'

    df_metadata = pd.read_csv(join(DATA_PATH, mlst_metadata_file), header = 1)
    
    df_metadata = df_metadata[['ACCESSION_NUMBER', 'Full_ST']]

    test_X_with_ST = pd.merge(test_X, df_metadata, left_on = 'ACCESSION_NUMBER', \
                              right_on = 'ACCESSION_NUMBER', how = 'inner')
    return test_X_with_ST

def join_test_features_and_label(test_X, test_Y):

    df_test = test_X.join(test_Y)
    return df_test
    

def select_and_load_model(results_file: str = MODEL_RESULTS_FILE):

    if 'baseline' in results_file:
        df_ml_models = pd.read_csv(results_file)
    else:
        df_ml_models = select_top_model(results_file)
    
    dict_ml_models = {each_host: {each_model_type: None for each_model_type in MODEL_TYPE_LIST} for each_host in HOST_TYPE_LIST}
    for each_host in HOST_TYPE_LIST:
        for each_model_type in MODEL_TYPE_LIST:
            filt = (df_ml_models['HOST_TYPE'] == each_host) & (df_ml_models['MODEL_TYPE'] == each_model_type)
            model_algorithm = df_ml_models.loc[filt]['ALGO'].to_list()[0]
            model_path = df_ml_models.loc[filt]['PATH'].to_list()[0]
            final_model_path = join(model_path, model_algorithm)
            ml_model = load_model(final_model_path)
            dict_ml_models[each_host][each_model_type] = ml_model

    return dict_ml_models

def select_and_load_model_from_consolidated_results_file(results_file: str = \
                                                         MODEL_CONSOLIDATED_RESULTS_FILE,\
                                                        feature_type : str = 'baseline'):

    df = pd.read_csv(results_file)
    tag_values = df.TAG_ERROR_ANALYSIS.value_counts()
    print(tag_values)
    if tag_values['Y'] == 32:
        pass
    else:
        raise ValueError("Incorrect Number of Yes Tags.")
    
    #filter by feature type
    if feature_type == 'baseline':
        filt_feature_type = df['FEATURE_TYPE'] == 'baseline'
    elif feature_type == 'virulence++':
        filt_feature_type = df['FEATURE_TYPE'] == 'virulence++'
    else:
        raise Exception("Incorrect Feature Type Passed.")
    
    #filter by whether tag for error analysis is Y i.e. YES
    df = df.loc[filt_feature_type]
    filt_tag_error_analysis = df['TAG_ERROR_ANALYSIS'] == 'Y'
    df = df.loc[filt_tag_error_analysis]

    if df.shape[0] == 16:
        pass
    else:
        raise ValueError("Incorrect data frame size for feature type: {}.".format(feature_type))    
    return df


def run_error_analysis():
    

    list_results = [['HOST_TYPE', 'MODEL_TYPE', 'FEATURE_TYPE', \
                    'INCLUDE_NON_KP_GENOMES_IN_TRAINING', 'INCLUDE_NON_KP_GENOMES_IN_TESTING', 'OVERSAMPLING', \
                    'ST', '#SAMPLES_TEST_SET',\
                    'precision0', 'recall0', 'precision1', 'recall1', 'f1']]

    ## SELECT AND LOAD MODELS - 
    # saved to a nested dict with keys as host and then model type
    # dict_ml_models = select_and_load_model(results_file=MODEL_RESULTS_FILE)
    # dict_ml_models_baseline = select_and_load_model(results_file=MODEL_RESULTS_BASELINE)
    for feature_type in ALLOWED_FEATURE_TYPES:
        #first runs inference for baseline and then in next iteration of the loop for virulence++
        df_models = select_and_load_model_from_consolidated_results_file(results_file=MODEL_CONSOLIDATED_RESULTS_FILE,\
                                                            feature_type=feature_type)
        

        ## RUN INFERENCE - 
        # get F-1 and Precision Recall Scores per ST
        # we groupby ST and then call inference on each group using apply
        for index,row in df_models.iterrows():
            host = row['HOST_TYPE']
            model_type = row['MODEL_TYPE']
            include_non_kp_in_testing = row['INCLUDE_NON_KP_GENOMES_IN_TESTING']
            if feature_type == 'baseline':
                baseline = True
            else:
                baseline = False
            test_X, test_Y = load_test_set(host=host, model_type = model_type, baseline = baseline, \
                                           include_non_kp_in_testing=include_non_kp_in_testing)
            df_test = join_test_features_and_label(test_X, test_Y)
            df_test_with_ST = join_test_set_with_ST_data(df_test)
            df_grouped_by_ST = df_test_with_ST.groupby(['Full_ST'])
            model_path = join(MODEL_PATH, row['PATH'])
            model_algorithm = row['ALGO']
            ml_model = load_model(join(model_path,model_algorithm))
            for key in list(df_grouped_by_ST.groups.keys()):
                    # if key == 'Exclude': #these are fine to include actually, they are novel unnamed kp
                    #     continue
                    df_temp = df_grouped_by_ST.get_group(key)
                    p0, r0, p1, r1, f1 = run_inference_single_group(df_temp, ml_model, baseline = baseline, host = host)
                    list_results.append([host, model_type, feature_type, \
                                         row['INCLUDE_NON_KP_GENOMES_IN_TRAINING'], include_non_kp_in_testing, row['OVERSAMPLING'],\
                                         key, len(df_temp),\
                                         p0, r0, p1, r1, f1])

    import csv
    f = open(join(RESULTS_PATH,'error_analysis.csv'),'w')
    file_writer = csv.writer(f)
    for each_list in list_results:
        file_writer.writerow(each_list)
    f.close()


if __name__ == "__main__":

    run_error_analysis()
    