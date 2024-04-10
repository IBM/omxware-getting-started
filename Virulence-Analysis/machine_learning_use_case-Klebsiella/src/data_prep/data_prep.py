#Code to read and clean data

import pandas as pd
from os.path import join
from copy import deepcopy

class Data:
    
    def __init__(self, data_path, all_hosts_file, human_hosts_file, genome_metadata_file, mlst_metadata_file):
        
        self.df_data_all_hosts = pd.read_csv(join(data_path, all_hosts_file))
        self.df_data_human_hosts = pd.read_csv(join(data_path, human_hosts_file))
        self.df_metadata = pd.read_csv(join(data_path, genome_metadata_file))
        self.df_mlst_metadata = pd.read_csv(join(data_path, mlst_metadata_file), header = 1)
        
    def drop_non_kp_genomes_from_dataframes(self, df_data, df_metadata):
        """
        expect dataframe from which to drop non kp genomes, and a df of metadata with info regarding which ones are non kp genomes
        """
        
        df_data_copy = deepcopy(df_data)
        df_metadata_copy = deepcopy(df_metadata[['ACCESSION_NUMBER', 'Scheme']])
        filt = df_metadata_copy.Scheme == "kpneumoniae"
        df_metadata_copy = df_metadata_copy.loc[filt]
        df_new = pd.merge(df_data_copy, df_metadata_copy, how = 'inner', on = 'ACCESSION_NUMBER')
        return df_new
        
    def drop_non_kp_genomes(self, host_type = None):
        """
        host_type: "human host" or "all hosts"
        based on host type, it loads the apt data and metadata and then calls drop_non_kp_genomes_from_dataframes
        """
        if host_type == 'human':
            self.df_data_human_host_dropped_non_kp = self.drop_non_kp_genomes_from_dataframes(self.df_data_human_hosts, self.df_mlst_metadata)
            return self.df_data_human_host_dropped_non_kp
        elif host_type == 'all hosts':
            self.df_data_all_hosts_dropped_non_kp = self.drop_non_kp_genomes_from_dataframes(self.df_data_all_hosts, self.df_mlst_metadata)
            return self.df_data_all_hosts_dropped_non_kp
        else:
            raise Exception('undefined host type')

            
    def drop_column(self, df, column_name):
        """
        drop column using a column name
        column name can be a single column only
        """
        df = df.drop(columns = [column_name])
        return df
    
    def check_if_non_kp_data_present(self, df, df_metadata):
        """
        check if df has non kp data
        """
        new_metadata = df_metadata[['ACCESSION_NUMBER', 'Scheme']]
        filt = new_metadata.Scheme != "kpneumoniae"
        new_metadata = new_metadata.loc[filt]
        df_new = pd.merge(df, new_metadata, on='ACCESSION_NUMBER', how = 'inner')
        if df_new.shape[0] > 0:
            return True
        else:
            return False
        
            
    
        
            
            
        
        
        
    