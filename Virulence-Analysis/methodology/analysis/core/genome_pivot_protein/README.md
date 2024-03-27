# Genome Pivot Protein

This table is an extension of the PIVOT_PROTEIN and records the genome accession and locus of the pivot. Note that the number of distinct genomes recorded here is a little less than in the original GENOME_TABLE and GENOME_PROTEIN tables. This is due to not all proteins in all genomes have a match in VFDB to be considered a pivot. Thus, those genomes will not be recorded here and fall out of the analysis.

[back to parent](/Virulence-Analysis/methodology/analysis/README.md)

Run the following to create the data:

```
./spark-sql.sh --sql-file sql/core/genome_pivot_protein.sql
```

OUTPUT

```sql
CACHE TABLE GENOME_PROTEIN

completed in 89.76 seconds


CACHE TABLE PIVOT_PROTEIN

completed in 1.32 seconds


DROP TABLE IF EXISTS GENOME_PIVOT_PROTEIN

completed in 1.38 seconds


CREATE TABLE GENOME_PIVOT_PROTEIN
  USING PARQUET
  AS
  SELECT
    B.ACCESSION_NUMBER,
    B.PROTEIN_UID_KEY,
    B.LOCUS
    FROM
      PIVOT_PROTEIN A
      INNER JOIN GENOME_PROTEIN B ON
        B.PROTEIN_UID_KEY = A.PROTEIN_UID_KEY
      GROUP BY
        B.ACCESSION_NUMBER,
        B.PROTEIN_UID_KEY,
        B.LOCUS

completed in 274.43 seconds


CACHE TABLE GENOME_PIVOT_PROTEIN

completed in 17.14 seconds


SELECT
  COUNT(1) AS NUM_ROWS,
  COUNT(DISTINCT ACCESSION_NUMBER) AS NUM_DISTINCT_GENOMES,
  COUNT(DISTINCT PROTEIN_UID_KEY) AS NUM_DISTINCT_PROTEINS
  FROM
    GENOME_PIVOT_PROTEIN

+---------+--------------------+---------------------+
|NUM_ROWS |NUM_DISTINCT_GENOMES|NUM_DISTINCT_PROTEINS|
+---------+--------------------+---------------------+
|154961983|206575              |11144804             |
+---------+--------------------+---------------------+

completed in 23.62 seconds


SELECT *
  FROM
    GENOME_PIVOT_PROTEIN
    ORDER BY 1, 3
    LIMIT 10

+----------------+--------------------------------+-----+
|ACCESSION_NUMBER|PROTEIN_UID_KEY                 |LOCUS|
+----------------+--------------------------------+-----+
|DRR000852       |e64e1edddf8f309d22d035ea555551ba|1    |
|DRR000852       |02156585fa000cdb6c629e49b3f4852d|6    |
|DRR000852       |201ba1d6b365d6b9df32993558412c74|7    |
|DRR000852       |6b552353a6f546e2fa0542f50531061b|15   |
|DRR000852       |94694d7948e8d65e09165619aaad159d|16   |
|DRR000852       |f63db225e2e690776a96cff530bd56d6|41   |
|DRR000852       |6b3d70902807db9d9c27e609df63a0a5|79   |
|DRR000852       |acc3137c32d710cbde7dec4c9a9356fd|90   |
|DRR000852       |e14e83fbee3dcb0b66892d2de024bf1d|96   |
|DRR000852       |522778a81d0d1d0b0f8363b99cf399e5|97   |
+----------------+--------------------------------+-----+

completed in 1.57 seconds


real	6m59.956s
user	95m3.237s
sys	10m58.802s
```
