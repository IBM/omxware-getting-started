CACHE TABLE GENOME_PROTEIN;

CACHE TABLE PIVOT_PROTEIN;

DROP TABLE IF EXISTS GENOME_PIVOT_PROTEIN;

CREATE TABLE GENOME_PIVOT_PROTEIN
  USING PARQUET
  AS
  SELECT
    B.ACCESSION_NUMBER,
    B.PROTEIN_UID_KEY,
    B.LOCUS
    FROM
      PIVOT_PROTEIN A
      INNER JOIN GENOME_PROTEIN B ON
        B.PROTEIN_UID_KEY = A.PROTEIN_UID_KEY
      GROUP BY
        B.ACCESSION_NUMBER,
        B.PROTEIN_UID_KEY,
        B.LOCUS;

CACHE TABLE GENOME_PIVOT_PROTEIN;

SELECT
  COUNT(1) AS NUM_ROWS,
  COUNT(DISTINCT ACCESSION_NUMBER) AS NUM_DISTINCT_GENOMES,
  COUNT(DISTINCT PROTEIN_UID_KEY) AS NUM_DISTINCT_PROTEINS
  FROM
    GENOME_PIVOT_PROTEIN;

SELECT *
  FROM
    GENOME_PIVOT_PROTEIN
    ORDER BY 1, 3
    LIMIT 10;
