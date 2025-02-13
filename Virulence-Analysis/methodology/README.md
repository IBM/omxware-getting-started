# Virulence

This repository holds code and other assets for working with virulent proteins in FGP.

## TOC

* [analysis](analysis) - Contains outputs and documentation from examining virulent proteins in FGP.
* [sql](sql) - Contains Spark SQL scripts for analyzing virulence.
* [vfdb](vfdb) - Contains python code for parsing the protein and gene fasta files from VFDB. The VFDB is
  located [here]( http://www.mgc.ac.cn/VFs/)
    * Total number of proteins in VFDB: **28,583**
    * Total number of VFDB proteins in FGP: **22,853**
    * Total number of VFDB proteins in FGP with IPR: **21,125**
 
## Environment

We used a 56 core virtual machine leveraging Intel(R) Xeon(R) Platinum 8260 CPU @ 2.40GHz, ~250GB RAM, and 2TB SAN drive for storage. We use git LFS for large file support. To use install git LFS and then issue `git lfs install`

## Python

The following environment was used for Python

* Python Version - 3.9.10

A python virtual environment was created using `python3.9 -m venv venv`

## Spark

The following environment was used for Spark processes

* Spark Version - 3.3.1 (spark-3.3.1-bin-hadoop3)
* Logging can be controlled by editing the log4j.properies file in conf
* PySpark documentation - https://spark.apache.org/docs/3.3.1/api/python/index.html

Source the file `spark-env.sh` to setup Python and Spark environments

to install packages run the following

```
pip install -r requirements.txt
```
