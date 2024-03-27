@sql/settings.sql;

CACHE TABLE GENOME_PROTEIN;

CACHE TABLE GENOME_PIVOT_PROTEIN;

CACHE TABLE PIVOT_PROTEIN;

DROP TABLE IF EXISTS GENOME_PIVOT_NEIGHBOR_PROTEIN;

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
        NEIGHBOR_TYPE;

CACHE TABLE GENOME_PIVOT_NEIGHBOR_PROTEIN;

SELECT
  COUNT(1) AS NUM_ROWS,
  COUNT(DISTINCT ACCESSION_NUMBER) AS NUM_DISTINCT_GENOMES,
  COUNT(DISTINCT PIVOT_PROTEIN_UID_KEY) AS NUM_DISTINCT_PIVOT_PROTEINS,
  COUNT(DISTINCT NEIGHBOR_PROTEIN_UID_KEY) AS NUM_DISTINCT_NEIGHBOR_PROTEINS
  FROM
    GENOME_PIVOT_NEIGHBOR_PROTEIN;

SELECT *
  FROM
    GENOME_PIVOT_NEIGHBOR_PROTEIN
    ORDER BY 1, 4, 5
    LIMIT 10;