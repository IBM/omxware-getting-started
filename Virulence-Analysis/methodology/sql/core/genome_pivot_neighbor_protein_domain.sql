CACHE TABLE GENOME_PIVOT_NEIGHBOR_PROTEIN;

CACHE TABLE PROTEIN_DOMAIN_ARCHITECTURE;

DROP TABLE IF EXISTS GENOME_PIVOT_NEIGHBOR_PROTEIN_DOMAIN;

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
        A.NEIGHBOR_TYPE;

CACHE TABLE GENOME_PIVOT_NEIGHBOR_PROTEIN_DOMAIN;

SELECT
  COUNT(1) AS NUM_ROWS,
  COUNT(DISTINCT ACCESSION_NUMBER) AS NUM_DISTINCT_GENOMES,
  COUNT(DISTINCT PIVOT_PROTEIN_UID_KEY) AS NUM_DISTINCT_PIVOT_PROTEINS,
  COUNT(DISTINCT PIVOT_DOMAIN_ARCHITECTURE_UID_KEY) AS NUM_DISTINCT_PIVOT_DAS,
  COUNT(DISTINCT NEIGHBOR_PROTEIN_UID_KEY) AS NUM_DISTINCT_NEIGHBOR_PROTEINS,
  COUNT(DISTINCT NEIGHBOR_DOMAIN_ARCHITECTURE_UID_KEY) AS NUM_DISTINCT_NEIGHBOR_DAS
  FROM
    GENOME_PIVOT_NEIGHBOR_PROTEIN_DOMAIN;

SELECT *
  FROM
    GENOME_PIVOT_NEIGHBOR_PROTEIN_DOMAIN
    ORDER BY 1, 6, 7
    LIMIT 10;
