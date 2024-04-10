import pandas as pd
import csv
from os.path import join
import os, sys

RESULTS_PATH = os.getenv('RESULTS_PATH')

BASELINE_RESULTS_FILE_NAME = 'baseline_tuned_model_results.csv'
VIRULENCE_RESULTS_FILE_NAME = 'virulence++_model_results.csv'
# GITHUB_PREPEND_LINK = ''
OUTPUT_FILE = 'complete_ml_results.csv'

def load_file(filename):
    df = pd.read_csv(join(RESULTS_PATH, filename))
    return df

def check_consolidated_file_sanity_baseline(df):
    pass

def add_and_order_columns(df, filename, feature_type):
    
#     #github source column
#     df['GITHUB_SOURCE'] = join(GITHUB_PREPEND_LINK, \
        
#                                 filename) 
    
    #feature type column
    df['FEATURE_TYPE'] = feature_type

    #tag error analysis column
    df['TAG_ERROR_ANALYSIS'] = 'N'

    #order columns
    cols = ['TAG_ERROR_ANALYSIS', 'HOST_TYPE', 'MODEL_TYPE', 'FEATURE_TYPE',\
               'INCLUDE_NON_KP_GENOMES_IN_TRAINING', 'INCLUDE_NON_KP_GENOMES_IN_TESTING',\
                'OVERSAMPLING', 'OVERSAMPLING_METHOD', 'ALGO', \
                  'F-1','AUC','CLASSIFICATION SCORE',\
                    'CLASS0 PRECISION','CLASS0 RECALL','CLASS1 PRECISION','CLASS1 RECALL',\
                        'PATH']#,'GITHUB_SOURCE']
    df = df[cols]

    return df

def concatenate_baseline_and_virulence_results_files(df_baseline, df_virulence):
    
    df_consolidated = pd.concat([df_baseline, df_virulence])
    return df_consolidated

def sort_consolidated_results_file(df):
    
    df = df.sort_values(by=['MODEL_TYPE','HOST_TYPE','INCLUDE_NON_KP_GENOMES_IN_TRAINING','INCLUDE_NON_KP_GENOMES_IN_TESTING', \
                       'FEATURE_TYPE', 'F-1'], ascending = [True, True, True, True, True, False], axis = 0)
    return df


if __name__ == "__main__":

    df_baseline = load_file(BASELINE_RESULTS_FILE_NAME)
    df_baseline = add_and_order_columns(df_baseline, BASELINE_RESULTS_FILE_NAME, 'baseline')    

    df_virulence = load_file(VIRULENCE_RESULTS_FILE_NAME)
    df_virulence = add_and_order_columns(df_virulence, VIRULENCE_RESULTS_FILE_NAME, 'virulence++')

    df_consolidated = concatenate_baseline_and_virulence_results_files(df_baseline, df_virulence)
    df_consolidated_sorted = sort_consolidated_results_file(df_consolidated)

    df_consolidated_sorted.to_csv(join('./',RESULTS_PATH, OUTPUT_FILE), index = False)
