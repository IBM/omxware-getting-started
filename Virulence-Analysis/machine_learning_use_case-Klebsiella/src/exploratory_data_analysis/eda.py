## source file for exploratory data analysis

import pandas as pd
import numpy as np
import copy
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.metrics import silhouette_samples
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from sklearn.neighbors import NearestNeighbors
from sklearn.cluster import DBSCAN

class EDA:
    
    def __init__(self, df : pd.DataFrame, change_index_to_accession : bool = True):
        """
        converts the passed dataframe to a class df
        also sets index to ACCESSION_NUMBER if that's not already the case
        """
        
        self.df = df
        
        if change_index_to_accession:
            if self.df.index.name != "ACCESSION_NUMBER":
                self.df.set_index("ACCESSION_NUMBER", inplace = True) #ACCESSION_NUMBER must be a column
        
        self.cluster_size_range = (2,7) #for kmeans
    def run_complete_analysis(self, run_clustering = True):
        
        print("LABELS FOUND:", list(self.df.LABEL.value_counts().index))
        print("-------------------------------")
        print("CHECK VALUE COUNTS")
        print(self.df.LABEL.value_counts())
        
        print("-------------------------------")
        print("CHECKING FOR DROPPED FEATURES IN EACH LABEL\n")
        # dropped features are features that take value 0
        self.dictionary_dropped_features = {}
        for each_label in list(self.df.LABEL.value_counts().index):
            self.dictionary_dropped_features[each_label] = \
                    self.check_dropped_features(df_input = self.df, \
                                               subset_by_label = True, \
                                               label_values_to_subset=[each_label],\
                                               label_column = 'LABEL', \
                                               drop_columns = False)

        print("-------------------------------")
        print("CHECKING FOR UNIQUELY PRESENT FEATURES") #checks if any features unique to only one label
        self.dictionary_unique_features = {}
        for each_label in list(self.df.LABEL.value_counts().index):
            self.check_unique_features(each_label)
        
        print("-------------------------------")
        if run_clustering:
            print("RUNNING KMEANS CLUSTERING \n")
            print("checking for cluster sizes from:", self.cluster_size_range, end = "\n")
            print("to try a different range, change self.cluster_size_range in src/exploratory_data_analysis/eda.py")
            
            dict_scores = self.run_kmeans(df_input = self.df, label_column = 'LABEL', cluster_size_range = self.cluster_size_range)
            
            print("PLOTTING SILHOUTTE SCORES VS #CLUSTERS")
            plt.xlabel("#CLUSTERS")
            plt.ylabel("SILHOUTTE SCORE")
            plt.plot(dict_scores.keys(), dict_scores.values())
            plt.show()
            
            print("-------------------------------")
            print("RUNNING DBSCAN")
            self.db_scan(self.df)

    def check_unique_features(self, label_of_interest: [str, int]) -> None:
        """
        this works by identifying the common features that are dropped(i.e. take value 0)
        in all labels other than the labels of interest. 
        This list of common dropped features is stored in intersection_features.
        
        The function then loops through each feature in intersection_features to identify
        if that feature is present in the list of features dropped in labels of interest. 
        If feature is not present then that feature is unique to label(s) of interest and
        added to the dictionary_unique_features. 
        """
        intersection_features = None

        for each_label in self.dictionary_dropped_features:
            if each_label == label_of_interest:
                continue
            else:
                if intersection_features is None:
                    intersection_features = self.dictionary_dropped_features[each_label]
                else:
                    intersection_features = list(set(intersection_features) & set(self.dictionary_dropped_features[each_label]))
        
        for each_element in intersection_features:
            if each_element in self.dictionary_dropped_features[label_of_interest]:
                continue
            else:
                if label_of_interest in self.dictionary_unique_features:
                    self.dictionary_unique_features[label_of_interest].append(each_element)
                else:
                    self.dictionary_unique_features[label_of_interest] = [each_element]
        print("Number of Unique Features For {} are {}".format(label_of_interest, len(self.dictionary_unique_features[label_of_interest])))
                
        
    
    def check_dropped_features(self, df_input: pd.DataFrame, \
                           label_column:str, drop_columns: bool, columns_to_drop:list[str] = None, \
                           subset_by_label:bool = False, label_values_to_subset:list[str] = None,) -> list:
        """
        Checks for dropped features for each LABEL i.e. features that always take the value 0 when data is subset by each LABEL
        
        sample args: df_input = self.df, subset_by_label = True, label_values_to_subset=[each_label],\
                                                               label_column = 'LABEL', drop_columns = False
        """
        df_copy = copy.deepcopy(df_input)
        if drop_columns:        
                df_copy.drop(columns = columns_to_drop, inplace = True)
        
        if subset_by_label:
            filt = df_copy[label_column].isin(label_values_to_subset)
            df_copy = df_copy.loc[filt]
        
        df_copy.drop(columns = [label_column], inplace = True)
        features_with_max_value_0 = df_copy.max() == 0
        dropped_features = features_with_max_value_0[features_with_max_value_0 == True]
        
        print("Total Features Dropped in {}: {}".format(label_values_to_subset, dropped_features.shape[0]))
        return list(dropped_features.index)

    
    def run_kmeans(self, df_input : pd.DataFrame, label_column: str, cluster_size_range: tuple[int, int] = (2,5), \
                   drop_columns: bool = False, columns_to_drop: list[str] = None, drop_labels: bool = False, \
                   labels_to_drop: list[str] = None):
        """
        runs kmeans
        sample args: df_input = self.df, label_column = 'LABEL', cluster_size_range = (2,7)
        returns a dictionary of silhoutte scores for each cluster size. This can be used to plot them against cluster size.
        """
        scaler = StandardScaler()
        df_copy = df_input.copy()

        if drop_columns:
            df_copy = df_copy.drop(columns = columns_to_drop)

        if drop_labels:
            filt = df_copy[label_column].isin(labels_to_drop)
            df_copy = df_copy.loc[~filt]

        df_features_only = df_copy.drop(columns = label_column)

        df_scaled = scaler.fit_transform(df_features_only)

        dict_scores = {}
        dropped_ipr_code = {}
        for k in range(cluster_size_range[0], cluster_size_range[1]):

            kmeans = KMeans(n_clusters=k, random_state=42)
            cluster_labels = kmeans.fit_predict(df_scaled)
            sil_score = silhouette_score(df_scaled, kmeans.labels_)

            df_copy['cluster_labels'] = kmeans.labels_

            for each_label in range(k):

                print("LABEL {}".format(each_label))
                df_temp = df_copy[df_copy['cluster_labels'] == each_label]
                print(df_temp[label_column].value_counts())

            print(len(cluster_labels))
            print("For {} clusters, silhoutte score is {}".format(k, sil_score))
            dict_scores[k] = sil_score
            self.silhoutte_diagram(df_scaled, cluster_labels, n_clusters=k)
        return dict_scores
    
    def silhoutte_diagram(self, X, cluster_labels, n_clusters):
        
        """
        draws silhoutte diagram, called inside kmeans
        """
        
        silhouette_avg = silhouette_score(X, cluster_labels)

        print(
            "For n_clusters =",
            n_clusters,
            "The average silhouette_score is :",
            silhouette_avg,
        )

        # Compute the silhouette scores for each sample
        sample_silhouette_values = silhouette_samples(X, cluster_labels)
        fig, (ax1, ax2) = plt.subplots(1, 2)
        fig.set_size_inches(18, 7)

        # The 1st subplot is the silhouette plot
        # The silhouette coefficient can range from -1, 1
        ax1.set_xlim([-1, 1])
        # The (n_clusters+1)*10 is for inserting blank space between silhouette
        # plots of individual clusters, to demarcate them clearly.
        ax1.set_ylim([0, len(X) + (n_clusters + 1) * 10])
        y_lower = 10
        for i in range(n_clusters):
            # Aggregate the silhouette scores for samples belonging to
            # cluster i, and sort them
            ith_cluster_silhouette_values = sample_silhouette_values[cluster_labels == i]

            ith_cluster_silhouette_values.sort()

            size_cluster_i = ith_cluster_silhouette_values.shape[0]
            y_upper = y_lower + size_cluster_i

            color = cm.nipy_spectral(float(i) / n_clusters)
            ax1.fill_betweenx(
                np.arange(y_lower, y_upper),
                0,
                ith_cluster_silhouette_values,
                facecolor=color,
                edgecolor=color,
                alpha=0.7,
            )

            # Label the silhouette plots with their cluster numbers at the middle
            ax1.text(-0.05, y_lower + 0.5 * size_cluster_i, str(i))

            # Compute the new y_lower for next plot
            y_lower = y_upper + 10  # 10 for the 0 samples

        ax1.set_title("The silhouette plot for the various clusters.")
        ax1.set_xlabel("The silhouette coefficient values")
        ax1.set_ylabel("Cluster label")

        # The vertical line for average silhouette score of all the values
        ax1.axvline(x=silhouette_avg, color="red", linestyle="--")

        ax1.set_yticks([])  # Clear the yaxis labels / ticks
        ax1.set_xticks([-0.1, 0, 0.2, 0.4, 0.6, 0.8, 1])

        plt.show()
    
    def db_scan(self, df):
        
        """
        runs db scan
        
        requirements: 
        1. it plots eps for dbscan, by looking at this curve determine what eps should be
        2. min_samples can be set to 10
        """
        
        df_copy = copy.deepcopy(df)
        
        def calculate_eps_for_dbscan(df_input: pd.DataFrame, label_column: str):

            neigh = NearestNeighbors(n_neighbors=2)
            nbrs = neigh.fit(df_input.drop(columns = [label_column]))
            distances, indices = nbrs.kneighbors(df_input.drop(columns = [label_column]))
            distances = np.sort(distances, axis=0)
            distances = distances[:,1]
            plt.plot(distances)
            plt.show()
        

        calculate_eps_for_dbscan(df_input = df_copy, label_column = 'LABEL')
        
        eps_input = input("on the basis of above plot, please pass the eps") #60
        min_samples = input("pass the minimum number of sample") #10
        
        dbscan = DBSCAN(eps = float(eps_input), min_samples = int(min_samples))
        dbscan.fit_predict(df_copy.drop(columns = ['LABEL']))
        
        preds = dbscan.labels_
        print("Predictions from DBSCAN: ", set(preds))
        
        dict_preds = dict()
        for x in preds:
            if x in dict_preds:
                dict_preds[x] += 1
            else:
                dict_preds[x] = 1
        for i in sorted(dict_preds.keys()):
            print("{}:{}".format(i,dict_preds[i]))
            
        print_samples = input("Print samples with DBSCAN labels?Yes/No")
        if print_samples == 'Yes':
            df_copy2 = copy.deepcopy(df_copy)
            df_copy2['dbscan_labels'] = preds
            print(df_copy2)
        