# PROTEIN_DOMAIN_ARCHITECTURE

This table provides a flattened representation of the table IPR_PROTEIN. The table collects all IPR accessions related to a protein, sorts them in lexical order and computes a MD5 hash for easier comparison. We call this collection of IPR accessions the domain architecture of a protein.

Run the following to create the table:

`./spark-sql.sh --sql-file sql/base/similarity/protein_domain_architecture.sql`

OUTPUT

```sql
CACHE TABLE IPR_PROTEIN

completed in 21.92 seconds


DROP TABLE IF EXISTS PROTEIN_DOMAIN_ARCHITECTURE

completed in 0.86 seconds


CREATE TABLE PROTEIN_DOMAIN_ARCHITECTURE
  USING PARQUET
  AS
  SELECT
    PROTEIN_UID_KEY,
    MD5(ARRAY_JOIN(DOMAIN_ARCHITECTURE, '~')) AS DOMAIN_ARCHITECTURE_UID_KEY,
    DOMAIN_ARCHITECTURE,
    SIZE(DOMAIN_ARCHITECTURE) AS FUNCTION_COUNT
    FROM
      (SELECT
        PROTEIN_UID_KEY,
        ARRAY_SORT(COLLECT_SET(IPR_ACCESSION)) AS DOMAIN_ARCHITECTURE
        FROM
          IPR_PROTEIN
          GROUP BY
            PROTEIN_UID_KEY)

completed in 177.61 seconds


SELECT
  COUNT(1) AS NUM_ROWS,
  COUNT(DISTINCT PROTEIN_UID_KEY) AS NUM_DISTINCT_PROTEINS,
  COUNT(DISTINCT DOMAIN_ARCHITECTURE_UID_KEY) AS NUM_DISTINCT_ARCHITECTURES,
  MIN(FUNCTION_COUNT) AS MIN_FUNCTION_COUNT,
  MAX(FUNCTION_COUNT) AS MAX_FUNCTION_COUNT
  FROM
    PROTEIN_DOMAIN_ARCHITECTURE

+--------+---------------------+--------------------------+------------------+------------------+
|NUM_ROWS|NUM_DISTINCT_PROTEINS|NUM_DISTINCT_ARCHITECTURES|MIN_FUNCTION_COUNT|MAX_FUNCTION_COUNT|
+--------+---------------------+--------------------------+------------------+------------------+
|42942941|42942941             |298649                    |1                 |124               |
+--------+---------------------+--------------------------+------------------+------------------+

completed in 86.57 seconds


SELECT
  PROTEIN_UID_KEY,
  DOMAIN_ARCHITECTURE_UID_KEY,
  DOMAIN_ARCHITECTURE,
  FUNCTION_COUNT
  FROM
    PROTEIN_DOMAIN_ARCHITECTURE
    ORDER BY 1, 2
    LIMIT 10

+--------------------------------+--------------------------------+------------------------------------------------------------------+--------------+
|PROTEIN_UID_KEY                 |DOMAIN_ARCHITECTURE_UID_KEY     |DOMAIN_ARCHITECTURE                                               |FUNCTION_COUNT|
+--------------------------------+--------------------------------+------------------------------------------------------------------+--------------+
|00000083b5cacb61de38fc94dffce1b9|30130dc48540340d0bc2c32d4e6d106b|[IPR000228, IPR013792, IPR017770, IPR023797, IPR036553, IPR037136]|6             |
|0000014592ca08d8b1385e32822f14ba|f1703f2fcab8b17465e33c9760baa9fb|[IPR006204, IPR006205, IPR013750, IPR014721, IPR020568, IPR036554]|6             |
|000001deccb2cbc508ab56ebb3bfd4ae|47148ebe4532f4c8330fc07221307890|[IPR011990]                                                       |1             |
|0000024f5e8585b0fb8fc86a668cd551|05ea3c93af2e06d957d457e22007e173|[IPR005995, IPR006124, IPR011258, IPR017849, IPR017850, IPR036646]|6             |
|000002e3b0d3f405d984bd1ee95d7fd1|d87cd64eadede5003dd78450994c0570|[IPR017946, IPR032075]                                            |2             |
|000003ac77101b5457b901e0b1fdc162|c971361eab931d5c5e7f40d1c4b8b99a|[IPR003352, IPR003501, IPR004718, IPR013011, IPR013014, IPR036095]|6             |
|000003df427df668c7e76e073ae7e0d1|d3abc4d7472d3b0344a8518de746d9ea|[IPR023895]                                                       |1             |
|000003eaea0da746af019b6242794c84|7390749b2626d000d6141acf9e0f3526|[IPR016161, IPR016162]                                            |2             |
|0000040804f857233b8a9784340f81b5|c77e12cbca66c46045e782cd0c3cb04d|[IPR004360, IPR029068, IPR037523]                                 |3             |
|0000042d95d5614a54616fc565987ede|9ed60a088188ecdba7905c2704772665|[IPR007272]                                                       |1             |
+--------------------------------+--------------------------------+------------------------------------------------------------------+--------------+

completed in 3.83 seconds


real  4m58.982s
user  65m20.525s
sys  9m48.103s
```
