# Genome Pivot Neighbor Domain Count

This table records neighbor occurrence counts by genome accession number and pivot domain architecture.

[back to parent](/Virulence-Analysis/methodology/analysis/README.md)

Run the following to create the data:

```
./spark-sql.sh --sql-file sql/core/genome_pivot_neighbor_domain_count.sql
```

OUTPUT

```sql
CACHE TABLE GENOME_PIVOT_NEIGHBOR_PROTEIN_DOMAIN

completed in 196.36 seconds


DROP TABLE IF EXISTS GENOME_PIVOT_NEIGHBOR_DOMAIN_COUNT

completed in 1.68 seconds


CREATE TABLE GENOME_PIVOT_NEIGHBOR_DOMAIN_COUNT
  USING PARQUET
  AS
  SELECT
    ACCESSION_NUMBER,
    PIVOT_DOMAIN_ARCHITECTURE_UID_KEY,
    NEIGHBOR_DOMAIN_ARCHITECTURE_UID_KEY,
    NEIGHBOR_TYPE,
    COUNT(NEIGHBOR_DOMAIN_ARCHITECTURE_UID_KEY) AS COUNT
    FROM
      GENOME_PIVOT_NEIGHBOR_PROTEIN_DOMAIN
      GROUP BY
        ACCESSION_NUMBER,
        PIVOT_DOMAIN_ARCHITECTURE_UID_KEY,
        NEIGHBOR_DOMAIN_ARCHITECTURE_UID_KEY,
        NEIGHBOR_TYPE

completed in 857.14 seconds


CACHE TABLE GENOME_PIVOT_NEIGHBOR_DOMAIN_COUNT

completed in 100.16 seconds


SELECT
  COUNT(1) AS NUM_ROWS,
  COUNT(DISTINCT ACCESSION_NUMBER) AS NUM_DISTINCT_GENOMES,
  COUNT(DISTINCT PIVOT_DOMAIN_ARCHITECTURE_UID_KEY) AS NUM_DISTINCT_PIVOT_DAS,
  COUNT(DISTINCT NEIGHBOR_DOMAIN_ARCHITECTURE_UID_KEY) AS NUM_DISTINCT_NEIGHBOR_DAS
  FROM
    GENOME_PIVOT_NEIGHBOR_DOMAIN_COUNT

+---------+--------------------+----------------------+-------------------------+
|NUM_ROWS |NUM_DISTINCT_GENOMES|NUM_DISTINCT_PIVOT_DAS|NUM_DISTINCT_NEIGHBOR_DAS|
+---------+--------------------+----------------------+-------------------------+
|604924777|206575              |2599                  |205665                   |
+---------+--------------------+----------------------+-------------------------+

completed in 29.73 seconds


SELECT *
  FROM
    GENOME_PIVOT_NEIGHBOR_DOMAIN_COUNT
    ORDER BY 1, 5 DESC
    LIMIT 10

+----------------+---------------------------------+------------------------------------+-------------+-----+
|ACCESSION_NUMBER|PIVOT_DOMAIN_ARCHITECTURE_UID_KEY|NEIGHBOR_DOMAIN_ARCHITECTURE_UID_KEY|NEIGHBOR_TYPE|COUNT|
+----------------+---------------------------------+------------------------------------+-------------+-----+
|DRR000852       |2b17e8fd881d02567be099bbdffc82e8 |2b17e8fd881d02567be099bbdffc82e8    |P            |35   |
|DRR000852       |a9b90241e2e1072a57ace851c11b18ae |a9b90241e2e1072a57ace851c11b18ae    |P            |32   |
|DRR000852       |35cc3325c2d5d06c3c63074c20e09c1c |35cc3325c2d5d06c3c63074c20e09c1c    |P            |26   |
|DRR000852       |abf0fb6ee6c6d9aae6872e0e026a7e13 |abf0fb6ee6c6d9aae6872e0e026a7e13    |P            |22   |
|DRR000852       |6585ba0aec245f2dd4a6783d328bfb65 |6585ba0aec245f2dd4a6783d328bfb65    |P            |18   |
|DRR000852       |101b6dc7e771d73386ca42591b4d85c8 |101b6dc7e771d73386ca42591b4d85c8    |P            |18   |
|DRR000852       |35cc3325c2d5d06c3c63074c20e09c1c |35cc3325c2d5d06c3c63074c20e09c1c    |C            |18   |
|DRR000852       |3f06b56054bd0e5b4555f79fcee89cb4 |3f06b56054bd0e5b4555f79fcee89cb4    |P            |15   |
|DRR000852       |e9ddc6d406d05903e4a2232b67fe0af6 |e9ddc6d406d05903e4a2232b67fe0af6    |P            |13   |
|DRR000852       |28aa119903d4a9aae5066d49a603e2f9 |28aa119903d4a9aae5066d49a603e2f9    |P            |13   |
+----------------+---------------------------------+------------------------------------+-------------+-----+

completed in 7.04 seconds


real	20m2.742s
user	326m59.345s
sys	25m24.286s
```
