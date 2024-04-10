#!/usr/bin/env python
# coding: utf-8

# # TRAINING BASELINE MODELS

import pandas as pd
import numpy as np
import copy
import os
from copy import deepcopy
from os.path import join
import csv
import sys
import time


DATA_PATH = os.getenv('DATA_PATH')
MODEL_PATH = os.getenv('MODEL_PATH')
RESULTS_PATH = os.getenv('RESULTS_PATH')
DRY_RUN = os.getenv('DRY_RUN')
NUM_JOBS = os.getenv('NUM_JOBS')
sys.path.append(os.getenv('SOURCE_PATH'))

from data_prep import Data, MLDataPrep

def read_baseline_data():
    
    df = pd.read_csv(join(DATA_PATH, 'genome_protein_data/kp_genome_pivot_neighbor_domain_count_final.csv'))
    return df

def transform_baseline_data(df_original):
    
    df = copy.deepcopy(df_original)
    pivot_filter = df['NEIGHBOR_TYPE'] == 'P' #selecting pivot proteins
    df_pivot_proteins_only = df.loc[pivot_filter]
    df_pivot_proteins_only.drop(columns=['NEIGHBOR_DOMAIN_ARCHITECTURE_UID_KEY', 'NEIGHBOR_TYPE'], inplace = True)

    df_grouped_accession_pivot_proteins_only = df_pivot_proteins_only.groupby('ACCESSION_NUMBER')
    
    # Check if pivot domain architecture are unique per accession i.e. each domain architecture uid is listed only once
    new =\
            df_grouped_accession_pivot_proteins_only\
            .PIVOT_DOMAIN_ARCHITECTURE_UID_KEY.unique().apply(len)\
            == df_grouped_accession_pivot_proteins_only\
            .PIVOT_DOMAIN_ARCHITECTURE_UID_KEY.count()

    # we see that it is not unique, thus we need to groupby ACCESSION and \
    # PIVOT_DOMAIN_ARCHITECTURE_UID_KEY and do a sum of the count so that we can use DataFrame.pivot
    df_aggregated = df_pivot_proteins_only.groupby(['ACCESSION_NUMBER',\
                                                    'PIVOT_DOMAIN_ARCHITECTURE_UID_KEY']).sum()

    df_new = df_aggregated.reset_index().pivot(index = 'ACCESSION_NUMBER', columns = \
                                               'PIVOT_DOMAIN_ARCHITECTURE_UID_KEY', values = 'COUNT')

    # will have a couple of NaN's because not all accessions will have all domain\
    # architectures. Replace them with 0
    df_new.fillna(0, inplace = True)
    df_baseline_feature_matrix = copy.deepcopy(df_new)
    df_baseline_feature_matrix.head()
    df_baseline_feature_matrix.reset_index(inplace = True)

    # ## LOAD LABEL DATA

    data_path = DATA_PATH
    all_hosts_file = 'features_and_output/df_data_all_hosts.csv'
    human_hosts_file = 'features_and_output/df_data_humans.csv'
    genome_metadata_file = 'metadata/genome_complete_metadata.csv'
    mlst_metadata_file = 'metadata/IBM_virulence_mlst_revised.csv'

    data_obj = Data(data_path, all_hosts_file, human_hosts_file, \
                    genome_metadata_file, mlst_metadata_file)

    df_humans = data_obj.df_data_human_hosts[['ACCESSION_NUMBER', 'LABEL']]
    df_all_hosts = data_obj.df_data_all_hosts[['ACCESSION_NUMBER', 'LABEL']]
    
    # JOIN WITH HUMAN AND ALL HOST DATA 
    df_baseline_human_hosts = pd.merge(df_baseline_feature_matrix, df_humans, on='ACCESSION_NUMBER', how = 'inner')
    df_baseline_all_hosts = pd.merge(df_baseline_feature_matrix, df_all_hosts, on='ACCESSION_NUMBER', how = 'inner')
    
    return df_baseline_human_hosts, df_baseline_all_hosts