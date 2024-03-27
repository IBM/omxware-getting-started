# Domain Architecture

Records the unique set of IPR codes for each protein as an ordered list constructed from the original IPR_PROTEIN table from FGP. The DOMAIN_ARCHITECTURE table records these unique sets, the counts of the types, and represents the records with an MD5 hash of the set. The architectures are crossed referenced with their associated proteins via PROTEIN_DOMAIN_ARCHITECTURE.

[back to parent](/Virulence-Analysis/methodology/analysis/README.md)

* [Table Creation](#table-creation)
* [Data Export](#data-export)

Exported file is located at [viruence_prediction_domain_architecture.csv.gz](https://precision.fda.gov/home/files/file-Gj1Z5x00ZqJf0G38JbzG1xqz-2)

### Table Creation

Run the following to create the data:

```
./spark-sql.sh --sql-file sql/core/domain_architecture.sql --udf-mods udfs
```

OUTPUT

```sql
CACHE TABLE IPR

completed in 8.78 seconds


CACHE TABLE IPR_PROTEIN

completed in 15.98 seconds


DROP TABLE IF EXISTS PROTEIN_IPR_TYPE_COUNT

completed in 1.09 seconds


CREATE TABLE PROTEIN_IPR_TYPE_COUNT
  USING PARQUET
  AS
  SELECT
    PROTEIN_UID_KEY,
    SUM(ACTIVE_SITE) AS NUM_ACTIVE_SITE,
    SUM(BINDING_SITE) AS NUM_BINDING_SITE,
    SUM(CONSERVED_SITE) AS NUM_CONSERVED_SITE,
    SUM(DOMAIN) AS NUM_DOMAIN,
    SUM(FAMILY) AS NUM_FAMILY,
    SUM(HOMOLOGOUS_SUPERFAMILY) AS NUM_HOMOLOGOUS_SUPERFAMILY,
    SUM(PTM) AS NUM_PTM,
    SUM(REPEAT) AS NUM_REPEAT
    FROM
      (SELECT
        B.PROTEIN_UID_KEY,
        CASE WHEN A.TYPE = 'ACTIVE_SITE' THEN 1 ELSE 0 END AS ACTIVE_SITE,
        CASE WHEN A.TYPE = 'BINDING_SITE' THEN 1 ELSE 0 END AS BINDING_SITE,
        CASE WHEN A.TYPE = 'CONSERVED_SITE' THEN 1 ELSE 0 END AS CONSERVED_SITE,
        CASE WHEN A.TYPE = 'DOMAIN' THEN 1 ELSE 0 END AS DOMAIN,
        CASE WHEN A.TYPE = 'FAMILY' THEN 1 ELSE 0 END AS FAMILY,
        CASE WHEN A.TYPE = 'HOMOLOGOUS_SUPERFAMILY' THEN 1 ELSE 0 END AS HOMOLOGOUS_SUPERFAMILY,
        CASE WHEN A.TYPE = 'PTM' THEN 1 ELSE 0 END AS PTM,
        CASE WHEN A.TYPE = 'REPEAT' THEN 1 ELSE 0 END AS REPEAT
        FROM
          IPR A
          INNER JOIN IPR_PROTEIN B ON
            B.IPR_ACCESSION = A.IPR_ACCESSION)
      GROUP BY
        PROTEIN_UID_KEY

completed in 26.92 seconds


CACHE TABLE PROTEIN_IPR_TYPE_COUNT

completed in 6.04 seconds


SELECT
  COUNT(1) AS NUM_ROWS,
  COUNT(DISTINCT PROTEIN_UID_KEY) AS NUM_DISTINCT_PROTEINS
  FROM
    PROTEIN_IPR_TYPE_COUNT

+--------+---------------------+
|NUM_ROWS|NUM_DISTINCT_PROTEINS|
+--------+---------------------+
|42724008|42724008             |
+--------+---------------------+

completed in 35.94 seconds


SELECT *
  FROM
    PROTEIN_IPR_TYPE_COUNT
    ORDER BY 1
    LIMIT 10

+--------------------------------+---------------+----------------+------------------+----------+----------+--------------------------+-------+----------+
|PROTEIN_UID_KEY                 |NUM_ACTIVE_SITE|NUM_BINDING_SITE|NUM_CONSERVED_SITE|NUM_DOMAIN|NUM_FAMILY|NUM_HOMOLOGOUS_SUPERFAMILY|NUM_PTM|NUM_REPEAT|
+--------------------------------+---------------+----------------+------------------+----------+----------+--------------------------+-------+----------+
|00000083b5cacb61de38fc94dffce1b9|0              |0               |0                 |1         |2         |3                         |0      |0         |
|0000014592ca08d8b1385e32822f14ba|0              |0               |0                 |2         |1         |3                         |0      |0         |
|000001deccb2cbc508ab56ebb3bfd4ae|0              |0               |0                 |0         |0         |1                         |0      |0         |
|0000024f5e8585b0fb8fc86a668cd551|0              |0               |0                 |2         |1         |3                         |0      |0         |
|000002e3b0d3f405d984bd1ee95d7fd1|0              |0               |0                 |0         |1         |1                         |0      |0         |
|000003ac77101b5457b901e0b1fdc162|0              |0               |0                 |5         |0         |1                         |0      |0         |
|000003df427df668c7e76e073ae7e0d1|0              |0               |0                 |0         |1         |0                         |0      |0         |
|000003eaea0da746af019b6242794c84|0              |0               |0                 |0         |0         |2                         |0      |0         |
|0000040804f857233b8a9784340f81b5|0              |0               |0                 |2         |0         |1                         |0      |0         |
|0000042d95d5614a54616fc565987ede|0              |0               |0                 |1         |0         |0                         |0      |0         |
+--------------------------------+---------------+----------------+------------------+----------+----------+--------------------------+-------+----------+

completed in 0.88 seconds


DROP TABLE IF EXISTS PROTEIN_IPR_ARRAY

completed in 0.43 seconds


CREATE TABLE PROTEIN_IPR_ARRAY
  USING PARQUET
  AS
  SELECT
    PROTEIN_UID_KEY,
    ARRAY_SORT(COLLECT_SET(IPR_ACCESSION)) AS DOMAIN_ARCHITECTURE
    FROM
      IPR_PROTEIN
      GROUP BY
        PROTEIN_UID_KEY

completed in 66.50 seconds


CACHE TABLE PROTEIN_IPR_ARRAY

completed in 5.08 seconds


SELECT
  COUNT(1) AS NUM_ROWS,
  COUNT(DISTINCT PROTEIN_UID_KEY) AS NUM_DISTINCT_PROTEINS
  FROM
    PROTEIN_IPR_ARRAY

+--------+---------------------+
|NUM_ROWS|NUM_DISTINCT_PROTEINS|
+--------+---------------------+
|42724008|42724008             |
+--------+---------------------+

completed in 8.55 seconds


SELECT *
  FROM
    PROTEIN_IPR_ARRAY
    ORDER BY 1
    LIMIT 5

+--------------------------------+------------------------------------------------------------------+
|PROTEIN_UID_KEY                 |DOMAIN_ARCHITECTURE                                               |
+--------------------------------+------------------------------------------------------------------+
|00000083b5cacb61de38fc94dffce1b9|[IPR000228, IPR013792, IPR017770, IPR023797, IPR036553, IPR037136]|
|0000014592ca08d8b1385e32822f14ba|[IPR006204, IPR006205, IPR013750, IPR014721, IPR020568, IPR036554]|
|000001deccb2cbc508ab56ebb3bfd4ae|[IPR011990]                                                       |
|0000024f5e8585b0fb8fc86a668cd551|[IPR005995, IPR006124, IPR011258, IPR017849, IPR017850, IPR036646]|
|000002e3b0d3f405d984bd1ee95d7fd1|[IPR017946, IPR032075]                                            |
+--------------------------------+------------------------------------------------------------------+

completed in 0.58 seconds


DROP TABLE IF EXISTS DOMAIN_ARCHITECTURE

completed in 0.43 seconds


CREATE TABLE DOMAIN_ARCHITECTURE
  USING PARQUET
  AS
  SELECT DISTINCT
    MD5(ARRAY_JOIN(DOMAIN_ARCHITECTURE, '~')) AS DOMAIN_ARCHITECTURE_UID_KEY,
    NUM_ACTIVE_SITE,
    NUM_BINDING_SITE,
    NUM_CONSERVED_SITE,
    NUM_DOMAIN,
    NUM_FAMILY,
    NUM_HOMOLOGOUS_SUPERFAMILY,
    NUM_PTM,
    NUM_REPEAT,
    SIZE(DOMAIN_ARCHITECTURE) AS FUNCTION_COUNT,
    DOMAIN_ARCHITECTURE
    FROM
      PROTEIN_IPR_ARRAY A
      INNER JOIN PROTEIN_IPR_TYPE_COUNT B ON
        B.PROTEIN_UID_KEY = A.PROTEIN_UID_KEY

completed in 111.54 seconds


CACHE TABLE DOMAIN_ARCHITECTURE

completed in 0.43 seconds


SELECT
  COUNT(1) AS NUM_ROWS,
  COUNT(DISTINCT DOMAIN_ARCHITECTURE_UID_KEY) AS NUM_DISTINCT_DAS,
  MIN(FUNCTION_COUNT) AS MIN_DA_SIZE,
  MAX(FUNCTION_COUNT) AS MAX_DA_SIZE,
  MEAN(FUNCTION_COUNT) AS MEAN_DA_SIZE,
  MEDIAN(COLLECT_LIST(FUNCTION_COUNT)) AS MEDIAN_DA_SIZE,
  MODE(COLLECT_LIST(FUNCTION_COUNT)) AS MODE_DA_SIZE,
  STDDEV_POP(FUNCTION_COUNT) AS STDDEV_DA_SIZE
  FROM
    DOMAIN_ARCHITECTURE

+--------+----------------+-----------+-----------+-----------------+--------------+------------+-----------------+
|NUM_ROWS|NUM_DISTINCT_DAS|MIN_DA_SIZE|MAX_DA_SIZE|MEAN_DA_SIZE     |MEDIAN_DA_SIZE|MODE_DA_SIZE|STDDEV_DA_SIZE   |
+--------+----------------+-----------+-----------+-----------------+--------------+------------+-----------------+
|297004  |297004          |1          |124        |7.605621473111473|5.0           |3.0         |8.872779230766643|
+--------+----------------+-----------+-----------+-----------------+--------------+------------+-----------------+

completed in 4.83 seconds


SELECT *
  FROM
    DOMAIN_ARCHITECTURE
    ORDER BY 1
    LIMIT 5

+--------------------------------+---------------+----------------+------------------+----------+----------+--------------------------+-------+----------+--------------+-------------------------------------------------------------------------------------------------------------------------+
|DOMAIN_ARCHITECTURE_UID_KEY     |NUM_ACTIVE_SITE|NUM_BINDING_SITE|NUM_CONSERVED_SITE|NUM_DOMAIN|NUM_FAMILY|NUM_HOMOLOGOUS_SUPERFAMILY|NUM_PTM|NUM_REPEAT|FUNCTION_COUNT|DOMAIN_ARCHITECTURE                                                                                                      |
+--------------------------------+---------------+----------------+------------------+----------+----------+--------------------------+-------+----------+--------------+-------------------------------------------------------------------------------------------------------------------------+
|000046223dd2b18cec017249a28d499f|0              |0               |0                 |0         |0         |2                         |0      |0         |2             |[IPR014729, IPR037914]                                                                                                   |
|00008344a49ecd9711f74b5a917a881b|0              |0               |0                 |7         |0         |4                         |0      |0         |11            |[IPR001650, IPR004042, IPR004365, IPR004860, IPR006142, IPR011545, IPR012340, IPR014001, IPR027417, IPR027434, IPR036844]|
|0000a7023bfbe4296d3f2b4434ba81c7|0              |0               |1                 |0         |0         |1                         |0      |0         |2             |[IPR011049, IPR018511]                                                                                                   |
|0000afac6eb9500ec4142e2b787c990f|0              |0               |0                 |1         |0         |2                         |0      |0         |3             |[IPR003891, IPR016021, IPR016024]                                                                                        |
|0000ed6143cbd780acb64eded12e9250|0              |0               |0                 |2         |0         |0                         |0      |0         |2             |[IPR001296, IPR011017]                                                                                                   |
+--------------------------------+---------------+----------------+------------------+----------+----------+--------------------------+-------+----------+--------------+-------------------------------------------------------------------------------------------------------------------------+

completed in 0.24 seconds


DROP TABLE IF EXISTS PROTEIN_DOMAIN_ARCHITECTURE

completed in 0.03 seconds


CREATE TABLE PROTEIN_DOMAIN_ARCHITECTURE
  USING PARQUET
  AS
  SELECT
    PROTEIN_UID_KEY,
    MD5(ARRAY_JOIN(DOMAIN_ARCHITECTURE, '~')) AS DOMAIN_ARCHITECTURE_UID_KEY
    FROM
      PROTEIN_IPR_ARRAY

completed in 42.58 seconds


CACHE TABLE PROTEIN_DOMAIN_ARCHITECTURE

completed in 5.53 seconds


SELECT
  COUNT(1) AS NUM_ROWS,
  COUNT(DISTINCT PROTEIN_UID_KEY) AS NUM_DISTINCT_PROTEINS,
  COUNT(DISTINCT DOMAIN_ARCHITECTURE_UID_KEY) AS NUM_DISTINCT_DAS
  FROM
    PROTEIN_DOMAIN_ARCHITECTURE

+--------+---------------------+----------------+
|NUM_ROWS|NUM_DISTINCT_PROTEINS|NUM_DISTINCT_DAS|
+--------+---------------------+----------------+
|42724008|42724008             |297004          |
+--------+---------------------+----------------+

completed in 67.70 seconds


SELECT *
  FROM
    PROTEIN_DOMAIN_ARCHITECTURE
    ORDER BY 1, 2
    LIMIT 10

+--------------------------------+--------------------------------+
|PROTEIN_UID_KEY                 |DOMAIN_ARCHITECTURE_UID_KEY     |
+--------------------------------+--------------------------------+
|00000083b5cacb61de38fc94dffce1b9|30130dc48540340d0bc2c32d4e6d106b|
|0000014592ca08d8b1385e32822f14ba|f1703f2fcab8b17465e33c9760baa9fb|
|000001deccb2cbc508ab56ebb3bfd4ae|47148ebe4532f4c8330fc07221307890|
|0000024f5e8585b0fb8fc86a668cd551|05ea3c93af2e06d957d457e22007e173|
|000002e3b0d3f405d984bd1ee95d7fd1|d87cd64eadede5003dd78450994c0570|
|000003ac77101b5457b901e0b1fdc162|c971361eab931d5c5e7f40d1c4b8b99a|
|000003df427df668c7e76e073ae7e0d1|d3abc4d7472d3b0344a8518de746d9ea|
|000003eaea0da746af019b6242794c84|7390749b2626d000d6141acf9e0f3526|
|0000040804f857233b8a9784340f81b5|c77e12cbca66c46045e782cd0c3cb04d|
|0000042d95d5614a54616fc565987ede|9ed60a088188ecdba7905c2704772665|
+--------------------------------+--------------------------------+

completed in 0.67 seconds


DROP TABLE PROTEIN_IPR_TYPE_COUNT

completed in 0.39 seconds


DROP TABLE PROTEIN_IPR_ARRAY

completed in 0.41 seconds


real	7m6.012s
user	71m48.539s
sys	10m38.350s
```

### Data Export

To export the final data table run the following:

```
./spark-submit.sh export.py --stmt "
SELECT
  DOMAIN_ARCHITECTURE_UID_KEY,
  NUM_ACTIVE_SITE,
  NUM_BINDING_SITE,
  NUM_CONSERVED_SITE,
  NUM_DOMAIN,
  NUM_FAMILY,
  NUM_HOMOLOGOUS_SUPERFAMILY,
  NUM_PTM,
  NUM_REPEAT,
  FUNCTION_COUNT,
  ARRAY_JOIN(DOMAIN_ARCHITECTURE, '~') AS DOMAIN_ARCHITECTURE
  FROM
    DOMAIN_ARCHITECTURE
    ORDER BY 1
" --path outputs/viruence_prediction_domain_architecture.csv
```

OUTPUT

```
exported 297004 records

real	0m19.496s
user	1m47.551s
sys	0m18.675s
```
