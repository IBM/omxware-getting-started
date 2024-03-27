# Virulence Summary Statistics

[back to parent](/Virulence-Analysis/methodology/analysis/README.md)

* [Standout Discoveries](#standout-discoveries)
* [Export Standout Discoveries](#export-standout-discoveries)
* [Export Standout Discoveries Protein](#export-standout-discoveries-protein)
* [Export Standout Discoveries IPR](#export-standout-discoveries-ipr)
* [Genus Standout Discoveries](#genus-standout-discoveries)
* [Export Genus Standout Discoveries](#export-genus-standout-discoveries)
* [Export Genus Standout Discoveries Protein](#export-genus-standout-discoveries-protein)
* [Export Genus Standout Discoveries IPR](#export-genus-standout-discoveries-ipr)
* [Protein CoPivot Frequency](#pivot-copivot-frequency)
* [Export Protein CoPivot Frequency](#export-pivot-copivot-frequency)
* [Protein Discovery Frequency](#pivot-discovery-frequency)
* [Export Protein Discovery Frequency](#export-pivot-discovery-frequency)
* [Genome Basic Stats](#genome-basic-stats)
* [Export Genome Basic Stats](#export-genome-basic-stats)
* [After Needle Analysis](#after-needle-analysis)

- Q1 Which virulence discoveries standout by count (top 25 across all organisms)? What are the protein names associated
  with these?
    - Q1a For the high occurring discoveries, do they occur with a diversity of virulence factors (pivots)?
    - Q1b For the newly discovered proteins occurring with low diversity pivots (consistently occurring D-P pairs), is
      there a diversity of function (IPR codes) indicating functional dependence?
        - Q1b1 For the neighbors, can you identify that the neighbors are regulatory in nature (and expected)? Or
          related to excretion?
- Q2 For all discovered domain architectures, what has the highest count for each genera (top 50)? Map those to GO terms
  for enriched pathways. What are the protein names associated with these?
    - Q2a Are there discovered DAs unique to genera?
    - Q2b Are there discovered DAs that are present across multiple genera?
- Q3 Which IPR codes occur in the most discovered DAs?
- Q4 What are the most frequent pairs of pivot and co-pivots?
- Q5 What are the most frequent pairs of pivot and discoveries?
- Q6 Basic stats by genome of counts: Total virulence factors per genome, Total discoveries per genome, Total co-pivots
  per genome

### Standout Discoveries

[back to top](#virulence-summary-statistics)

Which virulence discoveries standout by count (top 25 across all organisms)? What are the protein names associated with
these?

- For the high occurring discoveries, do they occur with a diversity of virulence factors (pivots)
  ? [see](#pivot-discovery-frequency)

```
./spark-sql.sh --sql-file sql/core/standout_discoveries.sql
```

OUTPUT

```sql
CACHE TABLE GENUS_PIVOT_NEIGHBOR_DOMAIN_COUNT_FINAL

completed in 11.56 seconds


CACHE TABLE DOMAIN_ARCHITECTURE

completed in 1.07 seconds


CACHE TABLE PROTEIN_DETAILS

completed in 6.82 seconds


CACHE TABLE PROTEIN_DOMAIN_ARCHITECTURE

completed in 7.78 seconds


DROP TABLE IF EXISTS STANDOUT_DISCOVERIES

completed in 0.95 seconds


CREATE TABLE STANDOUT_DISCOVERIES
  USING PARQUET
  AS
  SELECT
    NEIGHBOR_DOMAIN_ARCHITECTURE_UID_KEY,
    SUM(COUNT) AS COUNT
    FROM
      GENUS_PIVOT_NEIGHBOR_DOMAIN_COUNT_FINAL
      WHERE
        NEIGHBOR_TYPE = 'D'
      GROUP BY
        NEIGHBOR_DOMAIN_ARCHITECTURE_UID_KEY

completed in 7.51 seconds


CACHE TABLE STANDOUT_DISCOVERIES

completed in 0.27 seconds


SELECT
  COUNT(1) AS NUM_ROWS,
  COUNT(DISTINCT NEIGHBOR_DOMAIN_ARCHITECTURE_UID_KEY) AS NUM_DISTINCT_DISCOVERIES
  FROM
    STANDOUT_DISCOVERIES

+--------+------------------------+
|NUM_ROWS|NUM_DISTINCT_DISCOVERIES|
+--------+------------------------+
|80060   |80060                   |
+--------+------------------------+

completed in 0.87 seconds


SELECT *
  FROM
    STANDOUT_DISCOVERIES
    ORDER BY 2 DESC
    LIMIT 10

+------------------------------------+-------+
|NEIGHBOR_DOMAIN_ARCHITECTURE_UID_KEY|COUNT  |
+------------------------------------+-------+
|4b58d855c73735c23b4f62b426bedb43    |1154173|
|adf1d782feb2b6ffaa030589820ab368    |1144597|
|30daa1c6925b9d2b904fb50fd701a48f    |1100654|
|8266b4a355c253c96bbfe9f9ad576698    |1046140|
|a9cc37b399c2fd1ba92118ec4de9c9b1    |932544 |
|52afd54482e6a62475c81deec2390977    |870966 |
|e3c65e05f187e091444c66ff99a91677    |850473 |
|5288c5a0422fbe93f8b2c083b7fb4b1b    |822672 |
|82cb6dbfe53ec92ba2fe3230d971b29d    |671042 |
|1324500941f3b11abf67db7bf35fda84    |651469 |
+------------------------------------+-------+

completed in 0.24 seconds


DROP TABLE IF EXISTS STANDOUT_DISCOVERIES_PROTEIN

completed in 0.47 seconds


CREATE TABLE STANDOUT_DISCOVERIES_PROTEIN
  USING PARQUET
  AS
  SELECT
    A.NEIGHBOR_DOMAIN_ARCHITECTURE_UID_KEY,
    C.PROTEIN_FULLNAME
    FROM
      STANDOUT_DISCOVERIES A
      INNER JOIN PROTEIN_DOMAIN_ARCHITECTURE B ON
        B.DOMAIN_ARCHITECTURE_UID_KEY = A.NEIGHBOR_DOMAIN_ARCHITECTURE_UID_KEY
      INNER JOIN PROTEIN_DETAILS C ON
        C.PROTEIN_UID_KEY = B.PROTEIN_UID_KEY
      GROUP BY
        A.NEIGHBOR_DOMAIN_ARCHITECTURE_UID_KEY,
        C.PROTEIN_FULLNAME

completed in 26.04 seconds


CACHE TABLE STANDOUT_DISCOVERIES_PROTEIN

completed in 0.27 seconds


SELECT
  COUNT(1) AS NUM_ROWS,
  COUNT(DISTINCT NEIGHBOR_DOMAIN_ARCHITECTURE_UID_KEY) AS NUM_DISTINCT_DISCOVERIES,
  COUNT(DISTINCT PROTEIN_FULLNAME) AS NUM_DISTINCT_PROTEIN_NAMES
  FROM
    STANDOUT_DISCOVERIES_PROTEIN

+--------+------------------------+--------------------------+
|NUM_ROWS|NUM_DISTINCT_DISCOVERIES|NUM_DISTINCT_PROTEIN_NAMES|
+--------+------------------------+--------------------------+
|235822  |80060                   |19980                     |
+--------+------------------------+--------------------------+

completed in 2.94 seconds


SELECT *
  FROM
    STANDOUT_DISCOVERIES_PROTEIN
    ORDER BY 1, 2
    LIMIT 10

+------------------------------------+----------------------------------------+
|NEIGHBOR_DOMAIN_ARCHITECTURE_UID_KEY|PROTEIN_FULLNAME                        |
+------------------------------------+----------------------------------------+
|0000a7023bfbe4296d3f2b4434ba81c7    |Alginate lyase 7                        |
|0000a7023bfbe4296d3f2b4434ba81c7    |Bifunctional hemolysin/adenylate cyclase|
|0000a7023bfbe4296d3f2b4434ba81c7    |Endo-1,3-1,4-beta-glycanase ExsH        |
|0000a7023bfbe4296d3f2b4434ba81c7    |Hemolysin, chromosomal                  |
|0000a7023bfbe4296d3f2b4434ba81c7    |Hemolysin, plasmid                      |
|0000a7023bfbe4296d3f2b4434ba81c7    |Leukotoxin                              |
|0000a7023bfbe4296d3f2b4434ba81c7    |Lipase                                  |
|0000a7023bfbe4296d3f2b4434ba81c7    |Mannuronan C5-epimerase AlgE5           |
|0000a7023bfbe4296d3f2b4434ba81c7    |Nodulation protein O                    |
|0000a7023bfbe4296d3f2b4434ba81c7    |Poly(beta-D-mannuronate) C5 epimerase 1 |
+------------------------------------+----------------------------------------+

completed in 0.12 seconds


DROP TABLE IF EXISTS STANDOUT_DISCOVERIES_IPR

completed in 0.03 seconds


CREATE TABLE STANDOUT_DISCOVERIES_IPR
  USING PARQUET
  AS
  SELECT
    A.NEIGHBOR_DOMAIN_ARCHITECTURE_UID_KEY,
    EXPLODE(B.DOMAIN_ARCHITECTURE) AS IPR
    FROM
      STANDOUT_DISCOVERIES A
      INNER JOIN DOMAIN_ARCHITECTURE B ON
        B.DOMAIN_ARCHITECTURE_UID_KEY = A.NEIGHBOR_DOMAIN_ARCHITECTURE_UID_KEY
      GROUP BY
        A.NEIGHBOR_DOMAIN_ARCHITECTURE_UID_KEY,
        2

completed in 3.00 seconds


CACHE TABLE STANDOUT_DISCOVERIES_IPR

completed in 0.24 seconds


SELECT
  COUNT(1) AS NUM_ROWS,
  COUNT(DISTINCT NEIGHBOR_DOMAIN_ARCHITECTURE_UID_KEY) AS NUM_DISTINCT_DISCOVERIES,
  COUNT(DISTINCT IPR) AS NUM_DISTINCT_IPRS
  FROM
    STANDOUT_DISCOVERIES_IPR

+--------+------------------------+-----------------+
|NUM_ROWS|NUM_DISTINCT_DISCOVERIES|NUM_DISTINCT_IPRS|
+--------+------------------------+-----------------+
|458416  |80060                   |17914            |
+--------+------------------------+-----------------+

completed in 0.70 seconds


SELECT *
  FROM
    STANDOUT_DISCOVERIES_IPR
    ORDER BY 1, 2
    LIMIT 10

+------------------------------------+---------+
|NEIGHBOR_DOMAIN_ARCHITECTURE_UID_KEY|IPR      |
+------------------------------------+---------+
|0000a7023bfbe4296d3f2b4434ba81c7    |IPR011049|
|0000a7023bfbe4296d3f2b4434ba81c7    |IPR018511|
|00023a8ff256a14320934386e5776a23    |IPR000709|
|00023a8ff256a14320934386e5776a23    |IPR006311|
|00023a8ff256a14320934386e5776a23    |IPR028081|
|00023a8ff256a14320934386e5776a23    |IPR028082|
|00025eb807f10e45215a07f6dd90379a    |IPR007210|
|00025eb807f10e45215a07f6dd90379a    |IPR017783|
|0002837e100d61f5a338728964985c08    |IPR000711|
|0002837e100d61f5a338728964985c08    |IPR005749|
+------------------------------------+---------+

completed in 0.16 seconds


real	1m20.545s
user	18m1.622s
sys	4m48.279s
```

### Export Standout Discoveries

[back to top](#virulence-summary-statistics)

```
./spark-submit.sh export.py --stmt "
SELECT *
  FROM
    STANDOUT_DISCOVERIES
" --path outputs/standout_discoveries.csv
```

OUTPUT

```
exported 80060 records

real	0m15.164s
user	0m56.825s
sys	0m7.892s
```

[virulence_prediction_standout_discoveries.csv.gz](https://precision.fda.gov/home/files/file-Gj1Z7480ZqJfKYZK0ZB3qXxz-2)

### Export Standout Discoveries Protein

[back to top](#virulence-summary-statistics)

```
./spark-submit.sh export.py --stmt "
SELECT *
  FROM
    STANDOUT_DISCOVERIES_PROTEIN
" --path outputs/standout_discoveries_protein.csv
```

OUTPUT

```
exported 235822 records

real	0m14.252s
user	1m4.161s
sys	0m9.456s
```

[virulence_prediction_standout_discoveries_protein.csv.gz](https://precision.fda.gov/home/files/file-Gj1Z7F00ZqJQb7KFB99Vqxk4-2)

### Export Standout Discoveries IPR

[back to top](#virulence-summary-statistics)

```
./spark-submit.sh export.py --stmt "
SELECT *
  FROM
    STANDOUT_DISCOVERIES_IPR
" --path outputs/standout_discoveries_ipr.csv
```

OUTPUT

```
exported 458416 records

real	0m13.739s
user	0m47.773s
sys	0m6.583s
```

[virulence_prediction_standout_discoveries_ipr.csv.gz](https://precision.fda.gov/home/files/file-Gj1Z76Q0ZqJv3Jj6Kq8x3kFp-2)

### Genus Standout Discoveries

[back to top](#virulence-summary-statistics)

For all discovered domain architectures, what has the highest count for each genera (top 50)? Map those to GO terms
for enriched pathways. What are the protein names associated with these?

```
./spark-sql.sh --sql-file sql/core/genus_standout_discoveries.sql
```

OUTPUT

```sql
CACHE TABLE GENUS_PIVOT_NEIGHBOR_DOMAIN_COUNT_FINAL

completed in 11.69 seconds


CACHE TABLE DOMAIN_ARCHITECTURE

completed in 1.21 seconds


CACHE TABLE PROTEIN_DETAILS

completed in 6.58 seconds


CACHE TABLE PROTEIN_DOMAIN_ARCHITECTURE

completed in 8.22 seconds


DROP TABLE IF EXISTS GENUS_STANDOUT_DISCOVERIES

completed in 1.03 seconds


CREATE TABLE GENUS_STANDOUT_DISCOVERIES
  USING PARQUET
  AS
  SELECT
    GENUS_NAME,
    NEIGHBOR_DOMAIN_ARCHITECTURE_UID_KEY,
    SUM(COUNT) AS COUNT
    FROM
      GENUS_PIVOT_NEIGHBOR_DOMAIN_COUNT_FINAL
      WHERE
        NEIGHBOR_TYPE = 'D'
      GROUP BY
        GENUS_NAME,
        NEIGHBOR_DOMAIN_ARCHITECTURE_UID_KEY

completed in 7.81 seconds


CACHE TABLE GENUS_STANDOUT_DISCOVERIES

completed in 0.48 seconds


SELECT
  COUNT(1) AS NUM_ROWS,
  COUNT(DISTINCT GENUS_NAME) AS NUM_DISTINCT_GENERA,
  COUNT(DISTINCT NEIGHBOR_DOMAIN_ARCHITECTURE_UID_KEY) AS NUM_DISTINCT_DISCOVERIES
  FROM
    GENUS_STANDOUT_DISCOVERIES

+--------+-------------------+------------------------+
|NUM_ROWS|NUM_DISTINCT_GENERA|NUM_DISTINCT_DISCOVERIES|
+--------+-------------------+------------------------+
|1404878 |1400               |80060                   |
+--------+-------------------+------------------------+

completed in 3.57 seconds


SELECT *
  FROM
    GENUS_STANDOUT_DISCOVERIES
    ORDER BY 2 DESC
    LIMIT 10

+-------------------+------------------------------------+-----+
|GENUS_NAME         |NEIGHBOR_DOMAIN_ARCHITECTURE_UID_KEY|COUNT|
+-------------------+------------------------------------+-----+
|desulfatibacillum  |ffffcd5631cac9590d12c8bbe8da9b36    |4    |
|desulfobacterium   |ffffcd5631cac9590d12c8bbe8da9b36    |2    |
|acidovorax         |fffeadb0fed1f9fcd6d5b99b07a4d460    |16   |
|alicycliphilus     |fffeadb0fed1f9fcd6d5b99b07a4d460    |3    |
|haloactinobacterium|fffe23743386b51518a705389a8bb658    |4    |
|bordetella         |fffda9c648a61f0e4d60856958b52ddb    |3040 |
|fluviicola         |fffd35ef58f12dadad65fd77bd356945    |2    |
|panacibacter       |fffd35ef58f12dadad65fd77bd356945    |2    |
|lutibacter         |fffd35ef58f12dadad65fd77bd356945    |2    |
|limnochorda        |fffc94c27669bbce82b71730d513980b    |2    |
+-------------------+------------------------------------+-----+

completed in 0.40 seconds


DROP VIEW IF EXISTS PROTEIN_NAME_DOMAIN_ARCHITECTURE

completed in 0.02 seconds


CREATE VIEW PROTEIN_NAME_DOMAIN_ARCHITECTURE
  AS
  SELECT
    A.DOMAIN_ARCHITECTURE_UID_KEY,
    B.PROTEIN_FULLNAME
    FROM
      PROTEIN_DOMAIN_ARCHITECTURE A
      INNER JOIN PROTEIN_DETAILS B ON
        B.PROTEIN_UID_KEY = A.PROTEIN_UID_KEY
      GROUP BY
        A.DOMAIN_ARCHITECTURE_UID_KEY,
        B.PROTEIN_FULLNAME

completed in 0.10 seconds


CACHE TABLE PROTEIN_NAME_DOMAIN_ARCHITECTURE

completed in 34.48 seconds


DROP TABLE IF EXISTS GENUS_STANDOUT_DISCOVERIES_PROTEIN

completed in 0.45 seconds


CREATE TABLE GENUS_STANDOUT_DISCOVERIES_PROTEIN
  USING PARQUET
  AS
  SELECT
    B.GENUS_NAME,
    B.NEIGHBOR_DOMAIN_ARCHITECTURE_UID_KEY,
    A.PROTEIN_FULLNAME
    FROM
      PROTEIN_NAME_DOMAIN_ARCHITECTURE A
      INNER JOIN GENUS_STANDOUT_DISCOVERIES B ON
        B.NEIGHBOR_DOMAIN_ARCHITECTURE_UID_KEY = A.DOMAIN_ARCHITECTURE_UID_KEY
      GROUP BY
        B.GENUS_NAME,
        B.NEIGHBOR_DOMAIN_ARCHITECTURE_UID_KEY,
        A.PROTEIN_FULLNAME

completed in 18.26 seconds


CACHE TABLE GENUS_STANDOUT_DISCOVERIES_PROTEIN

completed in 1.66 seconds


SELECT
  COUNT(1) AS NUM_ROWS,
  COUNT(DISTINCT GENUS_NAME) AS NUM_DISTINCT_GENERA,
  COUNT(DISTINCT NEIGHBOR_DOMAIN_ARCHITECTURE_UID_KEY) AS NUM_DISTINCT_DISCOVERIES,
  COUNT(DISTINCT PROTEIN_FULLNAME) AS NUM_DISTINCT_PROTEIN_NAMES
  FROM
    GENUS_STANDOUT_DISCOVERIES_PROTEIN

+--------+-------------------+------------------------+--------------------------+
|NUM_ROWS|NUM_DISTINCT_GENERA|NUM_DISTINCT_DISCOVERIES|NUM_DISTINCT_PROTEIN_NAMES|
+--------+-------------------+------------------------+--------------------------+
|13503357|1400               |80060                   |19980                     |
+--------+-------------------+------------------------+--------------------------+

completed in 1.93 seconds


SELECT *
  FROM
    GENUS_STANDOUT_DISCOVERIES_PROTEIN
    ORDER BY 1, 2, 3
    LIMIT 10

+-----------+------------------------------------+-----------------------------------------------------+
|GENUS_NAME |NEIGHBOR_DOMAIN_ARCHITECTURE_UID_KEY|PROTEIN_FULLNAME                                     |
+-----------+------------------------------------+-----------------------------------------------------+
|abiotrophia|0115db492510494cd1394a89aaa10643    |Alpha-galactosidase                                  |
|abiotrophia|0115db492510494cd1394a89aaa10643    |Alpha-galactosidase AgaA                             |
|abiotrophia|0115db492510494cd1394a89aaa10643    |Alpha-galactosidase Mel36A                           |
|abiotrophia|0115db492510494cd1394a89aaa10643    |Bifunctional alpha-galactosidase/sucrose kinase AgaSK|
|abiotrophia|024c4b4853e5b26a611ff99e10ad1d6a    |ECF RNA polymerase sigma factor EcfG                 |
|abiotrophia|024c4b4853e5b26a611ff99e10ad1d6a    |ECF RNA polymerase sigma factor SigC                 |
|abiotrophia|024c4b4853e5b26a611ff99e10ad1d6a    |ECF RNA polymerase sigma factor SigK                 |
|abiotrophia|024c4b4853e5b26a611ff99e10ad1d6a    |ECF RNA polymerase sigma factor SigM                 |
|abiotrophia|024c4b4853e5b26a611ff99e10ad1d6a    |ECF RNA polymerase sigma factor SigR                 |
|abiotrophia|024c4b4853e5b26a611ff99e10ad1d6a    |ECF RNA polymerase sigma factor SigW                 |
+-----------+------------------------------------+-----------------------------------------------------+

completed in 0.41 seconds


DROP VIEW PROTEIN_NAME_DOMAIN_ARCHITECTURE

completed in 0.13 seconds


DROP TABLE IF EXISTS GENUS_STANDOUT_DISCOVERIES_IPR

completed in 0.01 seconds


CREATE TABLE GENUS_STANDOUT_DISCOVERIES_IPR
  USING PARQUET
  AS
  SELECT
    A.GENUS_NAME,
    A.NEIGHBOR_DOMAIN_ARCHITECTURE_UID_KEY,
    EXPLODE(B.DOMAIN_ARCHITECTURE) AS IPR
    FROM
      GENUS_STANDOUT_DISCOVERIES A
      INNER JOIN DOMAIN_ARCHITECTURE B ON
        B.DOMAIN_ARCHITECTURE_UID_KEY = A.NEIGHBOR_DOMAIN_ARCHITECTURE_UID_KEY
      GROUP BY
        A.GENUS_NAME,
        A.NEIGHBOR_DOMAIN_ARCHITECTURE_UID_KEY,
        3

completed in 7.41 seconds


CACHE TABLE GENUS_STANDOUT_DISCOVERIES_IPR

completed in 0.54 seconds


SELECT
  COUNT(1) AS NUM_ROWS,
  COUNT(DISTINCT GENUS_NAME) AS NUM_DISTINCT_GENERA,
  COUNT(DISTINCT NEIGHBOR_DOMAIN_ARCHITECTURE_UID_KEY) AS NUM_DISTINCT_DISCOVERIES,
  COUNT(DISTINCT IPR) AS NUM_DISTINCT_IPRS
  FROM
    GENUS_STANDOUT_DISCOVERIES_IPR

+--------+-------------------+------------------------+-----------------+
|NUM_ROWS|NUM_DISTINCT_GENERA|NUM_DISTINCT_DISCOVERIES|NUM_DISTINCT_IPRS|
+--------+-------------------+------------------------+-----------------+
|5185807 |1400               |80060                   |17914            |
+--------+-------------------+------------------------+-----------------+

completed in 1.62 seconds


SELECT *
  FROM
    GENUS_STANDOUT_DISCOVERIES_IPR
    ORDER BY 1, 2, 3
    LIMIT 10

+-----------+------------------------------------+---------+
|GENUS_NAME |NEIGHBOR_DOMAIN_ARCHITECTURE_UID_KEY|IPR      |
+-----------+------------------------------------+---------+
|abiotrophia|0115db492510494cd1394a89aaa10643    |IPR000111|
|abiotrophia|0115db492510494cd1394a89aaa10643    |IPR002252|
|abiotrophia|0115db492510494cd1394a89aaa10643    |IPR013785|
|abiotrophia|0115db492510494cd1394a89aaa10643    |IPR017853|
|abiotrophia|0115db492510494cd1394a89aaa10643    |IPR031704|
|abiotrophia|0115db492510494cd1394a89aaa10643    |IPR031705|
|abiotrophia|0115db492510494cd1394a89aaa10643    |IPR038417|
|abiotrophia|024c4b4853e5b26a611ff99e10ad1d6a    |IPR013325|
|abiotrophia|026146e74a968b6c0a94265b6512098f    |IPR000352|
|abiotrophia|026146e74a968b6c0a94265b6512098f    |IPR004374|
+-----------+------------------------------------+---------+

completed in 0.12 seconds


real	1m59.557s
user	22m40.605s
sys	6m29.461s
```

### Export Genus Standout Discoveries

[back to top](#virulence-summary-statistics)

```
./spark-submit.sh export.py --stmt "
SELECT *
  FROM
    GENUS_STANDOUT_DISCOVERIES
" --path outputs/genus_standout_discoveries.csv
```

OUTPUT

```
exported 1404878 records

real	0m16.749s
user	1m13.298s
sys	0m10.220s
```

[virulence_prediction_genus_standout_discoveries.csv.gz](https://precision.fda.gov/home/files/file-Gj1Z6KQ0ZqJgZ14yv9xByKxF-2)

### Export Genus Standout Discoveries Protein

[back to top](#virulence-summary-statistics)

```
./spark-submit.sh export.py --stmt "
SELECT *
  FROM
    GENUS_STANDOUT_DISCOVERIES_PROTEIN
" --path outputs/genus_standout_discoveries_protein.csv
```

OUTPUT

```
exported 13503357 records

real	0m16.805s
user	1m35.247s
sys	0m14.983s
```

[virulence_prediction_genus_standout_discoveries_protein.csv.gz](https://precision.fda.gov/home/files/file-Gj1Z6Z80ZqJbvKV4BzbxQBgf-2)

### Export Genus Standout Discoveries IPR

[back to top](#virulence-summary-statistics)

```
./spark-submit.sh export.py --stmt "
SELECT *
  FROM
    GENUS_STANDOUT_DISCOVERIES_IPR
" --path outputs/genus_standout_discoveries_ipr.csv
```

OUTPUT

```
exported 5185807 records

real	0m16.312s
user	1m27.120s
sys	0m11.226s
```

[virulence_prediction_genus_standout_discoveries_ipr.csv.gz](https://precision.fda.gov/home/files/file-Gj1Z6Vj0ZqJpQ770FG6BjvVX-2)

### Pivot CoPivot Frequency

[back to top](#virulence-summary-statistics)

What are the most frequent pairs of pivot and co-pivots?

```
./spark-sql.sh --sql-file sql/core/pivot_copivot_freq_summary.sql
```

OUTPUT

```sql
CACHE TABLE GENUS_PIVOT_NEIGHBOR_DOMAIN_COUNT_FINAL

completed in 10.97 seconds


DROP TABLE IF EXISTS PIVOT_COPIVOT_FREQUENCY

completed in 0.06 seconds


CREATE TABLE PIVOT_COPIVOT_FREQUENCY
  USING PARQUET
  AS
  SELECT
    PIVOT_DOMAIN_ARCHITECTURE_UID_KEY,
    NEIGHBOR_DOMAIN_ARCHITECTURE_UID_KEY,
    SUM(COUNT) AS COUNT
    FROM
      GENUS_PIVOT_NEIGHBOR_DOMAIN_COUNT_FINAL
      WHERE
        NEIGHBOR_TYPE = 'C'
      GROUP BY
        PIVOT_DOMAIN_ARCHITECTURE_UID_KEY,
        NEIGHBOR_DOMAIN_ARCHITECTURE_UID_KEY

completed in 10.60 seconds


CACHE TABLE PIVOT_COPIVOT_FREQUENCY

completed in 0.47 seconds


SELECT
  COUNT(1) AS NUM_ROWS,
  COUNT(DISTINCT PIVOT_DOMAIN_ARCHITECTURE_UID_KEY) AS NUM_DISTINCT_PIVOTS,
  COUNT(DISTINCT NEIGHBOR_DOMAIN_ARCHITECTURE_UID_KEY) AS NUM_DISTINCT_COPIVOTS
  FROM
    PIVOT_COPIVOT_FREQUENCY

+--------+-------------------+---------------------+
|NUM_ROWS|NUM_DISTINCT_PIVOTS|NUM_DISTINCT_COPIVOTS|
+--------+-------------------+---------------------+
|542828  |2577               |2577                 |
+--------+-------------------+---------------------+

completed in 3.89 seconds


SELECT *
  FROM
    PIVOT_COPIVOT_FREQUENCY
    ORDER BY 1, 2
    LIMIT 10

+---------------------------------+------------------------------------+-----+
|PIVOT_DOMAIN_ARCHITECTURE_UID_KEY|NEIGHBOR_DOMAIN_ARCHITECTURE_UID_KEY|COUNT|
+---------------------------------+------------------------------------+-----+
|000e97918ef5156f91e7b45faccb8a34 |000e97918ef5156f91e7b45faccb8a34    |4136 |
|000e97918ef5156f91e7b45faccb8a34 |00c15f2eb1af4226843af9938222952f    |6    |
|000e97918ef5156f91e7b45faccb8a34 |0447501765781eaeae56e6f29f5b0f84    |1    |
|000e97918ef5156f91e7b45faccb8a34 |07485fa4d667263ec01aac4e778019c4    |6    |
|000e97918ef5156f91e7b45faccb8a34 |090423f93efa59c92a3ada0b170792de    |1    |
|000e97918ef5156f91e7b45faccb8a34 |0906897c2ea5d51cbc8a8cc6dba3d1fd    |67   |
|000e97918ef5156f91e7b45faccb8a34 |0914ee268a846778a4c083938e49a664    |10   |
|000e97918ef5156f91e7b45faccb8a34 |0a003644ce1b1692d5ea6f3f30aa8012    |6    |
|000e97918ef5156f91e7b45faccb8a34 |0a1682303cdc6ea0e5adcadbee86563e    |5    |
|000e97918ef5156f91e7b45faccb8a34 |0ba0c466bc547dc0ae7f98ec35900957    |4    |
+---------------------------------+------------------------------------+-----+

completed in 0.32 seconds


real	0m33.145s
user	4m54.260s
sys	1m30.171s
```

### Export Pivot CoPivot Frequency

[back to top](#virulence-summary-statistics)

```
./spark-submit.sh export.py --stmt "
SELECT *
  FROM
    PIVOT_COPIVOT_FREQUENCY
" --path outputs/pivot_copivot_frequency.csv
```

OUTPUT

```
exported 542828 records

real	0m16.976s
user	1m11.177s
sys	0m9.414s
```

[virulence_prediction_pivot_copivot_frequency.csv.gz](https://precision.fda.gov/home/files/file-Gj1Z6pQ0ZqJq9XvB7vV2q4kf-2)

### Pivot Discovery Frequency

[back to top](#virulence-summary-statistics)

What are the most frequent pairs of pivot and discoveries?

```
./spark-sql.sh --sql-file sql/core/pivot_discovery_freq_summary.sql
```

OUTPUT

```sql
CACHE TABLE GENUS_PIVOT_NEIGHBOR_DOMAIN_COUNT_FINAL

completed in 12.20 seconds


DROP TABLE IF EXISTS PIVOT_DISCOVERY_FREQUENCY

completed in 0.05 seconds


CREATE TABLE PIVOT_DISCOVERY_FREQUENCY
  USING PARQUET
  AS
  SELECT
    PIVOT_DOMAIN_ARCHITECTURE_UID_KEY,
    NEIGHBOR_DOMAIN_ARCHITECTURE_UID_KEY,
    SUM(COUNT) AS COUNT
    FROM
      GENUS_PIVOT_NEIGHBOR_DOMAIN_COUNT_FINAL
      WHERE
        NEIGHBOR_TYPE = 'D'
      GROUP BY
        PIVOT_DOMAIN_ARCHITECTURE_UID_KEY,
        NEIGHBOR_DOMAIN_ARCHITECTURE_UID_KEY

completed in 11.58 seconds


CACHE TABLE PIVOT_DISCOVERY_FREQUENCY

completed in 0.56 seconds


SELECT
  COUNT(1) AS NUM_ROWS,
  COUNT(DISTINCT PIVOT_DOMAIN_ARCHITECTURE_UID_KEY) AS NUM_DISTINCT_PIVOTS,
  COUNT(DISTINCT NEIGHBOR_DOMAIN_ARCHITECTURE_UID_KEY) AS NUM_DISTINCT_DISCOVERYS
  FROM
    PIVOT_DISCOVERY_FREQUENCY

+--------+-------------------+-----------------------+
|NUM_ROWS|NUM_DISTINCT_PIVOTS|NUM_DISTINCT_DISCOVERYS|
+--------+-------------------+-----------------------+
|999628  |2308               |80060                  |
+--------+-------------------+-----------------------+

completed in 2.96 seconds


SELECT *
  FROM
    PIVOT_DISCOVERY_FREQUENCY
    ORDER BY 1, 2
    LIMIT 10

+---------------------------------+------------------------------------+-----+
|PIVOT_DOMAIN_ARCHITECTURE_UID_KEY|NEIGHBOR_DOMAIN_ARCHITECTURE_UID_KEY|COUNT|
+---------------------------------+------------------------------------+-----+
|000e97918ef5156f91e7b45faccb8a34 |00d2480106c37050779a7d5e1f261ad5    |77637|
|000e97918ef5156f91e7b45faccb8a34 |011f04ba0866c7545bd09e9547c536cd    |6    |
|000e97918ef5156f91e7b45faccb8a34 |018ced3ccfe98bd86ad813668c4d600d    |1    |
|000e97918ef5156f91e7b45faccb8a34 |0289005a9c3e51541964f7a3c11e1d31    |2    |
|000e97918ef5156f91e7b45faccb8a34 |0296a3c20c7bae5655535160f4ef7015    |10   |
|000e97918ef5156f91e7b45faccb8a34 |032787ac70f007581422e79bf06ea38a    |2    |
|000e97918ef5156f91e7b45faccb8a34 |033bd1747065ed9b48629b1f1a44267f    |3    |
|000e97918ef5156f91e7b45faccb8a34 |03e18239af7232a42a9f42520d34e36d    |25   |
|000e97918ef5156f91e7b45faccb8a34 |03f2c3b1c7ab5d7423c9799f863ac013    |6    |
|000e97918ef5156f91e7b45faccb8a34 |046d53169bf0367a4ea5850558b7350a    |1    |
+---------------------------------+------------------------------------+-----+

completed in 0.48 seconds


real	0m35.143s
user	5m40.954s
sys	1m20.112s
```

### Export Pivot Discovery Frequency

[back to top](#virulence-summary-statistics)

```
./spark-submit.sh export.py --stmt "
SELECT *
  FROM
    PIVOT_DISCOVERY_FREQUENCY
" --path outputs/pivot_discovery_frequency.csv
```

OUTPUT

```
exported 999628 records

real	0m16.021s
user	1m9.344s
sys	0m9.867s
```

[virulence_prediction_pivot_discovery_frequency.csv.gz](https://precision.fda.gov/home/files/file-Gj1Z6x80ZqJQ9bkpYz11zv8J-2)

### Genome Basic Stats

[back to top](#virulence-summary-statistics)

What are the basic stats by genome of counts: Total pivot per genome, Total discoveries per genome, Total co-pivots per
genome.

```
./spark-sql.sh --sql-file sql/core/genome_basic_stats.sql
```

OUTPUT

```sql
CACHE TABLE GENOME_PIVOT_NEIGHBOR_DOMAIN_COUNT_FINAL

completed in 86.37 seconds


DROP TABLE IF EXISTS GENOME_BASIC_STATS

completed in 1.06 seconds


CREATE TABLE GENOME_BASIC_STATS
  USING PARQUET
  AS
  SELECT
    ACCESSION_NUMBER,
    NEIGHBOR_TYPE,
    SUM(COUNT) AS COUNT
    FROM
      GENOME_PIVOT_NEIGHBOR_DOMAIN_COUNT_FINAL
      GROUP BY
        ACCESSION_NUMBER,
        NEIGHBOR_TYPE

completed in 33.97 seconds


CACHE TABLE GENOME_BASIC_STATS

completed in 0.54 seconds


SELECT
  COUNT(1) AS NUM_ROWS,
  COUNT(DISTINCT ACCESSION_NUMBER) AS NUM_DISTINCT_GENOMES,
  COUNT(DISTINCT NEIGHBOR_TYPE) AS NUM_DISTINCT_TYPES
  FROM
    GENOME_BASIC_STATS

+--------+--------------------+------------------+
|NUM_ROWS|NUM_DISTINCT_GENOMES|NUM_DISTINCT_TYPES|
+--------+--------------------+------------------+
|619481  |206573              |3                 |
+--------+--------------------+------------------+

completed in 2.55 seconds


SELECT *
  FROM
    GENOME_BASIC_STATS
    ORDER BY 1, 2
    LIMIT 10

+----------------+-------------+-----+
|ACCESSION_NUMBER|NEIGHBOR_TYPE|COUNT|
+----------------+-------------+-----+
|DRR000852       |C            |960  |
|DRR000852       |D            |1748 |
|DRR000852       |P            |756  |
|DRR001171       |C            |2270 |
|DRR001171       |D            |2776 |
|DRR001171       |P            |1529 |
|DRR014268       |C            |430  |
|DRR014268       |D            |794  |
|DRR014268       |P            |396  |
|DRR014269       |C            |452  |
+----------------+-------------+-----+

completed in 0.32 seconds


real	2m14.039s
user	57m20.349s
sys	6m55.109s
```

### Export Genome Basic Stats

[back to top](#virulence-summary-statistics)

```
./spark-submit.sh export.py --stmt "
SELECT *
  FROM
    GENOME_BASIC_STATS
" --path outputs/genome_basic_stats.csv
```

OUTPUT

```
exported 619481 records

real	0m16.575s
user	1m8.997s
sys	0m9.527s
```

[virulence_prediction_genome_basic_stats.csv.gz](https://precision.fda.gov/home/files/file-Gj1Z67Q0ZqJpQ770FG6BjvQf-2)

### After Needle Analysis

[back to top](#virulence-summary-statistics)

```
After Needle Analysis:
Number of Distinct Pivot DAS: 2599
Number of Distinct Neighbor DAS: 82659
Number of Distinct Pivot DAS NEIGHBOR_TYPE = 'D': 2308
Number of Distinct Neighbor DAS NEIGHBOR_TYPE = 'D': 80060
Number of Distinct Pivot Proteins: 11144804
Number of Distinct Neighbor Proteins: 27423496
Number of Distinct Pivot Proteins NEIGHBOR_TYPE = 'D': 11127574
Number of Distinct Neighbor Proteins NEIGHBOR_TYPE = 'D': 16278692
```

```sql
-- 2599
SELECT
    COUNT(DISTINCT PIVOT_DOMAIN_ARCHITECTURE_UID_KEY)
    FROM
        GENOME_PIVOT_NEIGHBOR_DOMAIN_COUNT_FINAL

-- 82659
SELECT
    COUNT(DISTINCT NEIGHBOR_DOMAIN_ARCHITECTURE_UID_KEY)
    FROM
        GENOME_PIVOT_NEIGHBOR_DOMAIN_COUNT_FINAL
        
-- 11144804
SELECT
    COUNT(DISTINCT PIVOT_PROTEIN_UID_KEY)
    FROM
        GENOME_PIVOT_NEIGHBOR_PROTEIN_DOMAIN
        WHERE
            PIVOT_DOMAIN_ARCHITECTURE_UID_KEY IN 
                (SELECT
                    PIVOT_DOMAIN_ARCHITECTURE_UID_KEY
                    FROM
                        GENOME_PIVOT_NEIGHBOR_DOMAIN_COUNT_FINAL
                        GROUP BY
                            PIVOT_DOMAIN_ARCHITECTURE_UID_KEY)
                            
-- 27423496
SELECT
    COUNT(DISTINCT NEIGHBOR_PROTEIN_UID_KEY)
    FROM
        GENOME_PIVOT_NEIGHBOR_PROTEIN_DOMAIN
        WHERE
            NEIGHBOR_DOMAIN_ARCHITECTURE_UID_KEY IN 
                (SELECT
                    NEIGHBOR_DOMAIN_ARCHITECTURE_UID_KEY
                    FROM
                        GENOME_PIVOT_NEIGHBOR_DOMAIN_COUNT_FINAL
                        GROUP BY
                            NEIGHBOR_DOMAIN_ARCHITECTURE_UID_KEY)
                            
-- 11127574
SELECT
    COUNT(DISTINCT PIVOT_PROTEIN_UID_KEY)
    FROM
        GENOME_PIVOT_NEIGHBOR_PROTEIN_DOMAIN
        WHERE
            PIVOT_DOMAIN_ARCHITECTURE_UID_KEY IN 
                (SELECT
                    PIVOT_DOMAIN_ARCHITECTURE_UID_KEY
                    FROM
                        GENOME_PIVOT_NEIGHBOR_DOMAIN_COUNT_FINAL
                        WHERE
                            NEIGHBOR_TYPE = 'D'
                        GROUP BY
                            PIVOT_DOMAIN_ARCHITECTURE_UID_KEY)
                            
-- 16278692
SELECT
    COUNT(DISTINCT NEIGHBOR_PROTEIN_UID_KEY)
    FROM
        GENOME_PIVOT_NEIGHBOR_PROTEIN_DOMAIN
        WHERE
            NEIGHBOR_DOMAIN_ARCHITECTURE_UID_KEY IN 
                (SELECT
                    NEIGHBOR_DOMAIN_ARCHITECTURE_UID_KEY
                    FROM
                        GENOME_PIVOT_NEIGHBOR_DOMAIN_COUNT_FINAL
                        WHERE
                            NEIGHBOR_TYPE = 'D'
                        GROUP BY
                            NEIGHBOR_DOMAIN_ARCHITECTURE_UID_KEY)
                            
-- 2308
SELECT
    COUNT(DISTINCT PIVOT_DOMAIN_ARCHITECTURE_UID_KEY)
    FROM
        GENOME_PIVOT_NEIGHBOR_DOMAIN_COUNT_FINAL
        WHERE
            NEIGHBOR_TYPE = 'D'
            
-- 80060
SELECT
    COUNT(DISTINCT NEIGHBOR_DOMAIN_ARCHITECTURE_UID_KEY)
    FROM
        GENOME_PIVOT_NEIGHBOR_DOMAIN_COUNT_FINAL
        WHERE
            NEIGHBOR_TYPE = 'D'
```

