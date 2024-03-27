# PROTEIN_VIRULENCE

[back to parent](../README.md)

Run the following to scrub the data into the finalized form:

```
./spark-sql.sh --sql-file sql/scrubbing/protein_virulence.sql
```

OUTPUT

```sql
CACHE TABLE PROTEIN_VIRULENCE_STAGING

completed in 8.41 seconds


DROP TABLE IF EXISTS PROTEIN_VIRULENCE

completed in 0.59 seconds


CREATE TABLE PROTEIN_VIRULENCE
  USING PARQUET
  AS
  SELECT
    PROTEIN_UID_KEY,
    SHORT_NAME,
    FULL_NAME,
    VIRULENCE_FACTOR,
    LOWER(GENUS_NAME) AS GENUS_NAME,
    SPECIES_NAME,
    STRAIN
    FROM
      PROTEIN_VIRULENCE_STAGING

completed in 1.44 seconds


CACHE TABLE PROTEIN_VIRULENCE

completed in 0.44 seconds


SELECT
  COUNT(1) AS NUM_ROWS,
  COUNT(DISTINCT PROTEIN_UID_KEY) AS NUM_DISTINCT_PROTEINS
  FROM
    PROTEIN_VIRULENCE

+--------+---------------------+
|NUM_ROWS|NUM_DISTINCT_PROTEINS|
+--------+---------------------+
|28616   |28583                |
+--------+---------------------+

completed in 1.20 seconds


SELECT *
  FROM
    PROTEIN_VIRULENCE
    ORDER BY 1
    LIMIT 10

+--------------------------------+-------------+----------------------------------------------------------+--------------------------------------------+--------------+--------------+------------------------------+
|PROTEIN_UID_KEY                 |SHORT_NAME   |FULL_NAME                                                 |VIRULENCE_FACTOR                            |GENUS_NAME    |SPECIES_NAME  |STRAIN                        |
+--------------------------------+-------------+----------------------------------------------------------+--------------------------------------------+--------------+--------------+------------------------------+
|0002ba31fbd5ca08f01a3eaff57bd04a|mce4D        |MCE-family protein Mce4D                                  |Mce4 (CVF339)                               |mycobacterium |sp.           |JDM601                        |
|000322c916db9eff63c30a7a862bb1ab|mbtG         |L-lysine 6-monooxygenase mbtG                             |Mycobactin (CVF315)                         |mycobacterium |abscessus     |subsp. bolletii str. GO 06    |
|00074c0eeaa108a55a4b222625060fd7|mce1E        |MCE-family lipoprotein LprK (MCE-family lipoprotein Mce1E)|Mce1 (CVF336)                               |mycobacterium |ulcerans      |Agy99                         |
|000919d093d765d0bf7fb0ce98f0c2f8|SAUSA300_0301|hypothetical protein                                      |Type VII secretion system (CVF624)          |staphylococcus|aureus        |subsp. aureus USA300_FPR3757  |
|00091fd2162738cdc4da072187ec79aa|mprB         |hypothetical protein                                      |MprA/B (CVF333)                             |mycobacterium |avium         |subsp. paratuberculosis K-10  |
|000e0c1d47741fad104a93ace8cbcf3c|tarp         |Translocated actin-recruiting protein                     |Type III secretion system effectors (CVF872)|chlamydia     |trachomatis   |L2b/UCH-1/proctitis           |
|0011f40ebe94dca6d71341b25f5ead6e|xpsK         |general secretion pathway protein K                       |xps (SS213)                                 |xanthomonas   |campestris    |pv. campestris str. ATCC 33913|
|00173a3dd244e6aec748d9af83239026|virB10       |type IV secretion system protein VirB10                   |Rvh T4SS (CVF797)                           |anaplasma     |centrale      |str. Israel                   |
|001762c800f3ceeb21a3435b55574d20|cagQ         |cag pathogenicity island protein Q                        |Cag PAI type IV secretion system (CVF217)   |helicobacter  |pylori        |G27                           |
|001976d13811974a75b463649720d99d|yst1J        |putative general secretion pathway protein J precursor    |yts1 (SS208)                                |yersinia      |enterocolitica|subsp. enterocolitica 8081    |
+--------------------------------+-------------+----------------------------------------------------------+--------------------------------------------+--------------+--------------+------------------------------+

completed in 0.21 seconds


DROP TABLE PROTEIN_VIRULENCE_STAGING

completed in 0.27 seconds


real	0m18.142s
user	0m56.049s
sys	0m7.619s
```
