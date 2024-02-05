# GENOME_PROTEIN_STAGING

[back to parent](../README.md)

Run the following to stage the data into Apache Spark:

```
./spark-sql.sh --sql-file sql/staging/genome_protein.sql
```

OUTPUT

```sql
SET best_similarity = 1

completed in 1.77 seconds

SET distance = 2

completed in 0.02 seconds

SET data_dir = /gpfs/grand/Users/eseabolt/virulence/data

completed in 0.01 seconds

SET outputs_dir = /gpfs/grand/Users/eseabolt/virulence/outputs

completed in 0.01 seconds


DROP TABLE IF EXISTS GENOME_PROTEIN_STAGING

completed in 4.42 seconds


CREATE TABLE GENOME_PROTEIN_STAGING (
  ACCESSION_NUMBER STRING,
  PROTEIN_UID_KEY STRING,
  LOCUS INT)
    USING csv
    OPTIONS (
      header false,
      path '${data_dir}/genome_protein.csv')

completed in 0.47 seconds


CACHE TABLE GENOME_PROTEIN_STAGING

completed in 84.42 seconds


SELECT
  COUNT(1) AS NUM_ROWS,
  COUNT(DISTINCT ACCESSION_NUMBER) AS NUM_DISTINCT_GENOMES,
  COUNT(DISTINCT PROTEIN_UID_KEY) AS NUM_DISTINCT_PROTEINS
  FROM
    GENOME_PROTEIN_STAGING

+---------+--------------------+---------------------+
|NUM_ROWS |NUM_DISTINCT_GENOMES|NUM_DISTINCT_PROTEINS|
+---------+--------------------+---------------------+
|734772080|206762              |53836975             |
+---------+--------------------+---------------------+

completed in 305.12 seconds


real  6m46.629s
user  90m57.691s
sys  14m15.292s
```
