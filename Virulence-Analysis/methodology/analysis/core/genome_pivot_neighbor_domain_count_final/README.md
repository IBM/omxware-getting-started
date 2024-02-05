# Genome Pivot Neighbor Domain Count Final

This table represents final counts at the genome level. Taking the sum of the counts in this table will produce the counts observed at the genus level.

[back to parent](/analysis/README.md)

Run the following to create the data:

```
./spark-sql.sh --sql-file sql/core/genome_pivot_neighbor_domain_count_final.sql
```

OUTPUT

```sql
CACHE TABLE GENOME_TABLE

completed in 8.98 seconds


CACHE TABLE GENUS_MINIMUM_CUTOFF_THRESHOLD

completed in 0.30 seconds


CACHE TABLE GENUS_PIVOT_NEIGHBOR_DOMAIN_COUNT_FINAL

completed in 1.77 seconds


CACHE TABLE GENOME_PIVOT_NEIGHBOR_DOMAIN_COUNT

completed in 78.30 seconds


DROP TABLE IF EXISTS GENUS_GENOME_PIVOT_NEIGHBOR_DOMAIN_COUNT

completed in 0.05 seconds


CREATE TABLE GENUS_GENOME_PIVOT_NEIGHBOR_DOMAIN_COUNT
  USING PARQUET
  AS
  SELECT
    A.GENUS_NAME,
    B.*
    FROM
      GENOME_TABLE A
      INNER JOIN GENOME_PIVOT_NEIGHBOR_DOMAIN_COUNT B ON
        B.ACCESSION_NUMBER = A.ACCESSION_NUMBER

completed in 75.31 seconds


CACHE TABLE GENUS_GENOME_PIVOT_NEIGHBOR_DOMAIN_COUNT

completed in 74.33 seconds


SELECT
  COUNT(1) AS NUM_ROWS,
  COUNT(DISTINCT GENUS_NAME) AS NUM_DISTINCT_GENERA,
  COUNT(DISTINCT ACCESSION_NUMBER) AS NUM_DISTINCT_GENOMES,
  COUNT(DISTINCT PIVOT_DOMAIN_ARCHITECTURE_UID_KEY) AS NUM_DISTINCT_PIVOTS,
  COUNT(DISTINCT NEIGHBOR_DOMAIN_ARCHITECTURE_UID_KEY) AS NUM_DISTINCT_NEIGHBORS
  FROM
    GENUS_GENOME_PIVOT_NEIGHBOR_DOMAIN_COUNT

+---------+-------------------+--------------------+-------------------+----------------------+
|NUM_ROWS |NUM_DISTINCT_GENERA|NUM_DISTINCT_GENOMES|NUM_DISTINCT_PIVOTS|NUM_DISTINCT_NEIGHBORS|
+---------+-------------------+--------------------+-------------------+----------------------+
|604924777|1401               |206575              |2599               |205665                |
+---------+-------------------+--------------------+-------------------+----------------------+

completed in 28.84 seconds


SELECT *
  FROM
    GENUS_GENOME_PIVOT_NEIGHBOR_DOMAIN_COUNT
    LIMIT 10

+--------------+----------------+---------------------------------+------------------------------------+-------------+-----+
|GENUS_NAME    |ACCESSION_NUMBER|PIVOT_DOMAIN_ARCHITECTURE_UID_KEY|NEIGHBOR_DOMAIN_ARCHITECTURE_UID_KEY|NEIGHBOR_TYPE|COUNT|
+--------------+----------------+---------------------------------+------------------------------------+-------------+-----+
|bacillus      |DRR014328       |45d88a3a9ff15c451fa46cbd3afb2bb5 |bd25c19e93a59cdd5a17bb87892a4570    |PD           |1    |
|bacillus      |DRR014740       |2b17e8fd881d02567be099bbdffc82e8 |2b17e8fd881d02567be099bbdffc82e8    |P            |83   |
|staphylococcus|DRR015575       |18db427071bf4187c97dfce95fb0ca31 |18db427071bf4187c97dfce95fb0ca31    |P            |1    |
|morganella    |DRR015595       |571b42ff58bf906f7c7f9970da2c1d99 |35cc3325c2d5d06c3c63074c20e09c1c    |C            |3    |
|burkholderia  |DRR015637       |59dbf2f37396f58b59d427a90ac5767c |f9d0af8675c6bc1c4674d8b8441ce792    |PD           |1    |
|providencia   |DRR015744       |91722e16156b523d723da95c7de0a95b |c49d9c413f9fd6aeb8691deefdcf334f    |PD           |1    |
|serratia      |DRR015758       |35cc3325c2d5d06c3c63074c20e09c1c |35cc3325c2d5d06c3c63074c20e09c1c    |C            |18   |
|tsukamurella  |DRR015819       |4053c439daebb3b974ef7269dec8199a |2ef27e96f76d1ef46c3a35b3729cb916    |PD           |1    |
|staphylococcus|DRR015844       |b65140fbd9036b5a2bd5bed40dd4a405 |5288c5a0422fbe93f8b2c083b7fb4b1b    |PD           |1    |
|shigella      |DRR015932       |a9b90241e2e1072a57ace851c11b18ae |2144bdc522c300f2daf98925878dc4d8    |PD           |1    |
+--------------+----------------+---------------------------------+------------------------------------+-------------+-----+

completed in 0.45 seconds


DROP TABLE IF EXISTS GENOME_PIVOT_NEIGHBOR_DOMAIN_COUNT_FINAL

completed in 1.01 seconds


CREATE TABLE GENOME_PIVOT_NEIGHBOR_DOMAIN_COUNT_FINAL
  USING PARQUET
  AS
  SELECT
    B.ACCESSION_NUMBER,
    B.PIVOT_DOMAIN_ARCHITECTURE_UID_KEY,
    B.NEIGHBOR_DOMAIN_ARCHITECTURE_UID_KEY,
    CASE WHEN B.NEIGHBOR_TYPE = 'PD'
      THEN 'D'
      ELSE B.NEIGHBOR_TYPE
    END AS NEIGHBOR_TYPE,
    B.COUNT
    FROM
      GENOME_TABLE A
      INNER JOIN GENUS_GENOME_PIVOT_NEIGHBOR_DOMAIN_COUNT B ON
        B.GENUS_NAME = A.GENUS_NAME AND
        B.ACCESSION_NUMBER = A.ACCESSION_NUMBER
      INNER JOIN GENUS_PIVOT_NEIGHBOR_DOMAIN_COUNT_FINAL C ON
        C.GENUS_NAME = B.GENUS_NAME AND
        C.PIVOT_DOMAIN_ARCHITECTURE_UID_KEY = B.PIVOT_DOMAIN_ARCHITECTURE_UID_KEY AND
        C.NEIGHBOR_DOMAIN_ARCHITECTURE_UID_KEY = B.NEIGHBOR_DOMAIN_ARCHITECTURE_UID_KEY
      GROUP BY
        B.ACCESSION_NUMBER,
        B.PIVOT_DOMAIN_ARCHITECTURE_UID_KEY,
        B.NEIGHBOR_DOMAIN_ARCHITECTURE_UID_KEY,
        4,
        B.COUNT

completed in 987.85 seconds


CACHE TABLE GENOME_PIVOT_NEIGHBOR_DOMAIN_COUNT_FINAL

completed in 57.08 seconds


SELECT
  COUNT(1) AS NUM_ROWS,
  COUNT(DISTINCT ACCESSION_NUMBER) AS NUM_DISTINCT_GENOMES,
  COUNT(DISTINCT PIVOT_DOMAIN_ARCHITECTURE_UID_KEY) AS NUM_DISTINCT_PIVOTS,
  COUNT(DISTINCT NEIGHBOR_DOMAIN_ARCHITECTURE_UID_KEY) AS NUM_DISTINCT_NEIGHBORS
  FROM
    GENOME_PIVOT_NEIGHBOR_DOMAIN_COUNT_FINAL

+---------+--------------------+-------------------+----------------------+
|NUM_ROWS |NUM_DISTINCT_GENOMES|NUM_DISTINCT_PIVOTS|NUM_DISTINCT_NEIGHBORS|
+---------+--------------------+-------------------+----------------------+
|557645831|206573              |2599               |82659                 |
+---------+--------------------+-------------------+----------------------+

completed in 22.31 seconds


SELECT *
  FROM
    GENOME_PIVOT_NEIGHBOR_DOMAIN_COUNT_FINAL
    ORDER BY 1, 2
    LIMIT 20

+----------------+---------------------------------+------------------------------------+-------------+-----+
|ACCESSION_NUMBER|PIVOT_DOMAIN_ARCHITECTURE_UID_KEY|NEIGHBOR_DOMAIN_ARCHITECTURE_UID_KEY|NEIGHBOR_TYPE|COUNT|
+----------------+---------------------------------+------------------------------------+-------------+-----+
|DRR000852       |004bbe5dfa2576f4eb22496dea1a68ca |004bbe5dfa2576f4eb22496dea1a68ca    |P            |2    |
|DRR000852       |004bbe5dfa2576f4eb22496dea1a68ca |6cc9c5a77bc59b9a80a60908e73237fb    |D            |1    |
|DRR000852       |004bbe5dfa2576f4eb22496dea1a68ca |0c2ebf137aa5a698e42e3b432b3b0564    |D            |1    |
|DRR000852       |004bbe5dfa2576f4eb22496dea1a68ca |e534f55bf9acd5b2a463332b1604fee4    |D            |1    |
|DRR000852       |004bbe5dfa2576f4eb22496dea1a68ca |82cb6dbfe53ec92ba2fe3230d971b29d    |D            |1    |
|DRR000852       |004bbe5dfa2576f4eb22496dea1a68ca |f922f6fbacd38435b275a010b19e58a7    |D            |1    |
|DRR000852       |004bbe5dfa2576f4eb22496dea1a68ca |8a4eee41faab6da2abd71cda0a232440    |C            |1    |
|DRR000852       |004bbe5dfa2576f4eb22496dea1a68ca |49a334c8e7bd78d0bda73d8be6584122    |D            |1    |
|DRR000852       |00c15f2eb1af4226843af9938222952f |8c0cfea72bb7ddab3df5c74865e46a49    |D            |1    |
|DRR000852       |00c15f2eb1af4226843af9938222952f |79e5a9c9f5f07ec8daec089b7d5fb77f    |D            |1    |
|DRR000852       |00c15f2eb1af4226843af9938222952f |00c15f2eb1af4226843af9938222952f    |P            |1    |
|DRR000852       |00c8d9363c3fd70dc7234eaaf54ce8de |36deb721dd2bec14f606553cd28d8fc1    |D            |1    |
|DRR000852       |00c8d9363c3fd70dc7234eaaf54ce8de |5b0f09e18f5a9b1b0e1be46e90c95707    |D            |1    |
|DRR000852       |00c8d9363c3fd70dc7234eaaf54ce8de |cc9b18a8a2a19bcb8d4b20de71716b07    |C            |2    |
|DRR000852       |00c8d9363c3fd70dc7234eaaf54ce8de |d9f00addf28afcfdf10a3d035cde01ed    |D            |1    |
|DRR000852       |00c8d9363c3fd70dc7234eaaf54ce8de |99a6ec6c55d7261c651c7fd389392987    |D            |1    |
|DRR000852       |00c8d9363c3fd70dc7234eaaf54ce8de |f08a49b3e5189441e1c2f9033d5e27bb    |C            |1    |
|DRR000852       |00c8d9363c3fd70dc7234eaaf54ce8de |00c8d9363c3fd70dc7234eaaf54ce8de    |P            |2    |
|DRR000852       |00c8d9363c3fd70dc7234eaaf54ce8de |1485d652ab5f1c7359275eb4fc589c8f    |D            |1    |
|DRR000852       |0137d518ab8063fbf3d193157849faa8 |0137d518ab8063fbf3d193157849faa8    |P            |1    |
+----------------+---------------------------------+------------------------------------+-------------+-----+

completed in 5.38 seconds


DROP TABLE GENUS_GENOME_PIVOT_NEIGHBOR_DOMAIN_COUNT

completed in 0.54 seconds


real	22m34.076s
user	352m2.684s
sys	28m16.077s
```
