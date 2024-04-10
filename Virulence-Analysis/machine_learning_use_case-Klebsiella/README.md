## Description:
This folder includes machine learning methods and downstream analysis for a clinical use case with *Klebsiella* to identify and predict features associated with virulence. The full method is detailed in the manuscript indicated in the [Citation information](../README.md).

## Usage Information:
- Most of the code is written in sklearn, and GPU is not required to run. 
- Code was run on a machine with 128 CPU cores, 256GB RAM with Ubuntu 20.04. However, this should run effortlessly on smaller machines as well. 
- In this subfolder `virulence++` is used as a tag for simplicity and is indicated in the manuscript as "discovery inclusion".
- To run on your system, please update all paths indicated in `common.sh` including updating `NUM_JOBS` based on the number of cores available.
- Please preserve the file directory structure included here.
- To better understand the usage of `NUM_JOBS`, please see these docs [https://scikit-learn.org/stable/glossary.html#term-n_jobs](https://scikit-learn.org/stable/glossary.html#term-n_jobs), [https://xgboost.readthedocs.io/en/latest/python/python_api.html](https://xgboost.readthedocs.io/en/latest/python/python_api.html).


### Creating a conda environment:
1. Install conda [LINK](https://conda.io/projects/conda/en/latest/user-guide/install/index.html)
2. Create conda environment:
`conda env create --name <envname> --file=environment.yml`
3. Activate conda environment:
`conda activate <envname>`

### Setting up environment to run code:
1. All dependencies are included in `environment.yml`. Before running the code included in this subfolder, create a conda environment using the yml file.
2. Update parameters and paths in `common.sh`.
3. Source this config using `source common.sh`. Note: If config changes, it will need to be sourced again.


### Source description:

```
src
├── data_prep
│   ├── __init__.py
│   ├── baseline_data_prep.py #file with data prep code for baseline models
│   ├── data_prep.py #file with data prep code from raw data
│   └── ml_data_prep.py #file with data prep code for virulence++
├── exploratory_data_analysis
│   ├── __init__.py
│   └── eda.py #util file for exploratory data analysis, requires eps input for DBSCAN
├── model
│   ├── __init__.py
│   ├── baseline_models_training_testing.py #code for training, testing baseline models
│   ├── error_analysis.py #code for doing performance analysis per ST. Requires output file from consolidate_accuracy_table.py
│   ├── model_utils #utils for ml modeling
│   │   ├── __init__.py 
│   │   ├── feature_selection.py
│   │   ├── machine_learning.py #core ML code, used by both baseline models and virulence++ models
│   │   └── top_features.py
│   ├── virulence++_model_testing.py 
│   └── virulence++_model_training.py
└── results
    └── consolidate_accuracy_table.py #combines results from baseline model testing and virulence++ model testing. Requires baseline and virulence++ testing output. Output file generated has a column, TAG_ERROR_ANALYSIS for used in downstream error analysis. By default, all values are marked as N and the user can modify this value to Y to include in error analysis. Output file included complete_ml_results.csv already has some models indicated for inclusion based on manuscript analysis.
```

## Relevant data files:
- All input data (features), models, and results files have been uploaded to PrecisionFDA (pFDA). Please request access, and these files can be downloaded from here [LINK]().  


## Citation: 
Please see citation information included [here](../README.md)
