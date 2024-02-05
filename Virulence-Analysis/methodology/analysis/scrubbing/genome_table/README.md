# GENOME_TABLE

[back to parent](../README.md)

Run the following to scrub the data into the finalized form:

```
./spark-sql.sh --sql-file sql/scrubbing/genome_table.sql
```

OUTPUT

```sql
CACHE TABLE GENOME_TABLE_STAGING

completed in 7.99 seconds


CACHE TABLE GENOME_PROTEIN

completed in 60.73 seconds


DROP TABLE IF EXISTS GENOME_TABLE

completed in 1.58 seconds


CREATE TABLE GENOME_TABLE
  USING PARQUET
  AS
  SELECT
    A.GENUS_NAME,
    A.ACCESSION_NUMBER
    FROM
      GENOME_TABLE_STAGING A
      INNER JOIN GENOME_PROTEIN B ON
        B.ACCESSION_NUMBER = A.ACCESSION_NUMBER
      GROUP BY
        A.GENUS_NAME,
        A.ACCESSION_NUMBER

completed in 66.44 seconds


CACHE TABLE GENOME_TABLE

completed in 0.33 seconds


SELECT
  COUNT(1) AS NUM_ROWS,
  COUNT(DISTINCT GENUS_NAME) AS NUM_DISTINCT_GENERA,
  COUNT(DISTINCT ACCESSION_NUMBER) AS NUM_DISTINCT_GENOMES
  FROM
    GENOME_TABLE

+--------+-------------------+--------------------+
|NUM_ROWS|NUM_DISTINCT_GENERA|NUM_DISTINCT_GENOMES|
+--------+-------------------+--------------------+
|206752  |1409               |206752              |
+--------+-------------------+--------------------+

completed in 2.96 seconds


SELECT *
  FROM
    GENOME_TABLE
      ORDER BY
        ACCESSION_NUMBER
      LIMIT 10

+-------------+----------------+
|GENUS_NAME   |ACCESSION_NUMBER|
+-------------+----------------+
|bacillus     |DRR000852       |
|pseudomonas  |DRR001171       |
|streptococcus|DRR014268       |
|streptococcus|DRR014269       |
|streptococcus|DRR014272       |
|streptococcus|DRR014273       |
|streptococcus|DRR014287       |
|streptococcus|DRR014301       |
|streptococcus|DRR014309       |
|bacillus     |DRR014327       |
+-------------+----------------+

completed in 0.18 seconds


DROP TABLE GENOME_TABLE_STAGING

completed in 0.12 seconds


real	2m29.243s
user	77m21.726s
sys	6m55.606s
```
