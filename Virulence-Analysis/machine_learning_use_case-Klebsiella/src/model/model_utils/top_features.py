import pandas as pd
from joblib import load
from typing import List
import xgboost
import numpy as np
import os
import sys


DATA_PATH = os.getenv('DATA_PATH')
MODEL_PATH = os.getenv('MODEL_PATH')
RESULTS_PATH = os.getenv('RESULTS_PATH')
DRY_RUN = os.getenv('DRY_RUN')
NUM_JOBS = os.getenv('NUM_JOBS')
sys.path.append(os.getenv('SOURCE_PATH'))

PROTEIN_DETAILS_FILE = os.getenv('PROTEIN_DETAILS_FILE')
PROTEIN_DOMAIN_ARCHITECTURE_FILE = os.getenv('PROTEIN_DOMAIN_ARCHITECTURE_FILE')
FEATURE_INDEX_TO_DA = os.getenv('FEATURE_INDEX_TO_DA')
PIVOT_NEIGHBOR_DA = os.getenv('PIVOT_NEIGHBOR_DA')

class TopFeatures:
    
    def __init__(self, model_file: str):
        self.model_file = model_file
        self.__load_model()
        self.__load_required_files()
        self.__generate_required_dataframes()
    
    def __load_required_files(self) -> None:
        
        self.df_protein_details = pd.read_csv(PROTEIN_DETAILS_FILE)
        self.df_protein_domain_architecture = pd.read_csv(PROTEIN_DOMAIN_ARCHITECTURE_FILE)
        self.df_feature_index_to_DA = pd.read_csv(FEATURE_INDEX_TO_DA)
        self.df_pivot_neighbor_DA = pd.read_csv(PIVOT_NEIGHBOR_DA)

    def __generate_required_dataframes(self) -> None:
        self.protein_uid_DA_protein_name = pd.merge(self.df_protein_details, self.df_protein_domain_architecture, how = 'inner', \
                                                    on = 'PROTEIN_UID_KEY')
        self.pivot_proteins = self.df_pivot_neighbor_DA['PIVOT_DOMAIN_ARCHITECTURE_UID_KEY'].unique()
        self.neighbor_proteins = self.df_pivot_neighbor_DA['NEIGHBOR_DOMAIN_ARCHITECTURE_UID_KEY'].unique()

    def __load_model(self) -> None:
        self.model_pipeline = load(self.model_file)
        self.ml_model = self.model_pipeline[2]

    def _calculate_top_model_features(self, n: int = 10) -> None:
        # self.top_features = np.array(self.ml_model.get_booster().get_score(importance_type = 'gain'))
        self.df_top_features = pd.DataFrame.from_dict(self.ml_model.get_booster().get_score(importance_type = 'gain'), orient='index', columns=['FEATURE_IMPORTANCE'])
        self.df_top_features = self.df_top_features.reset_index()
        self.df_top_features['index'] = self.df_top_features['index'].astype('int')
        self.df_top_n_features = self.df_top_features.sort_values(by=['FEATURE_IMPORTANCE'], ascending=False)[:n]
    
    def _get_DA_from_top_feature_index(self) -> None:
        
        self.df_top_n_features_DA = pd.merge(self.df_top_n_features, self.df_feature_index_to_DA, how = 'inner', \
                                             left_on = 'index', right_on='INDEX')
        self.list_top_n_features_DA = self.df_top_n_features_DA['LABEL'].unique()
    
    def _check_list_DA_pivot_only(self, temp_list: List[str]) -> List[bool]:
        
        results = map(self._check_if_DA_pivot_only, temp_list)
        return results
    
    def _check_list_DA_neighbor_only(self, temp_list: List[str]) -> List[bool]:
        
        results = map(self._check_if_DA_neighbor_only, temp_list)
        return results

    def _check_if_DA_pivot_only(self, da: str) -> bool:

        if da in self.pivot_proteins and da not in self.neighbor_proteins:
            return True
        else:
            return False
    
    def _check_if_DA_neighbor_only(self, da: str) -> bool:

        if da not in self.pivot_proteins and da in self.neighbor_proteins:
            return True
        else:
            return False
        
    def _get_protein_uid_name_from_DA(self, da: str | List[str]) -> pd.DataFrame:
        
        if isinstance(da, str):
            filt = self.protein_uid_DA_protein_name['DOMAIN_ARCHITECTURE_UID_KEY'] == da
        elif isinstance(da, list):
            filt = self.protein_uid_DA_protein_name['DOMAIN_ARCHITECTURE_UID_KEY'].isin(da)
        elif isinstance(da, pd.DataFrame):
            df = pd.merge(self.protein_uid_DA_protein_name, da, on='DOMAIN_ARCHITECTURE_UID_KEY', how = 'inner')
            return df
        else:
            raise TypeError("Invalid type of da", type(da))

        return self.protein_uid_DA_protein_name.loc[filt]
    

    


        



