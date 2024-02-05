# Virulence

This repository holds code and other assets for working with virulent proteins in FGP.

## TOC

* [analysis](analysis) - Contains outputs and documentation from examining virulent proteins in FGP.
* [bart](bart) - Contains files provided by Dr. Bart Weimer from UC Davis describing disease types for a selection of
  Helicobacter genomes.
* [cdc](cdc) - Contains files provided by Dr. Chris Elkins from the CDC describing virulent genes they work with.
* [cdcserver](cdcserver) - Demo application used during the visit to CDC in Jan. 2020.
* [ice](ice) - Information relating mobile elements and virulence.
* [sql](sql) - Contains Spark SQL scripts for analyzing virulence.
* [vfdb](vfdb) - Contains python code for parsing the protein and gene fasta files from VFDB. The VFDB is
  located [here]( http://www.mgc.ac.cn/VFs/)
    * Total number of proteins in VFDB: **28,583**
    * Total number of VFDB proteins in FGP: **22,853**
    * Total number of VFDB proteins in FGP with IPR: **21,125**

# Environment

* Machine - fgp-agent-01.sl.cloud9.ibm.com
* Directory - /gpfs/grand/Users/eseabolt/virulence

## Python

The following environment was used for Python

* Python Version - 3.9.10

A python virtual environment was created using `python3.9 -m venv venv`

## Spark

The following environment was used for Spark processes

* Spark Version - 3.2.1 (spark-3.2.1-bin-hadoop3.2)
* Logging can be controlled by editing the log4j.properies file in conf
* PySpark documentation - https://spark.apache.org/docs/3.2.1/api/python/index.html
* Jobs submitted to Spark can be monitored at fgp-agent-01.sl.cloud9.ibm.com:4040

Source the file `spark-env.sh` to setup Python and Spark environments

## DB2 Environment

* Machine - omxdb01-prod.sl.cloud9.ibm.com

## Thriftserver

In order to connect to the Spark database from a JDBC connection or DBeaver, the
script [thriftserver.sh](thriftserver.sh) needs to be run on fgp-agent-01.sl.cloud9.ibm.com. The server can be stopped
by calling stop-thriftserver.sh. The script [spark-env.sh](spark-env.sh) must be sourced before running these.
