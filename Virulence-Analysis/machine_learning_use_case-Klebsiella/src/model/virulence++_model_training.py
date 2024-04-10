# virulence++ model training

import pandas as pd
import numpy as np
from os.path import join
import os, sys
from sklearn.pipeline import Pipeline
import time
import csv

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

from data_prep import Data, MLDataPrep
from exploratory_data_analysis import EDA
from model.model_utils import FeatureSelection, MachineLearning


all_hosts_file = 'features_and_output/df_data_all_hosts.csv'
human_hosts_file = 'features_and_output/df_data_humans.csv'
genome_metadata_file = 'metadata/genome_complete_metadata.csv'
mlst_metadata_file = 'metadata/IBM_virulence_mlst_revised.csv'

data_obj = Data(DATA_PATH, all_hosts_file, human_hosts_file, \
                genome_metadata_file, mlst_metadata_file)

host_type = {
    'human': data_obj.df_data_human_hosts,
    'all hosts': data_obj.df_data_all_hosts
}

model_type = ['hv_vs_lv', 'vir_vs_nvir']
algo_type = ['SVM', 'XGBoost']
split_data = ['from_metadata', 'regular']
oversampling = [True]
oversampling_method = ['random', 'SMOTE', 'ADASYN']
include_non_kp_genomes_in_training = ['NO', 'TRAINING-ONLY'] 
include_non_kp_genomes_in_testing = [] #if not testing models and actually training, then set this to empty list

for each_host_type in host_type.keys():
    print("Host type:", each_host_type, flush = True)
    for each_model_type in model_type:
        print("Model Type:", each_model_type, flush = True)
        for each_include_non_kp_genomes in include_non_kp_genomes_in_training:
            print("non kp genomes include type:", each_include_non_kp_genomes, flush = True)
            for each_oversampling in oversampling:
                print("Oversampling Done?:", each_oversampling)
                for each_algo_type in algo_type:
                    start_time = time.time()
                    print("Algo type:", each_algo_type, flush = True)
                    
                    ml_data_prep_obj = MLDataPrep(df_input = host_type[each_host_type], \
                                                df_mlst_data = data_obj.df_mlst_metadata, \
                                                label_column = 'LABEL', host_type = each_host_type, \
                                                drop_labels = True, \
                                                label_encoding_scheme = each_model_type,\
                                                label_encoding_dict = None, \
                                                split_data = 'from metadata', test_size = 0.3,\
                                                oversampling = each_oversampling, \
                                                oversampling_method = 'ADASYN', random_weight = None, \
                                                reset_index = True, drop_columns = True, \
                                                columns_to_drop = ['ACCESSION_NUMBER'],\
                                                include_non_kp_genomes = each_include_non_kp_genomes)

                    train_X, train_Y, test_X, test_Y = ml_data_prep_obj.return_train_test_sets()
                    print("Data Prep Completed in time:",time.time() - start_time, flush = True)

                    feature_selection_obj = FeatureSelection(train_X, train_Y)
                    feature_pipe = feature_selection_obj.run_standard_feature_selection(add_sklearn_pipeline_object_only=True)
                    print("Feature Selection Pipeline Build Completed in time:",time.time() - start_time, flush = True)

                    if DRY_RUN:
                        save_path = "TEST"+each_host_type + '_' + each_model_type + \
                                '_' + 'oversampled_' + str(each_oversampling) + '_' + 'ADASYN' + '_' \
                                + 'include_non_kp_genomes' + '_' + each_include_non_kp_genomes
                    else:
                        save_path = each_host_type + '_' + each_model_type + \
                                '_' + 'oversampled_' + str(each_oversampling) + '_' + 'ADASYN' + '_' \
                                + 'include_non_kp_genomes' + '_' + each_include_non_kp_genomes
                    
                    save_path = join('VIRULENCE++_MODELS', save_path)
                    final_save_path = join(MODEL_PATH, save_path)
                    # print(save_path)
                    
                    ml_obj2 = MachineLearning(feature_pipe, train_X, train_Y, test_X, test_Y, \
                                            save_path = final_save_path,run_model = each_algo_type, \
                                              dry_run = DRY_RUN, number_of_jobs = NUM_JOBS)

                    
                    ml_obj2.run_pipeline()
                    print("ML Model Pipeline Run Completed in time:",time.time() - start_time ,\
                          flush = True)

                    ml_obj2.save_model()
                    print("ML Model Saved in time:",time.time() - start_time ,flush = True)

                    ml_obj2.analyze_output(display_learning_curves = False, \
                                           save_only = True) #this saves the model output metrics

                    print("ML Model Output Analysis Completed in time:",time.time() - start_time ,\
                          flush = True)

                    if DRY_RUN:
                        exit()

                    
