import pandas as pd
import numpy as np
import os
from os.path import join
from sklearn.pipeline import Pipeline
import csv
import sys
import time

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


OUTPUT_RESULTS_FILE = 'virulence++_model_results.csv'

all_hosts_file = 'features_and_output/df_data_all_hosts.csv'
human_hosts_file = 'features_and_output/df_data_humans.csv'
genome_metadata_file = 'metadata/genome_complete_metadata.csv'
mlst_metadata_file = 'metadata/IBM_virulence_mlst_revised.csv'

data_obj = Data(DATA_PATH, all_hosts_file, human_hosts_file, genome_metadata_file, mlst_metadata_file)

host_type = {
    'human': data_obj.df_data_human_hosts,
    'all hosts': data_obj.df_data_all_hosts
}
model_type = ['hv_vs_lv', 'vir_vs_nvir']
algo_type = ['SVM', 'XGBoost']
split_data = ['from_metadata', 'regular']
oversampling = [False, True]
oversampling_method = ['random', 'SMOTE', 'ADASYN']
include_non_kp_genomes_in_training = ['NO', 'TRAINING-ONLY'] 
include_non_kp_genomes_in_testing = ['NO', 'YES'] #if not testing models and actually training, then set this to empty list


file_name = join(RESULTS_PATH, OUTPUT_RESULTS_FILE)

# Writing data to the CSV file
f = open(file_name, mode='w', newline='')
writer = csv.writer(f)
writer.writerow(["HOST_TYPE", "MODEL_TYPE", "INCLUDE_NON_KP_GENOMES_IN_TRAINING", "INCLUDE_NON_KP_GENOMES_IN_TESTING", \
            "OVERSAMPLING", "OVERSAMPLING_METHOD", "ALGO", "F-1", "AUC", "CLASSIFICATION SCORE", "CLASS0 PRECISION", "CLASS0 RECALL", "CLASS1 PRECISION", "CLASS1 RECALL", "PATH"])


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
                    for each_include_non_kp_in_testing in include_non_kp_genomes_in_testing:
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
                                                    include_non_kp_genomes = each_include_non_kp_in_testing)
                        
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

                        

                        ml_obj2.load_model_from_file()
                        ml_obj2.analyze_output(save_metrics = False)
                        auc, f_1, classification_score = ml_obj2.get_model_metrics()
                        class0_precision, class0_recall, class1_precision, class1_recall = ml_obj2.get_precision_recalls_from_file()
                        writer.writerow([each_host_type, each_model_type, \
                                         each_include_non_kp_genomes, each_include_non_kp_in_testing,\
                                         each_oversampling, "ADASYN", each_algo_type, f_1, auc, \
                                         classification_score,class0_precision,\
                                         class0_recall, class1_precision, class1_recall ,save_path])
                        f.flush()


                        print("ML Model Metrics written to file in time:",time.time() - start_time ,flush = True)

                        if DRY_RUN:
                            exit()

f.close()
                    
