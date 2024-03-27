# IPR_PROTEIN_STAGING

[back to parent](../README.md)

Run the following to stage the data into Apache Spark:

```
./spark-sql.sh --sql-file sql/staging/ipr_protein.sql
```

OUTPUT

```sql
SET best_similarity = 1

completed in 1.84 seconds

SET distance = 2

completed in 0.02 seconds

SET data_dir = /gpfs/grand/Users/eseabolt/virulence/data

completed in 0.02 seconds

SET outputs_dir = /gpfs/grand/Users/eseabolt/virulence/outputs

completed in 0.01 seconds


DROP TABLE IF EXISTS IPR_PROTEIN_STAGING

completed in 3.20 seconds


CREATE TABLE IPR_PROTEIN_STAGING (
  IPR_ACCESSION STRING,
  PROTEIN_UID_KEY STRING)
    USING csv
    OPTIONS (
      header false,
      path '${data_dir}/ipr_protein.csv')

completed in 0.73 seconds


CACHE TABLE IPR_PROTEIN_STAGING

completed in 19.42 seconds


SELECT
  COUNT(1) AS NUM_ROWS,
  COUNT(DISTINCT IPR_ACCESSION) AS NUM_DISTINCT_IPRS,
  COUNT(DISTINCT PROTEIN_UID_KEY) AS NUM_DISTINCT_PROTEINS
  FROM
    IPR_PROTEIN_STAGING

+---------+-----------------+---------------------+
|NUM_ROWS |NUM_DISTINCT_IPRS|NUM_DISTINCT_PROTEINS|
+---------+-----------------+---------------------+
|146374065|25117            |42942941             |
+---------+-----------------+---------------------+

completed in 203.28 seconds


real	3m56.196s
user	22m7.994s
sys	7m21.794s
```
