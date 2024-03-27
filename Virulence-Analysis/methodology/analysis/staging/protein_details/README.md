# PROTEIN_DETAILS_STAGING

[back to parent](../README.md)

Run the following to stage the data into Apache Spark:

```
./spark-sql.sh --sql-file sql/staging/protein_details.sql
```

OUTPUT

```sql
SET best_similarity = 1

completed in 1.83 seconds

SET distance = 2

completed in 0.02 seconds

SET data_dir = /gpfs/grand/Users/eseabolt/virulence/data

completed in 0.01 seconds

SET outputs_dir = /gpfs/grand/Users/eseabolt/virulence/outputs

completed in 0.01 seconds


DROP TABLE IF EXISTS PROTEIN_DETAILS_STAGING

completed in 4.23 seconds


CREATE TABLE PROTEIN_DETAILS_STAGING (
  PROTEIN_UID_KEY STRING,
  PROTEIN_FULLNAME STRING)
    USING csv
    OPTIONS (
      header false,
      path '${data_dir}/protein_details.csv')

completed in 0.48 seconds


CACHE TABLE PROTEIN_DETAILS_STAGING

completed in 11.60 seconds


SELECT
  COUNT(1) AS NUM_ROWS,
  COUNT(DISTINCT PROTEIN_UID_KEY) AS NUM_DISTINCT_PROTEINS,
  COUNT(DISTINCT PROTEIN_FULLNAME) AS NUM_DISTINCT_NAMES
  FROM
    PROTEIN_DETAILS_STAGING

+--------+---------------------+------------------+
|NUM_ROWS|NUM_DISTINCT_PROTEINS|NUM_DISTINCT_NAMES|
+--------+---------------------+------------------+
|55059587|54104627             |21484             |
+--------+---------------------+------------------+

completed in 87.83 seconds


real  1m53.971s
user  11m58.692s
sys  4m23.989s
```
