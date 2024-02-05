# Pivot Protein

This table contains proteins from FGP that match by exact domain architecture to proteins in VFDB. These proteins have some aspect of virulence related to them as they share IPR codes in common with known virulent proteins. They are named pivots because they formulate the basis for querying neighbors near them.

[back to parent](/Virulence-Analysis/methodology/analysis/README.md)

Run the following to create the data:

```
./spark-sql.sh --sql-file sql/core/pivot_protein.sql
```

OUTPUT

```sql
CACHE TABLE PROTEIN_DOMAIN_ARCHITECTURE

completed in 16.12 seconds


CACHE TABLE PROTEIN_VIRULENCE

completed in 0.44 seconds


DROP TABLE IF EXISTS PIVOT_PROTEIN

completed in 0.87 seconds


CREATE TABLE PIVOT_PROTEIN
  USING PARQUET
  AS
  SELECT
    C.PROTEIN_UID_KEY
    FROM
      PROTEIN_VIRULENCE A
      INNER JOIN PROTEIN_DOMAIN_ARCHITECTURE B ON
        B.PROTEIN_UID_KEY = A.PROTEIN_UID_KEY
      INNER JOIN PROTEIN_DOMAIN_ARCHITECTURE C ON
        C.DOMAIN_ARCHITECTURE_UID_KEY = B.DOMAIN_ARCHITECTURE_UID_KEY
      GROUP BY
        C.PROTEIN_UID_KEY

completed in 79.17 seconds


CACHE TABLE PIVOT_PROTEIN

completed in 0.92 seconds


SELECT
  COUNT(1) AS NUM_ROWS,
  COUNT(DISTINCT PROTEIN_UID_KEY) AS NUM_DISTINCT_PROTEINS
  FROM
    PIVOT_PROTEIN

+--------+---------------------+
|NUM_ROWS|NUM_DISTINCT_PROTEINS|
+--------+---------------------+
|11144804|11144804             |
+--------+---------------------+

completed in 10.64 seconds


SELECT *
  FROM
    PIVOT_PROTEIN
    ORDER BY 1
    LIMIT 10

+--------------------------------+
|PROTEIN_UID_KEY                 |
+--------------------------------+
|000001deccb2cbc508ab56ebb3bfd4ae|
|0000040804f857233b8a9784340f81b5|
|000004523e0e3080c6712895ea37d7b3|
|000004556e857e3389bfb2a404013119|
|00000501eae11222df749394c4e76336|
|0000058d83c805b530709ac138da68c3|
|000007a23801e41b6be5beace1beabf3|
|00000882368904f3e31509358692fe30|
|00000957297b64df4e4a2f82ccad99ed|
|000009c3dc9dde7e5c378d6c8ab81211|
+--------------------------------+

completed in 0.54 seconds


real	1m56.427s
user	17m29.424s
sys	3m22.785s
```
