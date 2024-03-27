#! /usr/bin/env bash

set -o noglob

time spark-submit \
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
  --driver-memory 128G \
  --deploy-mode client \
  --files ${PWD}/hive-site.xml \
  "$@"

set +o noglob
