#!/usr/bin/env bash

. venv/bin/activate

export SPARK_HOME=${PWD}/spark
export JAVA_HOME=$(update-java-alternatives -l | tr -s ' ' | cut -d " " -f 3 | grep 1.8)
export PATH=${SPARK_HOME}/bin:${SPARK_HOME}/sbin:${JAVA_HOME}/bin:${PATH}
export SPARK_MASTER=local[*]
export SPARK_LOCAL_DIRS=${PWD}/tmp
export PYSPARK_PYTHON=$(which python)
export HADOOP_CONF_DIR=${PWD}
