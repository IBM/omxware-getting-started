# for feature selection
# FeatureDecorrelator code inspired from here: https://stackoverflow.com/questions/66221834/how-to-create-a-custom-python-class-to-be-used-in-pipeline-for-dropping-highly-c

import pandas as pd
import numpy as np
from typing import List
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline
from sklearn.feature_selection import VarianceThreshold

class FeatureDecorrelator(BaseEstimator, TransformerMixin):
    
    def __init__(self, threshold):
        self.threshold = threshold
        self.correlated_columns = None
        self.correlated_features = set()

    def fit(self, X, y=None):
        correlated_features = set()  
        X = pd.DataFrame(X)
        corr_matrix = X.corr()
        for i in range(len(corr_matrix.columns)):
            for j in range(i):
                if abs(corr_matrix.iloc[i, j]) > self.threshold: # we are interested in absolute coeff value
                    colname = corr_matrix.columns[i]  # getting the name of column
                    correlated_features.add(colname)
        self.correlated_features = correlated_features
        return self

    def transform(self, X, y=None):
        return (pd.DataFrame(X)).drop(labels=self.correlated_features, axis=1)
    
    def get_dropped_labels(self):
        if len(self.correlated_features) == 0:
            print("No Correlated Features")
        return self.correlated_features


class FeatureSelection:
    
    """
    1. add_sklearn_pipeline_object_only = True only returns a pipeline object for sklearn.
    2. if you select add_sklearn_pipeline_object_only = True, then the initial dataframes passed for feature set \
    and labels will not be used at all.
    3. pay attention to the order of feature selection, it's important!
    
    """
    
    def __init__(self, df_features, df_labels):
        
        # store values of which feature selection has been applied
        self.feature_selection_applied_dict = {
            'drop_highly_correlated_features': False,
            'drop_low_variance_features': False
        }
        self.pipeline = []
        self.df_features = df_features
        self.df_labels = df_labels
    
    @classmethod 
    def from_combined_features_labels(cls, df: pd.DataFrame, label_column = 'LABEL'):
        #this is an alternative constructor that can be instantiated from a single dataframe which consists of features and labels both
        df_features, df_labels = cls.separate_features_and_labels(df, label_column)
        return cls(df_features, df_labels)
        
    def separate_features_and_labels(self, df: pd.DataFrame, label_column = 'LABEL') -> List[pd.DataFrame]:
        df_label = df[['LABEL']]
        df_features = df.drop(columns = ['LABEL'])
        return df_features, df_label
    
    def run_standard_feature_selection(self, corr_threshold = 0.99, variance_threshold = 0, add_sklearn_pipeline_object_only = False):
        
        number_features_dropped_low_variance = self.drop_low_variance_features(variance_threshold = variance_threshold, add_sklearn_pipeline_object_only = add_sklearn_pipeline_object_only)
        number_features_dropped_high_correlation = self.drop_highly_correlated_features(corr_threshold = corr_threshold, add_sklearn_pipeline_object_only = add_sklearn_pipeline_object_only)
        
        if add_sklearn_pipeline_object_only:
            return self.get_sklearn_pipeline()
        else:
            return [self.get_features_matrix(), number_features_dropped_low_variance + number_features_dropped_high_correlation]
            
    def drop_highly_correlated_features(self, corr_threshold = 0.99, add_sklearn_pipeline_object_only = False):
        
        if add_sklearn_pipeline_object_only:
            self.feature_selection_applied_dict['drop_highly_correlated_features'] = True
            self.pipeline.append(('decorrelator', FeatureDecorrelator(corr_threshold)))
        else:
            print("Dropping highly correlated features")
            feature_obj = FeatureDecorrelator(corr_threshold)
            num_features_before_dropping = self.df_features.shape[1]
            self.df_features = feature_obj.fit_transform(self.df_features)
            num_features_after_dropping = self.df_features.shape[1]
            print("Number of features dropped", num_features_before_dropping - num_features_after_dropping)
            self.set_dropped_labels = feature_obj.get_dropped_labels()
            return num_features_before_dropping - num_features_after_dropping

    
    def drop_low_variance_features(self, variance_threshold = 0, add_sklearn_pipeline_object_only = False):
        
        if add_sklearn_pipeline_object_only:
            self.feature_selection_applied_dict['drop_low_variance_features'] = True
            low_variance_obj = VarianceThreshold(threshold = variance_threshold).set_output(transform = "pandas")
            self.pipeline.append(('low_var', low_variance_obj))
        else:
            print("Dropping features with variance less than: ", variance_threshold)
            low_variance_obj = VarianceThreshold(threshold = variance_threshold).set_output(transform = "pandas")
            num_features_before_dropping = self.df_features.shape[1]
            self.df_features = low_variance_obj.fit_transform(self.df_features)
            num_features_after_dropping = self.df_features.shape[1]
            return("Number of features dropped", num_features_before_dropping - num_features_after_dropping)

    def get_sklearn_pipeline(self):
        return self.pipeline
    
    def get_features_matrix(self):
        return self.df_features
    
    @staticmethod
    def join_features_and_labels(df_features: pd.DataFrame, df_label: pd.DataFrame) -> pd.DataFrame:
        df_merged = df_features.join(df_label)
        return df_merged