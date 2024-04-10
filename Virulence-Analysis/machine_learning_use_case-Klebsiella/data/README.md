# Data Description

This folder contains input features and relevant metadata used in model construction for our *Klebsiella* machine learning virulence prediction use case. Complete methods are described in [https://github.com/IBM/omxware-getting-started/tree/master/Virulence-Analysis](https://github.com/IBM/omxware-getting-started/tree/master/Virulence-Analysis) and relevant citation information is provided there as well. Briefly, features are based on protein domain architectures that have been vectorized from microbial genomes. The organism's isolation source is used as a proxy to indicate virulence severity risk.

### List of data tables:
```
├── features_and_output
│   ├── df_data_all_hosts.csv #dataframe for all hosts data, rows are genome accessions and columns are virulence domain architecture (DA) features and class label
│   └── df_data_humans.csv #dataframe for only human host data, rows are genome accessions and columns are virulence DA features and class label
├── genome_protein_data
│   └── kp_genome_pivot_neighbor_domain_count_final.csv #file with genome accessions, pivot DA, neighbor DA, type and count. Key count data used in data preparation for training.
├── metadata
│   ├── IBM_virulence_mlst_revised.csv #contains genome multilocus sequence type (MLST) metadata used in error analysis
│   └── genome_complete_metadata.csv #contains genome metadata such as GENUS_NAME, GENUS_TAX_ID, ISOLATION_SOURCE, HOST, etc.
```

### Usage tips:  

- `ACCESSION_NUMBER`, `DOMAIN_ARCHITECTURE_UID_KEY`, and `NEIGHBOR_DOMAIN_ARCHITECTURE_UID_KEY`are  unique identifiers for domain architectures and can be used to map data between tables. 
- `NEIGHBOR_DOMAIN_ARCHITECTURE_UID_KEY` contains co-pivot and discovery domain architectures (DAs) which are further described in the manuscript linked at citation information below.


### Citation:
Please see our GitHub [https://github.com/IBM/omxware-getting-started/tree/master/Virulence-Analysis](https://github.com/IBM/omxware-getting-started/tree/master/Virulence-Analysis) for the most current citation information.
