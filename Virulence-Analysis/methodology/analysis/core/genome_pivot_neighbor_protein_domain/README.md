# Genome Pivot Neighbor Protien Domain

This table is an extension of GENOME_PIVOT_NEIGHBOR_PROTEIN with the addition of pivot and neighbor domain architectures. Note that some NEIGHBOR_DOMAIN_ARCHITECTURE_UID_KEY in this table can be NULL. This is the case for proteins that are neighbors and have no defined domain architecture (IPR_PROTEIN) data.

[back to parent](/Virulence-Analysis/methodology/analysis/README.md)

Run the following to create the data:

```
./spark-sql.sh --sql-file sql/core/genome_pivot_neighbor_protein_domain.sql
```

OUTPUT

```sql
CACHE TABLE GENOME_PIVOT_NEIGHBOR_PROTEIN

completed in 123.13 seconds


CACHE TABLE PROTEIN_DOMAIN_ARCHITECTURE

completed in 5.57 seconds


DROP TABLE IF EXISTS GENOME_PIVOT_NEIGHBOR_PROTEIN_DOMAIN

completed in 1.64 seconds


CREATE TABLE GENOME_PIVOT_NEIGHBOR_PROTEIN_DOMAIN
  USING PARQUET
  AS
  SELECT
    A.ACCESSION_NUMBER,
    A.PIVOT_PROTEIN_UID_KEY,
    B.DOMAIN_ARCHITECTURE_UID_KEY AS PIVOT_DOMAIN_ARCHITECTURE_UID_KEY,
    A.NEIGHBOR_PROTEIN_UID_KEY,
    C.DOMAIN_ARCHITECTURE_UID_KEY AS NEIGHBOR_DOMAIN_ARCHITECTURE_UID_KEY,
    A.PIVOT_LOCUS,
    A.NEIGHBOR_LOCUS,
    A.NORMALIZED_LOCUS,
    A.NEIGHBOR_TYPE
    FROM
      GENOME_PIVOT_NEIGHBOR_PROTEIN A
      INNER JOIN PROTEIN_DOMAIN_ARCHITECTURE B ON
        B.PROTEIN_UID_KEY = A.PIVOT_PROTEIN_UID_KEY
      LEFT JOIN PROTEIN_DOMAIN_ARCHITECTURE C ON
        C.PROTEIN_UID_KEY = A.NEIGHBOR_PROTEIN_UID_KEY
      GROUP BY
        A.ACCESSION_NUMBER,
        A.PIVOT_PROTEIN_UID_KEY,
        B.DOMAIN_ARCHITECTURE_UID_KEY,
        A.NEIGHBOR_PROTEIN_UID_KEY,
        C.DOMAIN_ARCHITECTURE_UID_KEY,
        A.PIVOT_LOCUS,
        A.NEIGHBOR_LOCUS,
        A.NORMALIZED_LOCUS,
        A.NEIGHBOR_TYPE

completed in 1697.18 seconds


CACHE TABLE GENOME_PIVOT_NEIGHBOR_PROTEIN_DOMAIN

completed in 162.80 seconds


SELECT
  COUNT(1) AS NUM_ROWS,
  COUNT(DISTINCT ACCESSION_NUMBER) AS NUM_DISTINCT_GENOMES,
  COUNT(DISTINCT PIVOT_PROTEIN_UID_KEY) AS NUM_DISTINCT_PIVOT_PROTEINS,
  COUNT(DISTINCT PIVOT_DOMAIN_ARCHITECTURE_UID_KEY) AS NUM_DISTINCT_PIVOT_DAS,
  COUNT(DISTINCT NEIGHBOR_PROTEIN_UID_KEY) AS NUM_DISTINCT_NEIGHBOR_PROTEINS,
  COUNT(DISTINCT NEIGHBOR_DOMAIN_ARCHITECTURE_UID_KEY) AS NUM_DISTINCT_NEIGHBOR_DAS
  FROM
    GENOME_PIVOT_NEIGHBOR_PROTEIN_DOMAIN

+---------+--------------------+---------------------------+----------------------+------------------------------+-------------------------+
|NUM_ROWS |NUM_DISTINCT_GENOMES|NUM_DISTINCT_PIVOT_PROTEINS|NUM_DISTINCT_PIVOT_DAS|NUM_DISTINCT_NEIGHBOR_PROTEINS|NUM_DISTINCT_NEIGHBOR_DAS|
+---------+--------------------+---------------------------+----------------------+------------------------------+-------------------------+
|770055363|206575              |11144804                   |2599                  |32723557                      |205665                   |
+---------+--------------------+---------------------------+----------------------+------------------------------+-------------------------+

completed in 220.56 seconds


SELECT *
  FROM
    GENOME_PIVOT_NEIGHBOR_PROTEIN_DOMAIN
    ORDER BY 1, 6, 7
    LIMIT 10

+----------------+--------------------------------+---------------------------------+--------------------------------+------------------------------------+-----------+--------------+----------------+-------------+
|ACCESSION_NUMBER|PIVOT_PROTEIN_UID_KEY           |PIVOT_DOMAIN_ARCHITECTURE_UID_KEY|NEIGHBOR_PROTEIN_UID_KEY        |NEIGHBOR_DOMAIN_ARCHITECTURE_UID_KEY|PIVOT_LOCUS|NEIGHBOR_LOCUS|NORMALIZED_LOCUS|NEIGHBOR_TYPE|
+----------------+--------------------------------+---------------------------------+--------------------------------+------------------------------------+-----------+--------------+----------------+-------------+
|DRR000852       |e64e1edddf8f309d22d035ea555551ba|907c804ad461380825ff5806c800fd36 |e64e1edddf8f309d22d035ea555551ba|907c804ad461380825ff5806c800fd36    |1          |1             |0               |P            |
|DRR000852       |e64e1edddf8f309d22d035ea555551ba|907c804ad461380825ff5806c800fd36 |ef4722507bcba3a45c65c34f3448da76|6b015fd35d74149c2c36c5456ca645fd    |1          |2             |1               |PD           |
|DRR000852       |e64e1edddf8f309d22d035ea555551ba|907c804ad461380825ff5806c800fd36 |bc4ae5402da1f7ffc97e086d78530f1d|98e15bb50a6621fb63bf9e916ba7f732    |1          |3             |2               |PD           |
|DRR000852       |02156585fa000cdb6c629e49b3f4852d|8cdcb3c1d66fec1450ad75b98b46e51c |5211887f78b6a5a981f367fcb6978900|d91e855b9633c7bf2e8df99874bf19c4    |6          |4             |-2              |PD           |
|DRR000852       |02156585fa000cdb6c629e49b3f4852d|8cdcb3c1d66fec1450ad75b98b46e51c |d0f6086f585607dc679855de13623b52|e224b72e44e30301d209ee0463187ba3    |6          |5             |-1              |PD           |
|DRR000852       |02156585fa000cdb6c629e49b3f4852d|8cdcb3c1d66fec1450ad75b98b46e51c |02156585fa000cdb6c629e49b3f4852d|8cdcb3c1d66fec1450ad75b98b46e51c    |6          |6             |0               |P            |
|DRR000852       |02156585fa000cdb6c629e49b3f4852d|8cdcb3c1d66fec1450ad75b98b46e51c |201ba1d6b365d6b9df32993558412c74|5cc31c8587777f46a1bcda5728cab22b    |6          |7             |1               |C            |
|DRR000852       |02156585fa000cdb6c629e49b3f4852d|8cdcb3c1d66fec1450ad75b98b46e51c |2294ecc758be3a4f2086e48f805bc086|5ba36edbf3bfe41e63fc67efc0649d9d    |6          |8             |2               |PD           |
|DRR000852       |201ba1d6b365d6b9df32993558412c74|5cc31c8587777f46a1bcda5728cab22b |d0f6086f585607dc679855de13623b52|e224b72e44e30301d209ee0463187ba3    |7          |5             |-2              |PD           |
|DRR000852       |201ba1d6b365d6b9df32993558412c74|5cc31c8587777f46a1bcda5728cab22b |02156585fa000cdb6c629e49b3f4852d|8cdcb3c1d66fec1450ad75b98b46e51c    |7          |6             |-1              |C            |
+----------------+--------------------------------+---------------------------------+--------------------------------+------------------------------------+-----------+--------------+----------------+-------------+

completed in 11.57 seconds


real	37m14.758s
user	461m30.223s
sys	46m19.159s
```
