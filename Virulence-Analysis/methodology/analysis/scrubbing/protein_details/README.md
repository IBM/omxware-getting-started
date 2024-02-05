# PROTEIN_DETAILS

[back to parent](../README.md)

Run the following to scrub the data into the finalized form:

```
./spark-sql.sh --sql-file sql/scrubbing/protein_details.sql
```

OUTPUT

```sql
CACHE TABLE GENOME_PROTEIN

completed in 88.36 seconds


CACHE TABLE PROTEIN_DETAILS_STAGING

completed in 8.65 seconds


DROP TABLE IF EXISTS PROTEIN_DETAILS

completed in 1.14 seconds


CREATE TABLE PROTEIN_DETAILS
  USING PARQUET
  AS
  SELECT
    A.PROTEIN_UID_KEY,
    A.PROTEIN_FULLNAME
    FROM
      PROTEIN_DETAILS_STAGING A
      INNER JOIN GENOME_PROTEIN B ON
        B.PROTEIN_UID_KEY = A.PROTEIN_UID_KEY
      GROUP BY
        A.PROTEIN_UID_KEY,
        A.PROTEIN_FULLNAME

completed in 204.73 seconds


CACHE TABLE PROTEIN_DETAILS

completed in 6.43 seconds


SELECT
  COUNT(1) AS NUM_ROWS,
  COUNT(DISTINCT PROTEIN_UID_KEY) AS NUM_DISTINCT_PROTEINS,
  COUNT(DISTINCT PROTEIN_FULLNAME) AS NUM_DISTINCT_NAMES
  FROM
    PROTEIN_DETAILS

+--------+---------------------+------------------+
|NUM_ROWS|NUM_DISTINCT_PROTEINS|NUM_DISTINCT_NAMES|
+--------+---------------------+------------------+
|54791224|53836264             |21477             |
+--------+---------------------+------------------+

completed in 71.86 seconds


SELECT *
  FROM
    PROTEIN_DETAILS
    ORDER BY 1
    LIMIT 10

+--------------------------------+-----------------------------------------------------------+
|PROTEIN_UID_KEY                 |PROTEIN_FULLNAME                                           |
+--------------------------------+-----------------------------------------------------------+
|00000083b5cacb61de38fc94dffce1b9|RNA 3'-terminal phosphate cyclase                          |
|000000a0d302ea52f960668fbd97db14|hypothetical protein                                       |
|0000014592ca08d8b1385e32822f14ba|Galactokinase                                              |
|000001deccb2cbc508ab56ebb3bfd4ae|hypothetical protein                                       |
|000001fe24dcdeae5bfc92cdbb032272|hypothetical protein                                       |
|0000023d20f1083c64ab6521e706885b|hypothetical protein                                       |
|0000024f5e8585b0fb8fc86a668cd551|2,3-bisphosphoglycerate-independent phosphoglycerate mutase|
|0000026c595f02fcecc2e5caab86f0e6|hypothetical protein                                       |
|00000292ca4881130b0708d9d69c60ff|hypothetical protein                                       |
|00000294cb2541b38500ef597b37c1ea|hypothetical protein                                       |
+--------------------------------+-----------------------------------------------------------+

completed in 0.98 seconds


DROP TABLE PROTEIN_DETAILS_STAGING

completed in 0.13 seconds


real	6m31.906s
user	92m37.990s
sys	9m58.103s
```
