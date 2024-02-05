# Genus Pivot Neighbor Domain Count Final

This table contains the final counts after filtering by the minimum cutoff threshold calculated in previous steps. At this stage, any neighboring domain architecture that is a putative discovery (PD) and is greater than or equal to the threshold for its genus will be considered a discovery and marked with D. Items that are either P or C are retained regardless of threshold. Note that this table will not contain any neighbor architecture that are null.

[back to parent](/analysis/README.md)

Run the following to create the data:

```
./spark-sql.sh --sql-file sql/core/genus_pivot_neighbor_domain_count_final.sql
```

OUTPUT

```sql
CACHE TABLE GENUS_MINIMUM_CUTOFF_THRESHOLD

completed in 9.26 seconds


CACHE TABLE GENUS_PIVOT_NEIGHBOR_DOMAIN_COUNT

completed in 2.79 seconds


DROP TABLE IF EXISTS GENUS_PIVOT_NEIGHBOR_DOMAIN_COUNT_FINAL

completed in 0.87 seconds


CREATE TABLE GENUS_PIVOT_NEIGHBOR_DOMAIN_COUNT_FINAL
  USING PARQUET
  AS
  SELECT
    A.GENUS_NAME,
    A.PIVOT_DOMAIN_ARCHITECTURE_UID_KEY,
    A.NEIGHBOR_DOMAIN_ARCHITECTURE_UID_KEY,
    CASE WHEN A.NEIGHBOR_TYPE = 'PD'
      THEN 'D'
      ELSE A.NEIGHBOR_TYPE
    END AS NEIGHBOR_TYPE,
    A.COUNT
    FROM
      GENUS_PIVOT_NEIGHBOR_DOMAIN_COUNT A
      INNER JOIN GENUS_MINIMUM_CUTOFF_THRESHOLD B ON
        B.GENUS_NAME = A.GENUS_NAME AND
        (A.NEIGHBOR_TYPE != 'PD' OR A.COUNT >= B.THRESHOLD)
      WHERE
        A.NEIGHBOR_DOMAIN_ARCHITECTURE_UID_KEY IS NOT NULL

completed in 4.37 seconds


CACHE TABLE GENUS_PIVOT_NEIGHBOR_DOMAIN_COUNT_FINAL

completed in 1.31 seconds


SELECT
  COUNT(1) AS NUM_ROWS,
  COUNT(DISTINCT GENUS_NAME) AS NUM_DISTINCT_GENERA,
  COUNT(DISTINCT PIVOT_DOMAIN_ARCHITECTURE_UID_KEY) AS NUM_DISTINCT_PIVOT_DAS,
  COUNT(DISTINCT NEIGHBOR_DOMAIN_ARCHITECTURE_UID_KEY) AS NUM_DISTINCT_NEIGHBOR_DAS
  FROM
    GENUS_PIVOT_NEIGHBOR_DOMAIN_COUNT_FINAL

+--------+-------------------+----------------------+-------------------------+
|NUM_ROWS|NUM_DISTINCT_GENERA|NUM_DISTINCT_PIVOT_DAS|NUM_DISTINCT_NEIGHBOR_DAS|
+--------+-------------------+----------------------+-------------------------+
|5881993 |1400               |2599                  |82659                    |
+--------+-------------------+----------------------+-------------------------+

completed in 6.51 seconds


SELECT *
  FROM
    GENUS_PIVOT_NEIGHBOR_DOMAIN_COUNT_FINAL
    ORDER BY 1, 5 DESC
    LIMIT 20

+-----------+---------------------------------+------------------------------------+-------------+-----+
|GENUS_NAME |PIVOT_DOMAIN_ARCHITECTURE_UID_KEY|NEIGHBOR_DOMAIN_ARCHITECTURE_UID_KEY|NEIGHBOR_TYPE|COUNT|
+-----------+---------------------------------+------------------------------------+-------------+-----+
|abiotrophia|35cc3325c2d5d06c3c63074c20e09c1c |35cc3325c2d5d06c3c63074c20e09c1c    |P            |48   |
|abiotrophia|abf0fb6ee6c6d9aae6872e0e026a7e13 |abf0fb6ee6c6d9aae6872e0e026a7e13    |P            |43   |
|abiotrophia|35cc3325c2d5d06c3c63074c20e09c1c |35cc3325c2d5d06c3c63074c20e09c1c    |C            |36   |
|abiotrophia|d2bf9490c445b2e114aef9be1cc5e539 |d2bf9490c445b2e114aef9be1cc5e539    |P            |34   |
|abiotrophia|2b17e8fd881d02567be099bbdffc82e8 |2b17e8fd881d02567be099bbdffc82e8    |P            |33   |
|abiotrophia|d2bf9490c445b2e114aef9be1cc5e539 |d2bf9490c445b2e114aef9be1cc5e539    |C            |22   |
|abiotrophia|35cc3325c2d5d06c3c63074c20e09c1c |85c5765ba2807176221e7f7787d3ec77    |C            |16   |
|abiotrophia|85c5765ba2807176221e7f7787d3ec77 |35cc3325c2d5d06c3c63074c20e09c1c    |C            |16   |
|abiotrophia|3f06b56054bd0e5b4555f79fcee89cb4 |3f06b56054bd0e5b4555f79fcee89cb4    |P            |15   |
|abiotrophia|6a1bd247f5a0cb89cb0e9008bdc50e96 |6a1bd247f5a0cb89cb0e9008bdc50e96    |P            |15   |
|abiotrophia|e7f768f9aad8cdf55abe1dcd561a9527 |e7f768f9aad8cdf55abe1dcd561a9527    |P            |12   |
|abiotrophia|e6bbe3dab84c495b4f249e47fb2121d7 |e6bbe3dab84c495b4f249e47fb2121d7    |P            |10   |
|abiotrophia|85ba02fff094a9e6527c0e5d1e541989 |85ba02fff094a9e6527c0e5d1e541989    |P            |8    |
|abiotrophia|35cc3325c2d5d06c3c63074c20e09c1c |52afd54482e6a62475c81deec2390977    |D            |8    |
|abiotrophia|85c5765ba2807176221e7f7787d3ec77 |85c5765ba2807176221e7f7787d3ec77    |P            |8    |
|abiotrophia|a7987ea3e29487d7ce110f5e52350627 |a7987ea3e29487d7ce110f5e52350627    |P            |7    |
|abiotrophia|2e517330a138f68948efa9cc1c35530d |2e517330a138f68948efa9cc1c35530d    |P            |7    |
|abiotrophia|bab5d992bbdd43ea0f077c27663d983c |bab5d992bbdd43ea0f077c27663d983c    |P            |7    |
|abiotrophia|8ce27d592d713e29963826d14087446d |8ce27d592d713e29963826d14087446d    |P            |7    |
|abiotrophia|d2bf9490c445b2e114aef9be1cc5e539 |2b17e8fd881d02567be099bbdffc82e8    |C            |6    |
+-----------+---------------------------------+------------------------------------+-------------+-----+

completed in 0.61 seconds


real	0m33.439s
user	6m23.781s
sys	1m19.867s
```
