# IPR_PROTEIN

[back to parent](../README.md)

Run the following to scrub the data into the finalized form:

```
./spark-sql.sh --sql-file sql/scrubbing/ipr_protein.sql
```

OUTPUT

```sql
CACHE TABLE IPR

completed in 8.05 seconds


CACHE TABLE IPR_PROTEIN_STAGING

completed in 16.93 seconds


CACHE TABLE GENOME_PROTEIN

completed in 75.49 seconds


DROP TABLE IF EXISTS IPR_PROTEIN

completed in 1.66 seconds


CREATE TABLE IPR_PROTEIN
  USING PARQUET
  AS
  SELECT
    B.IPR_ACCESSION,
    B.PROTEIN_UID_KEY
    FROM
      IPR A
      INNER JOIN IPR_PROTEIN_STAGING B ON
        B.IPR_ACCESSION = A.IPR_ACCESSION
      INNER JOIN GENOME_PROTEIN C ON
        C.PROTEIN_UID_KEY = B.PROTEIN_UID_KEY
      GROUP BY
        B.IPR_ACCESSION,
        B.PROTEIN_UID_KEY

completed in 309.01 seconds


CACHE TABLE IPR_PROTEIN

completed in 9.46 seconds


SELECT
  COUNT(1) AS NUM_ROWS,
  COUNT(DISTINCT IPR_ACCESSION) AS NUM_DISTINCT_IPRS,
  COUNT(DISTINCT PROTEIN_UID_KEY) AS NUM_DISTINCT_PROTEINS
  FROM
    IPR_PROTEIN

+---------+-----------------+---------------------+
|NUM_ROWS |NUM_DISTINCT_IPRS|NUM_DISTINCT_PROTEINS|
+---------+-----------------+---------------------+
|145642408|25043            |42724008             |
+---------+-----------------+---------------------+

completed in 64.19 seconds


SELECT *
  FROM
    IPR_PROTEIN
    ORDER BY 1
    LIMIT 10

+-------------+--------------------------------+
|IPR_ACCESSION|PROTEIN_UID_KEY                 |
+-------------+--------------------------------+
|IPR000001    |b1ae519ef7335ee7a91813351ec19039|
|IPR000001    |371bb3eefc49e90d0ca5d703883d0655|
|IPR000001    |47798564974909ab7593f5bb64b15393|
|IPR000001    |b3d518bdfb15a0a48b6d1fd189cd3ed3|
|IPR000001    |96413630d16249d64746b34efe3472bd|
|IPR000001    |ee82a1307443cf9df76fa919d0189fbf|
|IPR000001    |06981eacbbb356c24cdf7f198fd0f45b|
|IPR000001    |86004bf154de2b7f534562231f1d97c9|
|IPR000001    |18a8187fb5e6448fae33c5376d001c73|
|IPR000001    |b6e19836fc139b8c253a2df0946325d3|
+-------------+--------------------------------+

completed in 1.59 seconds


DROP TABLE IPR_PROTEIN_STAGING

completed in 0.13 seconds


real	8m17.781s
user	101m10.284s
sys	12m38.769s
```
