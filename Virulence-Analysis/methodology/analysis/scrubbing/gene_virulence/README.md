# GENE_VIRULENCE

[back to parent](../README.md)

Run the following to scrub the data into the finalized form:

```
./spark-sql.sh --sql-file sql/scrubbing/gene_virulence.sql
```

OUTPUT

```sql
CACHE TABLE GENE_VIRULENCE_STAGING

completed in 7.86 seconds


DROP TABLE IF EXISTS GENE_VIRULENCE

completed in 0.04 seconds


CREATE TABLE GENE_VIRULENCE
  USING PARQUET
  AS
  SELECT
    GENE_UID_KEY,
    SHORT_NAME,
    FULL_NAME,
    VIRULENCE_FACTOR,
    LOWER(GENUS_NAME) AS GENUS_NAME,
    SPECIES_NAME,
    STRAIN
    FROM
      GENE_VIRULENCE_STAGING

completed in 1.53 seconds


CACHE TABLE GENE_VIRULENCE

completed in 0.48 seconds


SELECT
  COUNT(1) AS NUM_ROWS,
  COUNT(DISTINCT GENE_UID_KEY) AS NUM_DISTINCT_GENES
  FROM
    GENE_VIRULENCE

+--------+------------------+
|NUM_ROWS|NUM_DISTINCT_GENES|
+--------+------------------+
|32522   |32506             |
+--------+------------------+

completed in 1.22 seconds


SELECT *
  FROM
    GENE_VIRULENCE
    ORDER BY 1
    LIMIT 10

+--------------------------------+----------+-----------------------------------------------------------------------+---------------------------------------------+--------------+----------------+-------------------------+
|GENE_UID_KEY                    |SHORT_NAME|FULL_NAME                                                              |VIRULENCE_FACTOR                             |GENUS_NAME    |SPECIES_NAME    |STRAIN                   |
+--------------------------------+----------+-----------------------------------------------------------------------+---------------------------------------------+--------------+----------------+-------------------------+
|000076d461ed3d46b8f28f3d865c8f29|ahpC      |Alkyl hydroperoxide reductase subunit C, AhpC (alkyl hydroperoxidase C)|AhpC (CVF322)                                |mycobacterium |canettii        |CIPT 140070008           |
|0000bb2c4e291abb3914d3f84f12f5ca|cswA      |CS12 fimbria major subunit protein precursor                           |Adhesive fimbriae (VF0213)                   |escherichia   |coli            |O159:H4 str. 350C1       |
|0001e8cd0d4c572652377333888038fa|alg44     |alginate biosynthesis protein Alg44                                    |Alginate biosynthesis (CVF522)               |pseudomonas   |aeruginosa      |LESB58                   |
|000383cafe219d6409265aacf9dc31d9|vopC      |type III secretion system effector VopC                                |T3SS2 (VF0409)                               |vibrio        |parahaemolyticus|RIMD 2210633             |
|00052d109dd7cab35363b597cc4ea59c|hlyA      |hemolysin structural protein HlyA                                      |Alpha-hemolysin (CVF453)                     |escherichia   |coli            |UMNK88                   |
|0007fd00a9fb5ae37e50181b0823a2f7|plr/gapA  |glyceraldehyde-3-phosphate dehydrogenase                               |Streptococcal plasmin receptor/GAPDH (CVF123)|streptococcus |agalactiae      |A909                     |
|000b4b726142784d9db2dc9747273a34|atl       |bifunctional autolysin precursor                                       |Autolysin (CVF109)                           |staphylococcus|aureus          |subsp. aureus str. Newman|
|000bdbfc2240c90563225f920b546316|rvhB6e    |lipoprotein                                                            |Rvh T4SS (CVF804)                            |rickettsia    |prowazekii      |Breinl                   |
|000d6c900e8da3df7f141225d60ed373|zmp1      |Putative zinc metalloprotease                                          |Zn++ metallophrotease (CVF655)               |mycobacterium |canettii        |CIPT 140070017           |
|000f5c5ae97acd32e5c97c0ed9c1d4ae|mce8B     |virulence factor Mce family protein                                    |Mce8 (CVF343)                                |mycobacterium |smegmatis       |str. MC2 155             |
+--------------------------------+----------+-----------------------------------------------------------------------+---------------------------------------------+--------------+----------------+-------------------------+

completed in 0.23 seconds


DROP TABLE GENE_VIRULENCE_STAGING

completed in 0.46 seconds


real	0m17.884s
user	0m54.020s
sys	0m6.383s
```
