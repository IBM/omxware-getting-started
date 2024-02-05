# IPR_STAGING

[back to parent](../README.md)

Run the following to stage the data into Apache Spark:

```
./spark-sql.sh --sql-file sql/staging/ipr.sql
```

OUTPUT

```sql
SET best_similarity = 1

completed in 1.82 seconds

SET distance = 2

completed in 0.02 seconds

SET data_dir = /gpfs/grand/Users/eseabolt/virulence/data

completed in 0.02 seconds

SET outputs_dir = /gpfs/grand/Users/eseabolt/virulence/outputs

completed in 0.01 seconds


DROP TABLE IF EXISTS IPR_STAGING

completed in 4.23 seconds


CREATE TABLE IPR_STAGING (
  IPR_ACCESSION STRING,
  NAME STRING,
  DESCRIPTION STRING,
  TYPE STRING)
    USING csv
    OPTIONS (
      header false,
      path '${data_dir}/ipr.csv')

completed in 0.52 seconds


CACHE TABLE IPR_STAGING

completed in 2.23 seconds


SELECT
  COUNT(1) AS NUM_ROWS,
  COUNT(DISTINCT IPR_ACCESSION) AS NUM_DISTINCT_IPRS,
  COUNT(DISTINCT TYPE) AS NUM_DISTINCT_TYPES
  FROM
    IPR_STAGING

+--------+-----------------+------------------+
|NUM_ROWS|NUM_DISTINCT_IPRS|NUM_DISTINCT_TYPES|
+--------+-----------------+------------------+
|37110   |37110            |8                 |
+--------+-----------------+------------------+

completed in 1.31 seconds


real	0m15.193s
user	0m47.000s
sys	0m6.289s
```
