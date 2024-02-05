#! /usr/bin/env bash

spark-sql \
  --master local[*] \
  --conf spark.master.rest.enabled=true \
  --conf spark.sql.warehouse.dir=${PWD}/spark-warehouse \
  --conf spark.local.dir=${PWD}/tmp \
  --conf spark.driver.maxResultSize=40g \
  --conf spark.network.timeout=10000001 \
  --conf spark.executor.heartbeatInterval=10000000 \
  --conf spark.hadoop.mapreduce.fileoutputcommitter.algorithm.version=2 \
  --conf spark.hadoop.mapreduce.fileoutputcommitter.cleanup-failures.ignored=true \
  --conf spark.hadoop.parquet.enable.summary-metadata=false \
  --conf spark.sql.parquet.mergeSchema=false \
  --conf spark.sql.parquet.filterPushdown=true \
  --conf spark.sql.hive.metastorePartitionPruning=true \
  --conf spark.jars=${PWD}/lib/stocator-1.1.5-jar-with-dependencies.jar \
  --driver-memory 128G \
  --files ${PWD}/hive-site.xml \
  --files ${PWD}/core-site.xml
