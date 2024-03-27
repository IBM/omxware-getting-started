# GENOME_PROTEIN

[back to parent](../README.md)

Run the following to scrub the data into the finalized form:

```
./spark-sql.sh --sql-file sql/scrubbing/genome_protein.sql
```

OUTPUT

```sql
CACHE TABLE GENOME_PROTEIN_STAGING

completed in 85.22 seconds


CACHE TABLE GENOME_TABLE_STAGING

completed in 0.50 seconds


CACHE TABLE PROTEIN_DETAILS_STAGING

completed in 6.90 seconds


DROP TABLE IF EXISTS GENOME_PROTEIN

completed in 0.05 seconds


CREATE TABLE GENOME_PROTEIN
  USING PARQUET
  AS
  SELECT
    B.ACCESSION_NUMBER,
    B.PROTEIN_UID_KEY,
    B.LOCUS
    FROM
      GENOME_TABLE_STAGING A
      INNER JOIN GENOME_PROTEIN_STAGING B ON
        B.ACCESSION_NUMBER = A.ACCESSION_NUMBER
      INNER JOIN PROTEIN_DETAILS_STAGING C ON
        C.PROTEIN_UID_KEY = B.PROTEIN_UID_KEY
      GROUP BY
        B.ACCESSION_NUMBER,
        B.PROTEIN_UID_KEY,
        B.LOCUS

completed in 1180.15 seconds


CACHE TABLE GENOME_PROTEIN

completed in 49.29 seconds


SELECT
  COUNT(1) AS NUM_ROWS,
  COUNT(DISTINCT ACCESSION_NUMBER) AS NUM_DISTINCT_GENOMES,
  COUNT(DISTINCT PROTEIN_UID_KEY) AS NUM_DISTINCT_PROTEINS
  FROM
    GENOME_PROTEIN

+---------+--------------------+---------------------+
|NUM_ROWS |NUM_DISTINCT_GENOMES|NUM_DISTINCT_PROTEINS|
+---------+--------------------+---------------------+
|734747130|206752              |53836264             |
+---------+--------------------+---------------------+

completed in 86.89 seconds


SELECT *
  FROM
    GENOME_PROTEIN
    ORDER BY 1, 3
    LIMIT 10

+----------------+--------------------------------+-----+
|ACCESSION_NUMBER|PROTEIN_UID_KEY                 |LOCUS|
+----------------+--------------------------------+-----+
|DRR000852       |e64e1edddf8f309d22d035ea555551ba|1    |
|DRR000852       |ef4722507bcba3a45c65c34f3448da76|2    |
|DRR000852       |bc4ae5402da1f7ffc97e086d78530f1d|3    |
|DRR000852       |5211887f78b6a5a981f367fcb6978900|4    |
|DRR000852       |d0f6086f585607dc679855de13623b52|5    |
|DRR000852       |02156585fa000cdb6c629e49b3f4852d|6    |
|DRR000852       |201ba1d6b365d6b9df32993558412c74|7    |
|DRR000852       |2294ecc758be3a4f2086e48f805bc086|8    |
|DRR000852       |4a4919d315a881f9dc975ce936cf8a7f|9    |
|DRR000852       |d317bc59c5d5ec311f39c09b02c82c3c|10   |
+----------------+--------------------------------+-----+

completed in 4.58 seconds


DROP TABLE GENOME_PROTEIN_STAGING

completed in 0.56 seconds


real  23m44.617s
user  218m30.053s
sys  27m20.356s
```
