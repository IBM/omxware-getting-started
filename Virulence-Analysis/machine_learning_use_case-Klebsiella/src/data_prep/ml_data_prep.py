#Code to prepare data for machine learning

import pandas as pd
import numpy as np
from sklearn.model_selection import StratifiedShuffleSplit
from typing import List
import copy
import pdb
import sys
import os
sys.path.append(os.getenv('SOURCE_PATH'))

from data_prep import Data


class MLDataPrep(Data):
    
    def __init__(self, df_input : pd.DataFrame, df_mlst_data : pd.DataFrame, label_column : str = 'LABEL', host_type : str = None, \
                 drop_labels: bool = False, label_encoding_scheme : str = None, label_encoding_dict : dict = None, \
                 split_data : str = None, test_size : float = 0.1, oversampling : bool = False, oversampling_method = None, random_weight = None, \
                 reset_index : bool = True, drop_columns : bool = True, columns_to_drop : List[str] = ['ACCESSION_NUMBER'], include_non_kp_genomes: str = "NA"):
        
        """
        split_data can take "from metadata" or "regular"
        if "regular" is passed, then test_size also needs to be passed which is a float between 0.1 and 1.0
        "regular" does a random split
        "from metadata" is the split that was used during training of these models.
        
        label_encoding_scheme can take "hv_vs_lv" or "vir_vs_nvir" or "custom"
        if "custom" is passed, then label_encoding_dict needs to be passed
        
        host_type can be "human" or "all hosts"
        
        oversampling is True, then oversampling method can be ["random", "SMOTE", "ADASYN"]. 
        If it's "random", then pass None or don't pass anything in random_weight to do minority oversampling. Pass a float to do it by random weight.
        
        include_non_kp_genomes takes as values ["YES", "NO", "TRAINING-ONLY", "NA"]. Also note that to use include_non_kp_genomes with any option other than "NA", you must pass as input a dataframe which doesn't have non-kp genomes dropped.
        "YES" - expect full dataframe as input, with non-kp genomes included. 
        "NO" - expects full dataframe as input, with non-kp genomes included and then goes on to drop them completely before splitting the data.
        "TRAINING ONLY" - if split is from metadata, then that will be honored and any non-kp genomes in training will be kept. If split is regular, then the dataset will be split first on kp genomes only and then non-kp genomes will be added back to the training set.  
        
        """
        
        
        self.df_input = copy.deepcopy(df_input)
        self.df_mlst_metadata = copy.deepcopy(df_mlst_data)
        self.label_column = label_column
        self.drop_labels = drop_labels
        self.labels_to_drop = []
        self.columns_to_drop = columns_to_drop
        self.drop_columns = drop_columns
        self.reset_index = reset_index
        self.host_type = host_type
        self.include_non_kp_genomes = include_non_kp_genomes
        
        self.allowed_oversampling_methods = ["random", "SMOTE", "ADASYN"]
        self.allowed_responses_for_including_non_kp_genomes = ["YES", "NO", "TRAINING-ONLY", "NA"]
        
        
        # check conditions for including non kp genomes
        if self.include_non_kp_genomes not in self.allowed_responses_for_including_non_kp_genomes:
            raise Exception("Invalid value for include_non_kp_genomes")
        
        if self.include_non_kp_genomes == "NO":
            self.df_input = self.drop_non_kp_genomes_from_dataframes(self.df_input, self.df_mlst_metadata)
            self.df_input= self.drop_column(self.df_input, 'Scheme')
        
        elif self.include_non_kp_genomes == "YES" or self.include_non_kp_genomes == "TRAINING-ONLY":    
            if self.check_if_non_kp_data_present(self.df_input, self.df_mlst_metadata) == True:
                pass
            else:
                raise Exception("expected non kp genomes in input dataframe, but none found")
        elif self.include_non_kp_genomes == "NA":
            
            if self.check_if_non_kp_data_present(self.df_input, self.df_mlst_metadata) == False:
                pass
            else:
                raise Exception("Did not expect non kp genomes in input dataframe.")
            
            
        # drop labels
        if drop_labels:
            self.df_input = self.drop_data_labels(self.df_input, self.label_column, self.labels_to_drop)
        
        #label encoding scheme
        if label_encoding_scheme == "hv_vs_lv":
            self.label_encoding_dict = {
                    'NOT_VIRULENT' : 0,
                    'LOW_VIRULENT' : 0,
                    'COLONIZATION' : 0, 
                    'HIGH_VIRULENT' : 1
                }
            self.labels_to_drop = ['COLONIZATION', 'NOT_VIRULENT']
        elif label_encoding_scheme == "vir_vs_nvir":
            self.label_encoding_dict = {
                    'NOT_VIRULENT' : 0,
                    'LOW_VIRULENT' : 1,
                    'COLONIZATION' : 0, 
                    'HIGH_VIRULENT' : 1
                }
            self.labels_to_drop = []
        elif label_encoding_scheme == "custom":
            self.label_encoding_dict = label_encoding_dict
        
        else:
            raise Exception("Invalid label encoding scheme")
        
        
        #reset index
        if self.reset_index:
            if self.df_input.index.name == 'ACCESSION_NUMBER':
                self.df_input.reset_index(inplace = True)
            if self.df_mlst_metadata.index.name == 'ACCESSION_NUMBER':
                self.df_mlst_metadata.reset_index(inplace = True)
        
        ## splitting data
        if split_data == 'from metadata':
            if self.host_type not in ['human', 'all hosts']:
                raise Exception("Invalid host type")       
            self.train_X, self.train_Y, self.test_X, self.test_Y = \
                self.split_data_using_metadata(df_input = self.df_input, \
                                            df_mlst_metadata = self.df_mlst_metadata, \
                                            host_type = self.host_type, \
                                            drop_labels = self.drop_labels, \
                                            labels_to_drop = self.labels_to_drop, \
                                            include_non_kp_genomes = self.include_non_kp_genomes)
        elif split_data == 'regular': 
            self.test_size = test_size
            if self.test_size == 0 or self.test_size == 1:
                raise Exception("test size if defined to be 0 or 1")
            
            self.random_state = 42
                
            df_features, df_output = \
                self.encode_labels_and_drop_unwanted_columns(df_input = self.df_input, \
                                                         label_column = self.label_column, \
                                                         drop_labels = self.drop_labels, \
                                                         labels_to_drop = self.labels_to_drop, \
                                                         reset_index = self.reset_index, drop_columns = self.drop_columns,\
                                                         columns_to_drop = self.columns_to_drop)
            
            self.train_X, self.train_Y, self.test_X, self.test_Y = \
                self.split_data_train_test(df_features, df_output,\
                                            test_size = self.test_size, \
                                            random_state = self.random_state)
        
        else:
            raise Exception("Invalid split data type")
        
        ## oversampling
        if oversampling:
            self.oversample_method = oversampling_method
            if self.oversample_method not in self.allowed_oversampling_methods:
                raise Exception("Invalid oversampling method")
                            
            self.random_weight = random_weight
            
            self.train_X, self.train_Y = self.oversample_data(self.train_X, self.train_Y, self.oversample_method, self.random_weight)

    def ordinal_encoding(self, df_input: pd.DataFrame, label_column: str, drop_labels: bool = False, \
                    labels_to_drop: list[str] = None):
        
        df_copy = copy.deepcopy(df_input)
        df_copy = df_copy[[label_column]]
        if drop_labels:
            filt = df_copy[label_column].isin(labels_to_drop)
            df_copy = df_copy.loc[~filt]
        if self.label_encoding_dict == None:
            raise Exception("No label encoding dict")
        else:
            dict_replace = self.label_encoding_dict
        for each_key in dict_replace:
            if drop_labels:
                if each_key not in labels_to_drop:
                    df_copy.replace(each_key, dict_replace[each_key], inplace = True)
            elif not drop_labels:
                df_copy.replace(each_key, dict_replace[each_key], inplace = True)

        return df_copy
    
    def split_data_using_metadata(self, df_input: pd.DataFrame, df_mlst_metadata : pd.DataFrame,
                                  host_type : str = "human", drop_labels: bool = False, labels_to_drop : List[str] = None, include_non_kp_genomes: str = "NA"):
        
        df_copy = copy.deepcopy(df_input)
        df_mlst_metadata_copy = copy.deepcopy(df_mlst_metadata)
        
        # if index is ACCESSION_NUMBER, then reset 
        if df_copy.index.name == 'ACCESSION_NUMBER':
            df_copy.reset_index(inplace = True)
        
        if df_mlst_metadata_copy.index.name == 'ACCESSION_NUMBER':
            df_mlst_metadata_copy.reset_index(inplace = True)
        
        # determine which columns to keep based on host information
        
        if host_type == "human":
            columns_of_interest = ['TRAINING_SET_HUMAN_HOSTS', 'TESTING_SET_HUMAN_HOSTS']
        elif host_type == "all hosts":
            columns_of_interest = ['TRAINING_SET_ALL_HOSTS', 'TESTING_SET_ALL_HOSTS']
        else:
            print("Passed Host type:", host_type)
            raise Exception("Invalid host type")

        columns_of_interest.append('ACCESSION_NUMBER')
        
        columns_of_interest.append('Scheme')
        
        df_mlst_metadata_copy = df_mlst_metadata_copy[columns_of_interest]
        
        # join the 2 dataframes
        try:
            df_new = pd.merge(df_copy, df_mlst_metadata_copy, how = 'inner', on='ACCESSION_NUMBER')
        except Exception as e:
            print(str(e))
            pdb.post_mortem()
        
        #split into train and test
        filt_training = df_new[columns_of_interest[0]] == 1
        filt_testing = df_new[columns_of_interest[1]] == 1
        
        df_training = df_new.loc[filt_training]
        df_testing = df_new.loc[filt_testing]
        
        
        #if non kp genomes to be kept in training
        if include_non_kp_genomes == "TRAINING-ONLY":
            filt_non_kp_testing = df_testing.Scheme == "kpneumoniae"
            df_testing = df_testing.loc[filt_non_kp_testing]
            #the additional Scheme column does get dropped later on 
            
        
        #checking that no samples match between training and testing
        training_accessions = list(df_training.ACCESSION_NUMBER)
        testing_accessions = list(df_testing.ACCESSION_NUMBER)
        
        if len(set(training_accessions)) == len(training_accessions) \
            and len(set(testing_accessions)) == len(testing_accessions):
            if len(set(training_accessions).intersection(testing_accessions)) == 0:
                pass
            else:
                raise Exception("training and testing sets have common accessions")
        else:
            raise Exception("training or testing sets have duplicate accessions")
        
        
        train_X, train_Y = self.encode_labels_and_drop_unwanted_columns(df_training, label_column = self.label_column,\
                                                                        drop_labels = drop_labels, \
                                                                        labels_to_drop = labels_to_drop, \
                                                                       drop_columns = self.drop_columns, \
                                                                       columns_to_drop = columns_of_interest)
        test_X, test_Y = self.encode_labels_and_drop_unwanted_columns(df_testing, label_column = self.label_column,\
                                                                        drop_labels = drop_labels, \
                                                                        labels_to_drop = labels_to_drop, \
                                                                       drop_columns = self.drop_columns, \
                                                                       columns_to_drop = columns_of_interest)
                                                                        
        print(f"Label distribution in train_Y: {train_Y.value_counts()}")
        print(f"Label distribution in test_Y: {test_Y.value_counts()}")
        
        return train_X, train_Y, test_X, test_Y
    
    def drop_data_labels(self, df_input: pd.DataFrame, label_column : str, labels_to_drop : List[str] = None):
        
        df_copy = copy.deepcopy(df_input)
        filt = df_copy[label_column].isin(labels_to_drop)
        df_copy = df_copy.loc[~filt]
        return df_copy
    
    def encode_labels_and_drop_unwanted_columns(self, df_input : pd.DataFrame, label_column : str, \
                                                drop_labels: bool = False, labels_to_drop: List[str] = None, \
                                                reset_index : bool = True, drop_columns : bool = True,\
                                                columns_to_drop = ['ACCESSION_NUMBER']):
                                                 
        df_copy = copy.deepcopy(df_input)
                                                 
        # reset index and drop unwanted columns
        if reset_index:
            if df_copy.index.name == 'ACCESSION_NUMBER':
                df_copy.reset_index(inplace = True)
            if drop_columns:
                df_copy.drop(columns = columns_to_drop, inplace = True)
        
        #drop labels
        if drop_labels:
            df_copy = self.drop_data_labels(df_copy, label_column, labels_to_drop)
        
        # encode labels                                         
        df_output = self.ordinal_encoding(df_copy, label_column = label_column, drop_labels = drop_labels, \
                                labels_to_drop = labels_to_drop)
        
        df_features = df_copy.drop(columns = [label_column])
        
        return df_features, df_output
                                                 
    def oversample_data(self, train_X, train_Y, oversampling_method = None, random_weight = None):
        
        print(f"Label distribution in train_Y before oversampling: {train_Y.value_counts()}")

        if oversampling_method == 'random':
            from imblearn.over_sampling import RandomOverSampler
            if random_weight == None:
                oversample = RandomOverSampler(sampling_strategy='minority')
            else:
                oversample = RandomOverSampler(sampling_strategy=random_weight)
        elif oversampling_method == 'SMOTE':
            from imblearn.over_sampling import SMOTE
            smote = SMOTE(random_state = 42)
            train_X, train_Y = smote.fit_resample(train_X, train_Y)
        elif oversampling_method == 'ADASYN':
            from imblearn.over_sampling import ADASYN
            adasyn = ADASYN(random_state = 42, n_neighbors = 10)
            train_X, train_Y = adasyn.fit_resample(train_X, train_Y)
        print(f"Label distribution in train_Y after oversampling: {train_Y.value_counts()}")
        
        return train_X, train_Y

    def split_data_train_test(self, df_features, df_output, test_size : float = 0.1, random_state = 42):
        
        split = StratifiedShuffleSplit(n_splits=1, test_size=test_size, random_state=random_state)
        for train_index, test_index in split.split(df_features, df_output):
            train_X, train_Y, test_X, test_Y = df_features.iloc[train_index], df_output.iloc[train_index], \
                                               df_features.iloc[test_index], df_output.iloc[test_index]
        print(f"Label distribution in test_Y: {test_Y.value_counts()}")
            
        return train_X, train_Y, test_X, test_Y
    
    def return_train_test_sets(self):
        return self.train_X, self.train_Y, self.test_X, self.test_Y
