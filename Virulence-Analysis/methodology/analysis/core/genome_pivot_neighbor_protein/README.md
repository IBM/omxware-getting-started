# Genome Pivot Neighbor Protein

This table is an extension of GENOME_PIVOT_PROTEIN and records the genome accession, pivot, locus, and associated neighbors. Pivots are labeled with P and match proteins in VFDB based on exact domain architecture. Co-pivots are labeled with C and match proteins in VFDB based on exact domain architecture, however, these proteins are found as neighbors to the current pivot protein. Putative discoveries are labeled with PD and do not match any protein in VFDB. These proteins are labeled putative because they are not found to be discoveries until a selectivity threshold has been based in a sub-sequent step. These proteins might play critical roles via co-occurrence with pivots and co-pivots in the exhibited virulence. They could also be crucial in the study of pathogenicity islands too.

[back to parent](/analysis/README.md)

Run the following to create the data:

```
./spark-sql.sh --sql-file sql/core/genome_pivot_neighbor_protein.sql
```

OUTPUT

```sql
SET best_similarity = 1

completed in 1.79 seconds

SET distance = 2

completed in 0.03 seconds

SET data_dir = /gpfs/grand/Users/eseabolt/virulence/data

completed in 0.01 seconds

SET outputs_dir = /gpfs/grand/Users/eseabolt/virulence/outputs

completed in 0.01 seconds

SET plots_dir = /gpfs/grand/Users/eseabolt/virulence/plots

completed in 0.01 seconds


CACHE TABLE GENOME_PROTEIN

completed in 62.70 seconds


CACHE TABLE GENOME_PIVOT_PROTEIN

completed in 12.56 seconds


CACHE TABLE PIVOT_PROTEIN

completed in 0.81 seconds


DROP TABLE IF EXISTS GENOME_PIVOT_NEIGHBOR_PROTEIN

completed in 1.19 seconds


CREATE TABLE GENOME_PIVOT_NEIGHBOR_PROTEIN
  USING PARQUET
  AS
  SELECT
    ACCESSION_NUMBER,
    PIVOT_PROTEIN_UID_KEY,
    NEIGHBOR_PROTEIN_UID_KEY,
    PIVOT_LOCUS,
    NEIGHBOR_LOCUS,
    NORMALIZED_LOCUS,
    NEIGHBOR_TYPE
    FROM
      (SELECT
        A.ACCESSION_NUMBER,
        A.PROTEIN_UID_KEY AS PIVOT_PROTEIN_UID_KEY,
        B.PROTEIN_UID_KEY AS NEIGHBOR_PROTEIN_UID_KEY,
        A.LOCUS AS PIVOT_LOCUS,
        B.LOCUS AS NEIGHBOR_LOCUS,
        B.LOCUS - A.LOCUS AS NORMALIZED_LOCUS,
        CASE WHEN C.PROTEIN_UID_KEY IS NULL
          THEN 'PD'
          ELSE CASE WHEN B.LOCUS - A.LOCUS = 0 THEN 'P' ELSE 'C' END
        END AS NEIGHBOR_TYPE
        FROM
          GENOME_PIVOT_PROTEIN A
          INNER JOIN GENOME_PROTEIN B ON
            B.ACCESSION_NUMBER = A.ACCESSION_NUMBER AND
            B.LOCUS BETWEEN A.LOCUS - ${distance} AND A.LOCUS + ${distance}
          LEFT JOIN PIVOT_PROTEIN C ON
            C.PROTEIN_UID_KEY = B.PROTEIN_UID_KEY)
      GROUP BY
        ACCESSION_NUMBER,
        PIVOT_PROTEIN_UID_KEY,
        NEIGHBOR_PROTEIN_UID_KEY,
        PIVOT_LOCUS,
        NEIGHBOR_LOCUS,
        NORMALIZED_LOCUS,
        NEIGHBOR_TYPE

completed in 1557.95 seconds


CACHE TABLE GENOME_PIVOT_NEIGHBOR_PROTEIN

completed in 80.90 seconds


SELECT
  COUNT(1) AS NUM_ROWS,
  COUNT(DISTINCT ACCESSION_NUMBER) AS NUM_DISTINCT_GENOMES,
  COUNT(DISTINCT PIVOT_PROTEIN_UID_KEY) AS NUM_DISTINCT_PIVOT_PROTEINS,
  COUNT(DISTINCT NEIGHBOR_PROTEIN_UID_KEY) AS NUM_DISTINCT_NEIGHBOR_PROTEINS
  FROM
    GENOME_PIVOT_NEIGHBOR_PROTEIN

+---------+--------------------+---------------------------+------------------------------+
|NUM_ROWS |NUM_DISTINCT_GENOMES|NUM_DISTINCT_PIVOT_PROTEINS|NUM_DISTINCT_NEIGHBOR_PROTEINS|
+---------+--------------------+---------------------------+------------------------------+
|770055363|206575              |11144804                   |32723557                      |
+---------+--------------------+---------------------------+------------------------------+

completed in 132.77 seconds


SELECT *
  FROM
    GENOME_PIVOT_NEIGHBOR_PROTEIN
    ORDER BY 1, 4, 5
    LIMIT 10

+----------------+--------------------------------+--------------------------------+-----------+--------------+----------------+-------------+
|ACCESSION_NUMBER|PIVOT_PROTEIN_UID_KEY           |NEIGHBOR_PROTEIN_UID_KEY        |PIVOT_LOCUS|NEIGHBOR_LOCUS|NORMALIZED_LOCUS|NEIGHBOR_TYPE|
+----------------+--------------------------------+--------------------------------+-----------+--------------+----------------+-------------+
|DRR000852       |e64e1edddf8f309d22d035ea555551ba|e64e1edddf8f309d22d035ea555551ba|1          |1             |0               |P            |
|DRR000852       |e64e1edddf8f309d22d035ea555551ba|ef4722507bcba3a45c65c34f3448da76|1          |2             |1               |PD           |
|DRR000852       |e64e1edddf8f309d22d035ea555551ba|bc4ae5402da1f7ffc97e086d78530f1d|1          |3             |2               |PD           |
|DRR000852       |02156585fa000cdb6c629e49b3f4852d|5211887f78b6a5a981f367fcb6978900|6          |4             |-2              |PD           |
|DRR000852       |02156585fa000cdb6c629e49b3f4852d|d0f6086f585607dc679855de13623b52|6          |5             |-1              |PD           |
|DRR000852       |02156585fa000cdb6c629e49b3f4852d|02156585fa000cdb6c629e49b3f4852d|6          |6             |0               |P            |
|DRR000852       |02156585fa000cdb6c629e49b3f4852d|201ba1d6b365d6b9df32993558412c74|6          |7             |1               |C            |
|DRR000852       |02156585fa000cdb6c629e49b3f4852d|2294ecc758be3a4f2086e48f805bc086|6          |8             |2               |PD           |
|DRR000852       |201ba1d6b365d6b9df32993558412c74|d0f6086f585607dc679855de13623b52|7          |5             |-2              |PD           |
|DRR000852       |201ba1d6b365d6b9df32993558412c74|02156585fa000cdb6c629e49b3f4852d|7          |6             |-1              |C            |
+----------------+--------------------------------+--------------------------------+-----------+--------------+----------------+-------------+

completed in 7.64 seconds


real	31m9.663s
user	467m4.948s
sys	36m11.614s
```
