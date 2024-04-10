# Data Description

This folder contains classification results files from the virulence prediction ML results described in [https://github.com/IBM/omxware-getting-started/tree/master/Virulence-Analysis](https://github.com/IBM/omxware-getting-started/tree/master/Virulence-Analysis) and relevant citation information is provided there as well. Briefly, features were based on protein domain architectures that have been vectorized from microbial genomes. The organism's isolation source is used as a proxy to indicate virulence severity risk. The resulting accuracy and error analysis across all 48 models (virulence++ and baseline) are included here. Additional details are present in the cited manuscript. Note: for manuscript continuity, virulence++ is used in this repository as a short hand for the discovery inclusion feature set. 


### List of files:
```
├── baseline_tuned_model_results.csv
├── virulence++_model_results.csv
├── complete_ml_results.csv #combines baseline_tuned file with virulence++_model_results file. Combination done using `src/results/consolidate_accuracy_table/.py`
└── error_analysis.csv #error analysis for each model which used multi-locus sequence type to construct different testing sets. Code: `src/model/error_analysis.py`
```

### Column descriptions:

- `HOST_TYPE`: all hosts or only human hosts
- `MODEL_TYPE`: can either be `hv_vs_lv`(high vs low virulence) or `vir_vs_nvir`(virulent vs not virulent). Both are binary models.
- `INCLUDE_NON_KP_GENOMES_IN_TRAINING`: see comments in-line in `src/model/model_utils/machine_learning.py` for additional description
- `INCLUDE_NON_KP_GENOMES_IN_TESTING`: see comments in-line in `src/model/model_utils/machine_learning.py` for additional description
- `OVERSAMPLING`
- `OVERSAMPLING_METHOD`
- `ALGO`: can be `SVM` or `XGBoost` or `Baseline_tuned`. `Baseline_tuned` is also XGBoost but uses baseline method features.
- `F-1`
- `AUC`: area under curve
- `CLASSIFICATION SCORE`: mean accuracy on the given test data and labels
- `CLASS0 PRECISION` (see note below re: class distinction)
- `CLASS0 RECALL` (see note below re: class distinction)
- `CLASS1 PRECISION` (see note below re: class distinction)
- `CLASS1 RECALL` (see note below re: class distinction)
- `PATH`: ml model path. This needs to be appended to `MODEL_PATH` in `common.sh` to get the final path.
- `TAG_ERROR_ANALYSIS`: models tagged for error analysis i.e. to be tested for each sequence type. Manually selected usually on the basis of which is the best performing model in a set (identified based on `HOST_TYPE`, `MODEL_TYPE`, `OVERSAMPLING`, `INCLUDE_NON_KP_GENOMES_IN_TRANINING`, `INCLUDE_NON_KP_GENOMES_IN_TESTING`).
- `ST`: multi-locus sequence type
- `#SAMPLES_TEST_SET`: number of samples in test set

### Usage tips:
- For `CLASS1` versus `CLASS0`: `CLASS1` designation is always the more virulent class e.g., in `hv_vs_lv`, `hv` would be `CLASS1` likewise in `vir_vs_nvir`, `vir` is `CLASS1`. This makes `lv` and `nvir` belong to `CLASS0` in those comparisons, respectively.
- For code to load/save models, please see `src/model/model_utils/machine_learning.py`. Models have been deposited in PrecisionFDA. Please request access and download from [there](TODO). 
- For documentation on the data used to build feature sets, please see: [https://github.com/IBM/omxware-getting-started/tree/master/Virulence-Analysis](https://github.com/IBM/omxware-getting-started/tree/master/Virulence-Analysis).


### Citation:
Please see citation information included [here](../README.md).