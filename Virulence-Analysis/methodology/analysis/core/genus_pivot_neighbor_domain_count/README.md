# Genus Pivot Neighbor Domain Count

This table represents the rollup of neighbor domain architecture counts to be used for determination of minimum cutoff threshold by genus.

[back to parent](/Virulence-Analysis/methodology/analysis/README.md)

Run the following to create the data:

```
./spark-sql.sh --sql-file sql/core/genus_pivot_neighbor_domain_count.sql
```

OUTPUT

```sql
CACHE TABLE GENOME_PIVOT_NEIGHBOR_DOMAIN_COUNT

completed in 97.45 seconds


CACHE TABLE GENOME_TABLE

completed in 0.49 seconds


DROP TABLE IF EXISTS GENUS_PIVOT_NEIGHBOR_DOMAIN_COUNT

completed in 1.11 seconds


CREATE TABLE GENUS_PIVOT_NEIGHBOR_DOMAIN_COUNT
  USING PARQUET
  AS
  SELECT
    A.GENUS_NAME,
    B.PIVOT_DOMAIN_ARCHITECTURE_UID_KEY,
    B.NEIGHBOR_DOMAIN_ARCHITECTURE_UID_KEY,
    B.NEIGHBOR_TYPE,
    SUM(B.COUNT) AS COUNT
    FROM
      GENOME_TABLE A
      INNER JOIN GENOME_PIVOT_NEIGHBOR_DOMAIN_COUNT B ON
        B.ACCESSION_NUMBER = A.ACCESSION_NUMBER
      GROUP BY
        A.GENUS_NAME,
        B.PIVOT_DOMAIN_ARCHITECTURE_UID_KEY,
        B.NEIGHBOR_DOMAIN_ARCHITECTURE_UID_KEY,
        B.NEIGHBOR_TYPE

completed in 196.66 seconds


CACHE TABLE GENUS_PIVOT_NEIGHBOR_DOMAIN_COUNT

completed in 2.33 seconds


SELECT
  COUNT(1) AS NUM_ROWS,
  COUNT(DISTINCT GENUS_NAME) AS NUM_DISTINCT_GENERA,
  COUNT(DISTINCT PIVOT_DOMAIN_ARCHITECTURE_UID_KEY) AS NUM_DISTINCT_PIVOT_DAS,
  COUNT(DISTINCT NEIGHBOR_DOMAIN_ARCHITECTURE_UID_KEY) AS NUM_DISTINCT_NEIGHBOR_DAS
  FROM
    GENUS_PIVOT_NEIGHBOR_DOMAIN_COUNT

+--------+-------------------+----------------------+-------------------------+
|NUM_ROWS|NUM_DISTINCT_GENERA|NUM_DISTINCT_PIVOT_DAS|NUM_DISTINCT_NEIGHBOR_DAS|
+--------+-------------------+----------------------+-------------------------+
|11586596|1401               |2599                  |205665                   |
+--------+-------------------+----------------------+-------------------------+

completed in 5.18 seconds


SELECT *
  FROM
    GENUS_PIVOT_NEIGHBOR_DOMAIN_COUNT
    ORDER BY 1, 5 DESC
    LIMIT 10

+-----------+---------------------------------+------------------------------------+-------------+-----+
|GENUS_NAME |PIVOT_DOMAIN_ARCHITECTURE_UID_KEY|NEIGHBOR_DOMAIN_ARCHITECTURE_UID_KEY|NEIGHBOR_TYPE|COUNT|
+-----------+---------------------------------+------------------------------------+-------------+-----+
|abiotrophia|35cc3325c2d5d06c3c63074c20e09c1c |35cc3325c2d5d06c3c63074c20e09c1c    |P            |48   |
|abiotrophia|abf0fb6ee6c6d9aae6872e0e026a7e13 |abf0fb6ee6c6d9aae6872e0e026a7e13    |P            |43   |
|abiotrophia|35cc3325c2d5d06c3c63074c20e09c1c |35cc3325c2d5d06c3c63074c20e09c1c    |C            |36   |
|abiotrophia|d2bf9490c445b2e114aef9be1cc5e539 |d2bf9490c445b2e114aef9be1cc5e539    |P            |34   |
|abiotrophia|2b17e8fd881d02567be099bbdffc82e8 |2b17e8fd881d02567be099bbdffc82e8    |P            |33   |
|abiotrophia|abf0fb6ee6c6d9aae6872e0e026a7e13 |null                                |PD           |32   |
|abiotrophia|d2bf9490c445b2e114aef9be1cc5e539 |d2bf9490c445b2e114aef9be1cc5e539    |C            |22   |
|abiotrophia|3f06b56054bd0e5b4555f79fcee89cb4 |null                                |PD           |21   |
|abiotrophia|35cc3325c2d5d06c3c63074c20e09c1c |85c5765ba2807176221e7f7787d3ec77    |C            |16   |
|abiotrophia|35cc3325c2d5d06c3c63074c20e09c1c |null                                |PD           |16   |
+-----------+---------------------------------+------------------------------------+-------------+-----+

completed in 0.53 seconds


real	5m13.497s
user	103m22.896s
sys	9m14.331s
```
