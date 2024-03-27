# Genus Percent Site Based

The following generates a table reporting the percent pivot, co-pivot, and discoveries that are **site only** and with final domain architecture counts post-Kneedle analysis. 

[back to parent](/Virulence-Analysis/methodology/analysis/README.md)

* [Table Creation](#table-creation)
* [Data Export](#data-export)

Exported file is located at [virulence_prediction_genus_pct_site_based.csv.gz](https://precision.fda.gov/home/files/file-Gj1Vv400ZqJvz5ykFZxYKzQF-2). You will need a [precisionFDA](https://precision.fda.gov/) account to access.

### Table Creation

Run the following to create the data:

```
./spark-sql.sh --sql-file sql/core/genus_pct_site_based.sql
```

OUTPUT

```sql
CACHE TABLE DOMAIN_ARCHITECTURE

completed in 9.67 seconds


CACHE TABLE GENUS_PIVOT_NEIGHBOR_DOMAIN_COUNT_FINAL

completed in 2.31 seconds

-- represents the unique count of site only domain architectures BEFORE computing minimum cutoff threshold


SELECT
  COUNT(DISTINCT DOMAIN_ARCHITECTURE_UID_KEY) AS NUM_DISTINCT_SITE_ONLY_DAS
  FROM
    DOMAIN_ARCHITECTURE
    WHERE
      NUM_DOMAIN = 0 AND
      NUM_FAMILY = 0 AND
      NUM_HOMOLOGOUS_SUPERFAMILY = 0

+--------------------------+
|NUM_DISTINCT_SITE_ONLY_DAS|
+--------------------------+
|843                       |
+--------------------------+

completed in 1.51 seconds


DROP VIEW IF EXISTS SITE_ONLY_DOMAIN_ARCHITECTURE

completed in 0.03 seconds

-- represents the unique set of site only domain architectures AFTER computing minimum cutoff threshold


CREATE VIEW SITE_ONLY_DOMAIN_ARCHITECTURE
  AS
  SELECT DISTINCT
    B.DOMAIN_ARCHITECTURE_UID_KEY
    FROM
      GENUS_PIVOT_NEIGHBOR_DOMAIN_COUNT_FINAL A
      INNER JOIN DOMAIN_ARCHITECTURE B ON
        B.DOMAIN_ARCHITECTURE_UID_KEY = A.NEIGHBOR_DOMAIN_ARCHITECTURE_UID_KEY
      WHERE
        B.NUM_DOMAIN = 0 AND
        B.NUM_FAMILY = 0 AND
        B.NUM_HOMOLOGOUS_SUPERFAMILY = 0

completed in 0.36 seconds


CACHE TABLE SITE_ONLY_DOMAIN_ARCHITECTURE

completed in 9.47 seconds


SELECT
  COUNT(1) AS NUM_ROWS,
  COUNT(DISTINCT DOMAIN_ARCHITECTURE_UID_KEY) AS NUM_DISTINCT_SITE_ONLY_DAS
  FROM
    SITE_ONLY_DOMAIN_ARCHITECTURE

+--------+--------------------------+
|NUM_ROWS|NUM_DISTINCT_SITE_ONLY_DAS|
+--------+--------------------------+
|277     |277                       |
+--------+--------------------------+

completed in 0.96 seconds


SELECT *
  FROM
    SITE_ONLY_DOMAIN_ARCHITECTURE
    ORDER BY 1
    LIMIT 5

+--------------------------------+
|DOMAIN_ARCHITECTURE_UID_KEY     |
+--------------------------------+
|01562272dc3249f9e16efba899cfd555|
|033659ef6e8597ad66b3ee8f65ea7256|
|0514987356d95e91ad65298f0b4315e3|
|05b1400aa245f9a3c8c9ee2819442de1|
|096b13623cd09bdb8aadec066bf93212|
+--------------------------------+

completed in 0.27 seconds


DROP VIEW IF EXISTS PIVOT_SITE_ONLY_DOMAIN_ARCHITECTURE

completed in 0.01 seconds


CREATE VIEW PIVOT_SITE_ONLY_DOMAIN_ARCHITECTURE
  AS
  SELECT DISTINCT
    A.PIVOT_DOMAIN_ARCHITECTURE_UID_KEY AS DOMAIN_ARCHITECTURE_UID_KEY
    FROM
      GENUS_PIVOT_NEIGHBOR_DOMAIN_COUNT_FINAL A
      INNER JOIN SITE_ONLY_DOMAIN_ARCHITECTURE B ON
        B.DOMAIN_ARCHITECTURE_UID_KEY = A.PIVOT_DOMAIN_ARCHITECTURE_UID_KEY
      WHERE
        A.NEIGHBOR_TYPE = 'P'

completed in 0.12 seconds


CACHE TABLE PIVOT_SITE_ONLY_DOMAIN_ARCHITECTURE

completed in 1.85 seconds


SELECT
  COUNT(1) AS NUM_ROWS,
  COUNT(DISTINCT DOMAIN_ARCHITECTURE_UID_KEY) AS NUM_DISTINCT_SITE_ONLY_DAS
  FROM
    PIVOT_SITE_ONLY_DOMAIN_ARCHITECTURE

+--------+--------------------------+
|NUM_ROWS|NUM_DISTINCT_SITE_ONLY_DAS|
+--------+--------------------------+
|20      |20                        |
+--------+--------------------------+

completed in 1.45 seconds


SELECT *
  FROM
    PIVOT_SITE_ONLY_DOMAIN_ARCHITECTURE
    ORDER BY 1
    LIMIT 5

+--------------------------------+
|DOMAIN_ARCHITECTURE_UID_KEY     |
+--------------------------------+
|1b86094f05e98d681c45e6310d0789d8|
|1ca28c7dfa64910a8e2cda18063133ee|
|2eb0025cad5c05a6cd9e3a9d8ccee488|
|317c9691bddbdb1aa48193c8808572a1|
|389c6bbc00603ea0eda7b50c4d1f1c6d|
+--------------------------------+

completed in 0.21 seconds


DROP VIEW IF EXISTS COPIVOT_SITE_ONLY_DOMAIN_ARCHITECTURE

completed in 0.01 seconds


CREATE VIEW COPIVOT_SITE_ONLY_DOMAIN_ARCHITECTURE
  AS
  SELECT DISTINCT
    A.NEIGHBOR_DOMAIN_ARCHITECTURE_UID_KEY AS DOMAIN_ARCHITECTURE_UID_KEY
    FROM
      GENUS_PIVOT_NEIGHBOR_DOMAIN_COUNT_FINAL A
      INNER JOIN SITE_ONLY_DOMAIN_ARCHITECTURE B ON
        B.DOMAIN_ARCHITECTURE_UID_KEY = A.NEIGHBOR_DOMAIN_ARCHITECTURE_UID_KEY
      WHERE
        A.NEIGHBOR_TYPE = 'C'

completed in 0.10 seconds


CACHE TABLE COPIVOT_SITE_ONLY_DOMAIN_ARCHITECTURE

completed in 1.75 seconds


SELECT
  COUNT(1) AS NUM_ROWS,
  COUNT(DISTINCT DOMAIN_ARCHITECTURE_UID_KEY) AS NUM_DISTINCT_SITE_ONLY_DAS
  FROM
    COPIVOT_SITE_ONLY_DOMAIN_ARCHITECTURE

+--------+--------------------------+
|NUM_ROWS|NUM_DISTINCT_SITE_ONLY_DAS|
+--------+--------------------------+
|20      |20                        |
+--------+--------------------------+

completed in 0.70 seconds


SELECT *
  FROM
    COPIVOT_SITE_ONLY_DOMAIN_ARCHITECTURE
    ORDER BY 1
    LIMIT 5

+--------------------------------+
|DOMAIN_ARCHITECTURE_UID_KEY     |
+--------------------------------+
|1b86094f05e98d681c45e6310d0789d8|
|1ca28c7dfa64910a8e2cda18063133ee|
|2eb0025cad5c05a6cd9e3a9d8ccee488|
|317c9691bddbdb1aa48193c8808572a1|
|389c6bbc00603ea0eda7b50c4d1f1c6d|
+--------------------------------+

completed in 0.18 seconds


DROP VIEW IF EXISTS DISCOVERED_SITE_ONLY_DOMAIN_ARCHITECTURE

completed in 0.01 seconds


CREATE VIEW DISCOVERED_SITE_ONLY_DOMAIN_ARCHITECTURE
  AS
  SELECT DISTINCT
    A.NEIGHBOR_DOMAIN_ARCHITECTURE_UID_KEY AS DOMAIN_ARCHITECTURE_UID_KEY
    FROM
      GENUS_PIVOT_NEIGHBOR_DOMAIN_COUNT_FINAL A
      INNER JOIN SITE_ONLY_DOMAIN_ARCHITECTURE B ON
        B.DOMAIN_ARCHITECTURE_UID_KEY = A.NEIGHBOR_DOMAIN_ARCHITECTURE_UID_KEY
      WHERE
        A.NEIGHBOR_TYPE = 'D'

completed in 0.08 seconds


CACHE TABLE DISCOVERED_SITE_ONLY_DOMAIN_ARCHITECTURE

completed in 1.85 seconds


SELECT
  COUNT(1) AS NUM_ROWS,
  COUNT(DISTINCT DOMAIN_ARCHITECTURE_UID_KEY) AS NUM_DISTINCT_SITE_ONLY_DAS
  FROM
    DISCOVERED_SITE_ONLY_DOMAIN_ARCHITECTURE

+--------+--------------------------+
|NUM_ROWS|NUM_DISTINCT_SITE_ONLY_DAS|
+--------+--------------------------+
|257     |257                       |
+--------+--------------------------+

completed in 0.64 seconds


SELECT *
  FROM
    DISCOVERED_SITE_ONLY_DOMAIN_ARCHITECTURE
    ORDER BY 1
    LIMIT 5

+--------------------------------+
|DOMAIN_ARCHITECTURE_UID_KEY     |
+--------------------------------+
|01562272dc3249f9e16efba899cfd555|
|033659ef6e8597ad66b3ee8f65ea7256|
|0514987356d95e91ad65298f0b4315e3|
|05b1400aa245f9a3c8c9ee2819442de1|
|096b13623cd09bdb8aadec066bf93212|
+--------------------------------+

completed in 0.15 seconds


DROP VIEW IF EXISTS PIVOT_SITE_ONLY_COUNT_BY_GENUS

completed in 0.01 seconds


CREATE VIEW PIVOT_SITE_ONLY_COUNT_BY_GENUS
  AS
  SELECT
    A.GENUS_NAME,
    COUNT(DISTINCT DOMAIN_ARCHITECTURE_UID_KEY) AS NUM_DISTINCT_SITE_ONLY_DAS
    FROM
      GENUS_PIVOT_NEIGHBOR_DOMAIN_COUNT_FINAL A
      INNER JOIN PIVOT_SITE_ONLY_DOMAIN_ARCHITECTURE B ON
        B.DOMAIN_ARCHITECTURE_UID_KEY = A.PIVOT_DOMAIN_ARCHITECTURE_UID_KEY
      WHERE
        A.NEIGHBOR_TYPE = 'P'
      GROUP BY
        A.GENUS_NAME

completed in 0.09 seconds


CACHE TABLE PIVOT_SITE_ONLY_COUNT_BY_GENUS

completed in 5.20 seconds


SELECT
  COUNT(1) AS NUM_ROWS,
  COUNT(DISTINCT GENUS_NAME) AS NUM_DISTINCT_GENERA
  FROM
    PIVOT_SITE_ONLY_COUNT_BY_GENUS

+--------+-------------------+
|NUM_ROWS|NUM_DISTINCT_GENERA|
+--------+-------------------+
|1289    |1289               |
+--------+-------------------+

completed in 0.65 seconds


SELECT *
  FROM
    PIVOT_SITE_ONLY_COUNT_BY_GENUS
    ORDER BY 2 DESC
    LIMIT 10

+--------------+--------------------------+
|GENUS_NAME    |NUM_DISTINCT_SITE_ONLY_DAS|
+--------------+--------------------------+
|chlamydia     |12                        |
|arthrobacter  |11                        |
|escherichia   |10                        |
|acinetobacter |9                         |
|microbacterium|9                         |
|pseudomonas   |9                         |
|mesorhizobium |9                         |
|streptomyces  |9                         |
|streptococcus |9                         |
|mycobacterium |9                         |
+--------------+--------------------------+

completed in 0.72 seconds


DROP VIEW IF EXISTS COPIVOT_SITE_ONLY_COUNT_BY_GENUS

completed in 0.01 seconds


CREATE VIEW COPIVOT_SITE_ONLY_COUNT_BY_GENUS
  AS
  SELECT
    A.GENUS_NAME,
    COUNT(DISTINCT DOMAIN_ARCHITECTURE_UID_KEY) AS NUM_DISTINCT_SITE_ONLY_DAS
    FROM
      GENUS_PIVOT_NEIGHBOR_DOMAIN_COUNT_FINAL A
      INNER JOIN COPIVOT_SITE_ONLY_DOMAIN_ARCHITECTURE B ON
        B.DOMAIN_ARCHITECTURE_UID_KEY = A.NEIGHBOR_DOMAIN_ARCHITECTURE_UID_KEY
      WHERE
        A.NEIGHBOR_TYPE = 'C'
      GROUP BY
        A.GENUS_NAME

completed in 0.08 seconds


CACHE TABLE COPIVOT_SITE_ONLY_COUNT_BY_GENUS

completed in 6.51 seconds


SELECT
  COUNT(1) AS NUM_ROWS,
  COUNT(DISTINCT GENUS_NAME) AS NUM_DISTINCT_GENERA
  FROM
    COPIVOT_SITE_ONLY_COUNT_BY_GENUS

+--------+-------------------+
|NUM_ROWS|NUM_DISTINCT_GENERA|
+--------+-------------------+
|1230    |1230               |
+--------+-------------------+

completed in 0.87 seconds


SELECT *
  FROM
    COPIVOT_SITE_ONLY_COUNT_BY_GENUS
    ORDER BY 2 DESC
    LIMIT 10

+--------------+--------------------------+
|GENUS_NAME    |NUM_DISTINCT_SITE_ONLY_DAS|
+--------------+--------------------------+
|escherichia   |10                        |
|chlamydia     |10                        |
|acinetobacter |9                         |
|arthrobacter  |9                         |
|pseudomonas   |9                         |
|streptococcus |9                         |
|microbacterium|9                         |
|salmonella    |8                         |
|enterobacter  |8                         |
|mesorhizobium |8                         |
+--------------+--------------------------+

completed in 0.62 seconds


DROP VIEW IF EXISTS DISCOVERED_SITE_ONLY_COUNT_BY_GENUS

completed in 0.01 seconds


CREATE VIEW DISCOVERED_SITE_ONLY_COUNT_BY_GENUS
  AS
  SELECT
    A.GENUS_NAME,
    COUNT(DISTINCT DOMAIN_ARCHITECTURE_UID_KEY) AS NUM_DISTINCT_SITE_ONLY_DAS
    FROM
      GENUS_PIVOT_NEIGHBOR_DOMAIN_COUNT_FINAL A
      INNER JOIN DISCOVERED_SITE_ONLY_DOMAIN_ARCHITECTURE B ON
        B.DOMAIN_ARCHITECTURE_UID_KEY = A.NEIGHBOR_DOMAIN_ARCHITECTURE_UID_KEY
      WHERE
        A.NEIGHBOR_TYPE = 'D'
      GROUP BY
        A.GENUS_NAME

completed in 0.08 seconds


CACHE TABLE DISCOVERED_SITE_ONLY_COUNT_BY_GENUS

completed in 5.20 seconds


SELECT
  COUNT(1) AS NUM_ROWS,
  COUNT(DISTINCT GENUS_NAME) AS NUM_DISTINCT_GENERA
  FROM
    DISCOVERED_SITE_ONLY_COUNT_BY_GENUS

+--------+-------------------+
|NUM_ROWS|NUM_DISTINCT_GENERA|
+--------+-------------------+
|1150    |1150               |
+--------+-------------------+

completed in 1.01 seconds


SELECT *
  FROM
    DISCOVERED_SITE_ONLY_COUNT_BY_GENUS
    ORDER BY 2 DESC
    LIMIT 10

+----------------------+--------------------------+
|GENUS_NAME            |NUM_DISTINCT_SITE_ONLY_DAS|
+----------------------+--------------------------+
|labilithrix           |20                        |
|streptomyces          |19                        |
|mesorhizobium         |18                        |
|pseudomonas           |16                        |
|clostridium           |15                        |
|candidatus viridilinea|15                        |
|paenibacillus         |13                        |
|archangium            |12                        |
|minicystis            |12                        |
|runella               |12                        |
+----------------------+--------------------------+

completed in 0.47 seconds


DROP VIEW IF EXISTS GENUS_DOMAIN_ARCHITECTURE_COUNT

completed in 0.43 seconds


CREATE VIEW GENUS_DOMAIN_ARCHITECTURE_COUNT
  AS
  SELECT
    GENUS_NAME,
    COUNT(DISTINCT NEIGHBOR_DOMAIN_ARCHITECTURE_UID_KEY) AS NUM_DISTINCT_DAS
    FROM
      GENUS_PIVOT_NEIGHBOR_DOMAIN_COUNT_FINAL
      GROUP BY
        GENUS_NAME

completed in 0.04 seconds


CACHE TABLE GENUS_DOMAIN_ARCHITECTURE_COUNT

completed in 24.81 seconds


SELECT
  COUNT(1) AS NUM_ROWS,
  COUNT(DISTINCT GENUS_NAME) AS NUM_DISTINCT_GENERA
  FROM
    GENUS_DOMAIN_ARCHITECTURE_COUNT

+--------+-------------------+
|NUM_ROWS|NUM_DISTINCT_GENERA|
+--------+-------------------+
|1400    |1400               |
+--------+-------------------+

completed in 0.59 seconds


SELECT *
  FROM
    GENUS_DOMAIN_ARCHITECTURE_COUNT
    ORDER BY 2 DESC
    LIMIT 10

+----------------------+----------------+
|GENUS_NAME            |NUM_DISTINCT_DAS|
+----------------------+----------------+
|streptomyces          |6697            |
|candidatus viridilinea|6439            |
|pseudomonas           |5988            |
|mesorhizobium         |5912            |
|paenibacillus         |5412            |
|bacillus              |5284            |
|clostridium           |4821            |
|escherichia           |4662            |
|sphingomonas          |4510            |
|acinetobacter         |4178            |
+----------------------+----------------+

completed in 0.59 seconds


DROP TABLE IF EXISTS GENUS_PCT_SITE_BASED

completed in 0.60 seconds


CREATE TABLE GENUS_PCT_SITE_BASED
  USING PARQUET
  AS
  SELECT DISTINCT
    A.GENUS_NAME,
    A.NUM_DISTINCT_DAS AS NUM_DISTINCT_DAS,
    CASE WHEN B.GENUS_NAME IS NULL
      THEN 0
      ELSE B.NUM_DISTINCT_SITE_ONLY_DAS
    END AS NUM_DISTINCT_SITE_ONLY_PIVOT_DAS,
    CASE WHEN C.GENUS_NAME IS NULL
      THEN 0
      ELSE C.NUM_DISTINCT_SITE_ONLY_DAS
    END AS NUM_DISTINCT_SITE_ONLY_COPIVOT_DAS,
    CASE WHEN D.GENUS_NAME IS NULL
      THEN 0
      ELSE D.NUM_DISTINCT_SITE_ONLY_DAS
    END AS NUM_DISTINCT_SITE_ONLY_DISCOVERED_DAS,
    CASE WHEN B.GENUS_NAME IS NULL
      THEN 0
      ELSE (B.NUM_DISTINCT_SITE_ONLY_DAS / A.NUM_DISTINCT_DAS) * 100.0
    END AS PCT_SITE_ONLY_PIVOTS,
    CASE WHEN C.GENUS_NAME IS NULL
      THEN 0
      ELSE (C.NUM_DISTINCT_SITE_ONLY_DAS / A.NUM_DISTINCT_DAS) * 100.0
    END AS PCT_SITE_ONLY_COPIVOTS,
    CASE WHEN D.GENUS_NAME IS NULL
      THEN 0
      ELSE (D.NUM_DISTINCT_SITE_ONLY_DAS / A.NUM_DISTINCT_DAS) * 100.0
    END AS PCT_SITE_ONLY_DISCOVERED
    FROM
      GENUS_DOMAIN_ARCHITECTURE_COUNT A
      LEFT JOIN PIVOT_SITE_ONLY_COUNT_BY_GENUS B ON
        B.GENUS_NAME = A.GENUS_NAME
      LEFT JOIN COPIVOT_SITE_ONLY_COUNT_BY_GENUS C ON
        C.GENUS_NAME = A.GENUS_NAME
      LEFT JOIN DISCOVERED_SITE_ONLY_COUNT_BY_GENUS D ON
        D.GENUS_NAME = A.GENUS_NAME

completed in 2.62 seconds


CACHE TABLE GENUS_PCT_SITE_BASED

completed in 0.50 seconds


SELECT
  COUNT(1) AS NUM_ROWS,
  COUNT(DISTINCT GENUS_NAME) AS NUM_DISTINCT_GENERA
  FROM
    GENUS_PCT_SITE_BASED

+--------+-------------------+
|NUM_ROWS|NUM_DISTINCT_GENERA|
+--------+-------------------+
|1400    |1400               |
+--------+-------------------+

completed in 1.12 seconds


SELECT *
  FROM
    GENUS_PCT_SITE_BASED
    LIMIT 10

+---------------+----------------+--------------------------------+----------------------------------+-------------------------------------+--------------------+----------------------+------------------------+
|GENUS_NAME     |NUM_DISTINCT_DAS|NUM_DISTINCT_SITE_ONLY_PIVOT_DAS|NUM_DISTINCT_SITE_ONLY_COPIVOT_DAS|NUM_DISTINCT_SITE_ONLY_DISCOVERED_DAS|PCT_SITE_ONLY_PIVOTS|PCT_SITE_ONLY_COPIVOTS|PCT_SITE_ONLY_DISCOVERED|
+---------------+----------------+--------------------------------+----------------------------------+-------------------------------------+--------------------+----------------------+------------------------+
|azoarcus       |2005            |6                               |5                                 |1                                    |0.29925187032418954 |0.24937655860349126   |0.04987531172069825     |
|empedobacter   |1023            |1                               |1                                 |3                                    |0.09775171065493646 |0.09775171065493646   |0.2932551319648094      |
|dokdonia       |892             |3                               |3                                 |0                                    |0.336322869955157   |0.336322869955157     |0.0                     |
|thiocystis     |1479            |1                               |1                                 |3                                    |0.0676132521974307  |0.0676132521974307    |0.2028397565922921      |
|planifilum     |1034            |1                               |1                                 |0                                    |0.09671179883945842 |0.09671179883945842   |0.0                     |
|planktomarina  |1255            |1                               |1                                 |1                                    |0.0796812749003984  |0.0796812749003984    |0.0796812749003984      |
|marvinbryantia |1256            |1                               |1                                 |5                                    |0.07961783439490447 |0.07961783439490447   |0.3980891719745223      |
|pelagibacterium|1435            |2                               |1                                 |1                                    |0.13937282229965156 |0.06968641114982578   |0.06968641114982578     |
|gloeocapsa     |1681            |3                               |3                                 |1                                    |0.1784651992861392  |0.1784651992861392    |0.0594883997620464      |
|desulfofundulus|979             |1                               |1                                 |0                                    |0.10214504596527069 |0.10214504596527069   |0.0                     |
+---------------+----------------+--------------------------------+----------------------------------+-------------------------------------+--------------------+----------------------+------------------------+

completed in 0.26 seconds


DROP VIEW DISCOVERED_SITE_ONLY_COUNT_BY_GENUS

completed in 0.13 seconds


DROP VIEW COPIVOT_SITE_ONLY_COUNT_BY_GENUS

completed in 0.10 seconds


DROP VIEW PIVOT_SITE_ONLY_COUNT_BY_GENUS

completed in 0.10 seconds


DROP VIEW DISCOVERED_SITE_ONLY_DOMAIN_ARCHITECTURE

completed in 0.09 seconds


DROP VIEW COPIVOT_SITE_ONLY_DOMAIN_ARCHITECTURE

completed in 0.08 seconds


DROP VIEW PIVOT_SITE_ONLY_DOMAIN_ARCHITECTURE

completed in 0.08 seconds


DROP VIEW SITE_ONLY_DOMAIN_ARCHITECTURE

completed in 0.08 seconds


real	1m38.944s
user	11m11.733s
sys	4m41.950s
```

### Data Export

To export the final data table run the following:

```
./spark-submit.sh export.py --stmt "
SELECT *
  FROM
    GENUS_PCT_SITE_BASED
    ORDER BY 1" --path outputs/virulence_prediction_genus_pct_site_based.csv
```

OUTPUT

```
exported 1400 records

real	0m18.252s
user	1m16.567s
sys	0m15.716s
```
