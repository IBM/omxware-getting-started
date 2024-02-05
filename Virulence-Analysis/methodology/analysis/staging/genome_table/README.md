# GENOME_TABLE_STAGING

[back to parent](../README.md)

Run the following to stage the data into Apache Spark:

```
./spark-sql.sh --sql-file sql/staging/genome_table.sql
```

OUTPUT

```sql
SET best_similarity = 1

completed in 1.81 seconds

SET distance = 2

completed in 0.02 seconds

SET data_dir = /gpfs/grand/Users/eseabolt/virulence/data

completed in 0.01 seconds

SET outputs_dir = /gpfs/grand/Users/eseabolt/virulence/outputs

completed in 0.01 seconds


DROP TABLE IF EXISTS GENOME_TABLE_STAGING

completed in 4.28 seconds


CREATE TABLE GENOME_TABLE_STAGING (
  GENUS_NAME STRING,
  ACCESSION_NUMBER STRING)
    USING csv
    OPTIONS (
      header false,
      path '${data_dir}/genome_table.csv')

completed in 0.46 seconds


CACHE TABLE GENOME_TABLE_STAGING

completed in 2.50 seconds


SELECT
  COUNT(1) AS NUM_ROWS,
  COUNT(DISTINCT GENUS_NAME) AS NUM_DISTINCT_GENERA,
  COUNT(DISTINCT ACCESSION_NUMBER) AS NUM_DISTINCT_GENOMES
  FROM
    GENOME_TABLE_STAGING

+--------+-------------------+--------------------+
|NUM_ROWS|NUM_DISTINCT_GENERA|NUM_DISTINCT_GENOMES|
+--------+-------------------+--------------------+
|206758  |1409               |206758              |
+--------+-------------------+--------------------+

completed in 1.54 seconds


real  0m16.633s
user  0m48.459s
sys  0m6.098s
```
