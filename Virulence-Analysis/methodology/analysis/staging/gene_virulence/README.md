# GENE_VIRULENCE_STAGING

[back to parent](../README.md)

Run the following to stage the data into Apache Spark:

```
./spark-sql.sh --sql-file sql/staging/gene_virulence.sql
```

OUTPUT

```sql
SET best_similarity = 1

completed in 1.80 seconds

SET distance = 2

completed in 0.02 seconds

SET data_dir = /gpfs/grand/Users/eseabolt/virulence/data

completed in 0.02 seconds

SET outputs_dir = /gpfs/grand/Users/eseabolt/virulence/outputs

completed in 0.01 seconds

SET plots_dir = /gpfs/grand/Users/eseabolt/virulence/plots

completed in 0.01 seconds


DROP TABLE IF EXISTS GENE_VIRULENCE_STAGING

completed in 3.03 seconds


CREATE TABLE GENE_VIRULENCE_STAGING (
  GENE_UID_KEY STRING,
  SHORT_NAME STRING,
  FULL_NAME STRING,
  VIRULENCE_FACTOR STRING,
  GENUS_NAME STRING,
  SPECIES_NAME STRING,
  STRAIN STRING)
    USING csv
    OPTIONS (
      header false,
      path '${data_dir}/gene_virulence.csv')

completed in 0.81 seconds


CACHE TABLE GENE_VIRULENCE_STAGING

completed in 2.62 seconds


SELECT
  COUNT(1) AS NUM_ROWS,
  COUNT(DISTINCT GENE_UID_KEY) AS NUM_DISTINCT_GENES
  FROM
    GENE_VIRULENCE_STAGING

+--------+------------------+
|NUM_ROWS|NUM_DISTINCT_GENES|
+--------+------------------+
|32522   |32506             |
+--------+------------------+

completed in 1.19 seconds


real	0m15.440s
user	0m44.323s
sys	0m5.644s
```
