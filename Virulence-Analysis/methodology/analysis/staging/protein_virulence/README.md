# PROTEIN_VIRULENCE_STAGING

[back to parent](../README.md)

Run the following to stage the data into Apache Spark:

```
./spark-sql.sh --sql-file sql/staging/protein_virulence.sql
```

OUTPUT

```sql
SET best_similarity = 1

completed in 1.79 seconds

SET distance = 2

completed in 0.02 seconds

SET data_dir = /gpfs/grand/Users/eseabolt/virulence/data

completed in 0.01 seconds

SET outputs_dir = /gpfs/grand/Users/eseabolt/virulence/outputs

completed in 0.01 seconds


DROP TABLE IF EXISTS PROTEIN_VIRULENCE_STAGING

completed in 3.89 seconds


CREATE TABLE PROTEIN_VIRULENCE_STAGING (
  PROTEIN_UID_KEY STRING,
  SHORT_NAME STRING,
  FULL_NAME STRING,
  VIRULENCE_FACTOR STRING,
  GENUS_NAME STRING,
  SPECIES_NAME STRING,
  STRAIN STRING)
    USING csv
    OPTIONS (
      header false,
      path '${data_dir}/protein_virulence.csv')

completed in 0.47 seconds


CACHE TABLE PROTEIN_VIRULENCE_STAGING

completed in 2.28 seconds


SELECT
  COUNT(1) AS NUM_ROWS,
  COUNT(DISTINCT PROTEIN_UID_KEY) AS NUM_DISTINCT_PROTEINS
  FROM
    PROTEIN_VIRULENCE_STAGING

+--------+---------------------+
|NUM_ROWS|NUM_DISTINCT_PROTEINS|
+--------+---------------------+
|28616   |28583                |
+--------+---------------------+

completed in 1.07 seconds


real	0m15.553s
user	0m46.548s
sys	0m5.516s
```
