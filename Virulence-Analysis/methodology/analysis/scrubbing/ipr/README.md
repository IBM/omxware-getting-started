# IPR

[back to parent](../README.md)

Run the following to scrub the data into the finalized form:

```
./spark-sql.sh --sql-file sql/scrubbing/ipr.sql
```

OUTPUT

```sql
CACHE TABLE IPR_STAGING

completed in 7.58 seconds


DROP TABLE IF EXISTS IPR

completed in 0.60 seconds


CREATE TABLE IPR
  USING PARQUET
  AS
  SELECT
    IPR_ACCESSION,
    TYPE,
    NAME,
    DESCRIPTION
    FROM
      IPR_STAGING

completed in 1.51 seconds


CACHE TABLE IPR

completed in 0.42 seconds


SELECT
  IPR_ACCESSION,
  COUNT(IPR_ACCESSION) AS DUPLICATE_COUNT
  FROM
    IPR
    GROUP BY
      IPR_ACCESSION
    HAVING
      COUNT(IPR_ACCESSION) > 1

+-------------+---------------+
|IPR_ACCESSION|DUPLICATE_COUNT|
+-------------+---------------+
+-------------+---------------+

completed in 0.85 seconds


SELECT
  COUNT(1) AS NUM_ROWS,
  COUNT(DISTINCT IPR_ACCESSION) AS NUM_DISTINCT_IPRS,
  COUNT(DISTINCT TYPE) AS NUM_DISTINCT_TYPES
  FROM
    IPR

+--------+-----------------+------------------+
|NUM_ROWS|NUM_DISTINCT_IPRS|NUM_DISTINCT_TYPES|
+--------+-----------------+------------------+
|37110   |37110            |8                 |
+--------+-----------------+------------------+

completed in 1.11 seconds


SELECT *
  FROM
    IPR
    ORDER BY 1
    LIMIT 10

+-------------+------+-----------------------------------+----------------------------------------------+
|IPR_ACCESSION|TYPE  |NAME                               |DESCRIPTION                                   |
+-------------+------+-----------------------------------+----------------------------------------------+
|IPR000001    |DOMAIN|Kringle                            |Kringle                                       |
|IPR000003    |FAMILY|Retinoid X receptor/HNF4           |null                                          |
|IPR000006    |FAMILY|Metallothionein, vertebrate        |null                                          |
|IPR000007    |DOMAIN|Tubby, C-terminal                  |null                                          |
|IPR000008    |DOMAIN|C2_dom                             |C2 domain                                     |
|IPR000009    |FAMILY|PP2A_PR55                          |Protein phosphatase 2A regulatory subunit PR55|
|IPR000010    |DOMAIN|Cystatin_dom                       |Cystatin domain                               |
|IPR000011    |FAMILY|Ubiquitin/SUMO-activating enzyme E1|null                                          |
|IPR000012    |FAMILY|Retroviral VpR/VpX protein         |null                                          |
|IPR000013    |FAMILY|Peptidase_M7                       |Peptidase M7, snapalysin                      |
+-------------+------+-----------------------------------+----------------------------------------------+

completed in 0.20 seconds


DROP TABLE IPR_STAGING

completed in 0.12 seconds


real	0m17.205s
user	1m4.225s
sys	0m6.907s
```
