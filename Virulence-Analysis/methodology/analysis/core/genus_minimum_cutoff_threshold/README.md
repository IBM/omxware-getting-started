# Genus Minimum Cutoff Threshold

Calculation of the minimum cutoff or selectivity threshold used to remove low frequency neighbors. The cutoff is determined via a Spark User Defined Function (UDF) called mct which utilizes the KneeLocator object from [here](https://github.com/arvkevi/kneed). Since most of the data is noisy, the curves are fitted with an exponential decay function. This model is passed to KneeLocator which determines the minimum (elbow). Plots are also created for reference. See [udfs.py](/Virulence-Analysis/methodology/udfs.py) for implementation. All available genera can be found in the [plots](/Virulence-Analysis/methodology/plots/mct) directory. Only neighbor type of PD is used for this analysis.

[back to parent](/Virulence-Analysis/methodology/analysis/README.md)

### Example analysis for Klebsiella

![klebsiella.png](/Virulence-Analysis/methodology/plots/mct/k/klebsiella.png)

Run the following to create the data:

```
./spark-sql.sh --sql-file sql/core/genus_minimum_cutoff_threshold.sql --udf-mods udfs
```

OUTPUT

```sql
SET best_similarity = 1

completed in 1.87 seconds

SET distance = 2

completed in 0.02 seconds

SET data_dir = /gpfs/grand/Users/eseabolt/virulence/data

completed in 0.02 seconds

SET outputs_dir = /gpfs/grand/Users/eseabolt/virulence/outputs

completed in 0.01 seconds

SET plots_dir = /gpfs/grand/Users/eseabolt/virulence/plots

completed in 0.01 seconds


CACHE TABLE GENUS_PIVOT_NEIGHBOR_DOMAIN_COUNT

completed in 9.93 seconds


DROP TABLE IF EXISTS GENUS_MINIMUM_CUTOFF_THRESHOLD

completed in 0.73 seconds


CREATE TABLE GENUS_MINIMUM_CUTOFF_THRESHOLD
  USING PARQUET
  AS
  SELECT
    GENUS_NAME,
    MCT(COLLECT_LIST(COUNT), GENUS_NAME, '${plots_dir}/mct') AS THRESHOLD
    FROM
      GENUS_PIVOT_NEIGHBOR_DOMAIN_COUNT
      WHERE
        NEIGHBOR_DOMAIN_ARCHITECTURE_UID_KEY IS NOT NULL AND
        NEIGHBOR_TYPE = 'PD'
      GROUP BY
        GENUS_NAME

genus=abiotrophia, num_x=879, num_y=879, elbow_x=96.0, elbow_y=2.0
genus=auricoccus, num_x=678, num_y=678, elbow_x=58.0, elbow_y=2.0
genus=alcaligenes, num_x=3451, num_y=3451, elbow_x=1524.0, elbow_y=10.0
genus=acidiphilium, num_x=3748, num_y=3748, elbow_x=21.0, elbow_y=3.0
genus=bombella, num_x=1106, num_y=1106, elbow_x=493.0, elbow_y=2.0
genus=arachidicoccus, num_x=4747, num_y=4747, elbow_x=774.0, elbow_y=3.0
genus=advenella, num_x=3286, num_y=3286, elbow_x=18.0, elbow_y=3.0
genus=acidobacterium, num_x=1423, num_y=1423, elbow_x=58.0, elbow_y=2.0
genus=candidatus ruthia, num_x=379, num_y=379, elbow_x=12.0, elbow_y=2.0
genus=gracilibacillus, num_x=2043, num_y=2043, elbow_x=21.0, elbow_y=2.0
genus=actinoplanes, num_x=14327, num_y=14327, elbow_x=3046.0, elbow_y=4.0
genus=acholeplasma, num_x=2773, num_y=2773, elbow_x=514.0, elbow_y=3.0
genus=aminobacter, num_x=5039, num_y=5039, elbow_x=45.0, elbow_y=4.0
genus=bergeyella, num_x=3508, num_y=3508, elbow_x=1063.0, elbow_y=2.0
genus=avibacterium, num_x=2341, num_y=2341, elbow_x=914.0, elbow_y=4.0
genus=candidatus atelocyanobacterium, num_x=503, num_y=503, elbow_x=16.0, elbow_y=2.0
genus=candidatus zinderia, num_x=37, num_y=37, elbow_x=8.0, elbow_y=1.0
genus=achromobacter, num_x=22539, num_y=22539, elbow_x=3999.0, elbow_y=17.0
genus=chromohalobacter, num_x=1556, num_y=1556, elbow_x=95.0, elbow_y=2.0
genus=aureitalea, num_x=1116, num_y=1116, elbow_x=63.0, elbow_y=2.0
genus=desemzia, num_x=906, num_y=906, elbow_x=77.0, elbow_y=1.0
genus=actinopolyspora, num_x=1907, num_y=1907, elbow_x=6.0, elbow_y=2.0
genus=halothece, num_x=1431, num_y=1431, elbow_x=97.0, elbow_y=2.0
genus=arthrospira, num_x=1658, num_y=1658, elbow_x=24.0, elbow_y=2.0
genus=chitinolyticbacter, num_x=1725, num_y=1725, elbow_x=91.0, elbow_y=2.0
genus=lactococcus, num_x=10450, num_y=10450, elbow_x=1979.0, elbow_y=16.0
genus=acidisarcina, num_x=2548, num_y=2548, elbow_x=133.0, elbow_y=2.0
genus=desulfonauticus, num_x=829, num_y=829, elbow_x=59.0, elbow_y=1.0
genus=carboxydothermus, num_x=811, num_y=811, elbow_x=56.0, elbow_y=2.0
genus=dolichospermum, num_x=1462, num_y=1462, elbow_x=141.0, elbow_y=2.0
genus=brenneria, num_x=3629, num_y=3629, elbow_x=36.0, elbow_y=3.0
genus=arthrobacter, num_x=32867, num_y=32867, elbow_x=3135.0, elbow_y=5.0
genus=fluviicola, num_x=2153, num_y=2153, elbow_x=857.0, elbow_y=2.0
genus=chelatococcus, num_x=2835, num_y=2835, elbow_x=42.0, elbow_y=4.0
genus=methylocella, num_x=2593, num_y=2593, elbow_x=796.0, elbow_y=3.0
genus=candidatus hepatoplasma, num_x=83, num_y=83, elbow_x=10.0, elbow_y=2.0
genus=luteimicrobium, num_x=1961, num_y=1961, elbow_x=51.0, elbow_y=2.0
genus=adlercreutzia, num_x=936, num_y=936, elbow_x=13.0, elbow_y=2.0
genus=desulfitobacterium, num_x=5168, num_y=5168, elbow_x=1429.0, elbow_y=4.0
genus=chloroherpeton, num_x=1095, num_y=1095, elbow_x=48.0, elbow_y=2.0
genus=mixta, num_x=3066, num_y=3066, elbow_x=1311.0, elbow_y=5.0
genus=halobacteroides, num_x=964, num_y=964, elbow_x=96.0, elbow_y=2.0
genus=desulfococcus, num_x=2721, num_y=2721, elbow_x=1192.0, elbow_y=4.0
genus=acidithiobacillus, num_x=3819, num_y=3819, elbow_x=1203.0, elbow_y=6.0
genus=citricoccus, num_x=1478, num_y=1478, elbow_x=24.0, elbow_y=4.0
genus=moorella, ERROR=Optimal parameters not found: Number of calls to function has reached maxfev = 800.
genus=dinoroseobacter, num_x=1840, num_y=1840, elbow_x=37.0, elbow_y=2.0
genus=mogibacterium, num_x=585, num_y=585, elbow_x=37.0, elbow_y=2.0
genus=massilia, num_x=14592, num_y=14592, elbow_x=2937.0, elbow_y=4.0
genus=confluentimicrobium, num_x=1725, num_y=1725, elbow_x=21.0, elbow_y=2.0
genus=crassaminicella, num_x=1002, num_y=1002, elbow_x=64.0, elbow_y=2.0
genus=neorhizobium, num_x=6166, num_y=6166, elbow_x=35.0, elbow_y=4.0
genus=scardovia, num_x=640, num_y=640, elbow_x=53.0, elbow_y=2.0
genus=elusimicrobium, num_x=622, num_y=622, elbow_x=47.0, elbow_y=2.0
genus=hyphomonas, num_x=3064, num_y=3064, elbow_x=615.0, elbow_y=2.0
genus=aestuariibacter, num_x=2870, num_y=2870, elbow_x=43.0, elbow_y=1.0
genus=actinobacillus, num_x=5441, num_y=5441, elbow_x=1420.0, elbow_y=6.0
genus=inhella, num_x=1760, num_y=1760, elbow_x=94.0, elbow_y=2.0
genus=gemella, num_x=1816, num_y=1816, elbow_x=583.0, elbow_y=5.0
genus=dyadobacter, num_x=3876, num_y=3876, elbow_x=66.0, elbow_y=3.0
genus=obesumbacterium, num_x=1874, num_y=1874, elbow_x=157.0, elbow_y=2.0
genus=micrococcus, num_x=7471, num_y=7471, elbow_x=1742.0, elbow_y=6.0
genus=modestobacter, num_x=2509, num_y=2509, elbow_x=22.0, elbow_y=2.0
genus=nitratifractor, num_x=748, num_y=748, elbow_x=45.0, elbow_y=2.0
genus=albidiferax, num_x=2784, num_y=2784, elbow_x=26.0, elbow_y=1.0
genus=leptotrichia, num_x=4405, num_y=4405, elbow_x=954.0, elbow_y=6.0
genus=sphaerochaeta, num_x=2677, num_y=2677, elbow_x=8.0, elbow_y=3.0
genus=kitasatospora, num_x=10077, num_y=10077, elbow_x=80.0, elbow_y=2.0
genus=oceanobacter, num_x=1780, num_y=1780, elbow_x=97.0, elbow_y=1.0
genus=petrocella, num_x=1295, num_y=1295, elbow_x=46.0, elbow_y=2.0
genus=planococcus, num_x=6057, num_y=6057, elbow_x=1621.0, elbow_y=6.0
genus=glycomyces, num_x=4964, num_y=4964, elbow_x=71.0, elbow_y=2.0
genus=planctomyces, num_x=4062, num_y=4062, elbow_x=72.0, elbow_y=2.0
genus=persicobacter, num_x=1888, num_y=1888, elbow_x=75.0, elbow_y=2.0
genus=actinomyces, num_x=9711, num_y=9711, elbow_x=1535.0, elbow_y=5.0
genus=alistipes, num_x=6937, num_y=6937, elbow_x=1460.0, elbow_y=5.0
genus=paraglaciecola, num_x=5158, num_y=5158, elbow_x=1352.0, elbow_y=3.0
genus=coriobacterium, num_x=721, num_y=721, elbow_x=58.0, elbow_y=2.0
genus=syntrophothermus, num_x=819, num_y=819, elbow_x=71.0, elbow_y=2.0
genus=marinomonas, num_x=8984, num_y=8984, elbow_x=1827.0, elbow_y=4.0
genus=romboutsia, num_x=1346, num_y=1346, elbow_x=113.0, elbow_y=1.0
genus=litoreibacter, num_x=1691, num_y=1691, elbow_x=32.0, elbow_y=2.0
genus=roseitalea, num_x=1588, num_y=1588, elbow_x=32.0, elbow_y=2.0
genus=herbinix, num_x=960, num_y=960, elbow_x=80.0, elbow_y=2.0
genus=odoribacter, num_x=1605, num_y=1605, elbow_x=107.0, elbow_y=5.0
genus=roseomonas, num_x=3341, num_y=3341, elbow_x=32.0, elbow_y=6.0
genus=blattabacterium, num_x=439, num_y=439, elbow_x=191.0, elbow_y=18.0
genus=aequorivita, num_x=3118, num_y=3118, elbow_x=1003.0, elbow_y=3.0
genus=pseudarcicella, num_x=1231, num_y=1231, elbow_x=39.0, elbow_y=2.0
genus=alkalitalea, num_x=1355, num_y=1355, elbow_x=57.0, elbow_y=3.0
genus=alloprevotella, num_x=835, num_y=835, elbow_x=61.0, elbow_y=2.0
genus=anaerocolumna, num_x=5184, num_y=5184, elbow_x=96.0, elbow_y=2.0
genus=exiguobacterium, num_x=3243, num_y=3243, elbow_x=1215.0, elbow_y=7.0
genus=rhodobacter, num_x=13369, num_y=13369, elbow_x=2779.0, elbow_y=6.0
genus=pluralibacter, num_x=3720, num_y=3720, elbow_x=1687.0, elbow_y=5.0
genus=alkalilimnicola, num_x=1268, num_y=1268, elbow_x=52.0, elbow_y=2.0
genus=bilophila, ERROR=Optimal parameters not found: Number of calls to function has reached maxfev = 800.
genus=salegentibacter, num_x=3561, num_y=3561, elbow_x=1313.0, elbow_y=3.0
genus=labrenzia, num_x=7245, num_y=7245, elbow_x=33.0, elbow_y=8.0
genus=microvirga, num_x=5650, num_y=5650, elbow_x=42.0, elbow_y=3.0
genus=agarivorans, num_x=1766, num_y=1766, elbow_x=70.0, elbow_y=2.0
genus=porphyrobacter, num_x=3159, num_y=3159, elbow_x=1135.0, elbow_y=4.0
genus=psychromonas, num_x=2159, num_y=2159, elbow_x=529.0, elbow_y=2.0
genus=mycobacteroides, num_x=10982, num_y=10982, elbow_x=3243.0, elbow_y=20.0
genus=euzebya, num_x=2399, num_y=2399, elbow_x=50.0, elbow_y=2.0
genus=candidatus walczuchella, num_x=49, num_y=49, elbow_x=1.0, elbow_y=2.0
genus=allisonella, num_x=603, num_y=603, elbow_x=52.0, elbow_y=1.0
genus=thermobaculum, num_x=1263, num_y=1263, elbow_x=29.0, elbow_y=2.0
genus=aliiarcobacter, num_x=842, num_y=842, elbow_x=40.0, elbow_y=4.0
genus=maricaulis, num_x=2064, num_y=2064, elbow_x=937.0, elbow_y=2.0
genus=faecalibacterium, num_x=5102, num_y=5102, elbow_x=1161.0, elbow_y=4.0
genus=novispirillum, num_x=1794, num_y=1794, elbow_x=47.0, elbow_y=1.0
genus=parafilimonas, num_x=1713, num_y=1713, elbow_x=116.0, elbow_y=1.0
genus=paraoceanicella, num_x=2352, num_y=2352, elbow_x=32.0, elbow_y=2.0
genus=aquimarina, num_x=3603, num_y=3603, elbow_x=1184.0, elbow_y=3.0
genus=thiomonas, num_x=2534, num_y=2534, elbow_x=1123.0, elbow_y=3.0
genus=desulfomonile, num_x=1894, num_y=1894, elbow_x=74.0, elbow_y=2.0
genus=bifidobacterium, num_x=24035, num_y=24035, elbow_x=2013.0, elbow_y=20.0
genus=filimonas, num_x=2442, num_y=2442, elbow_x=26.0, elbow_y=2.0
genus=cupriavidus, num_x=24307, num_y=24307, elbow_x=3555.0, elbow_y=8.0
genus=allofrancisella, num_x=626, num_y=626, elbow_x=40.0, elbow_y=2.0
genus=bacteroides, num_x=12481, num_y=12481, elbow_x=2308.0, elbow_y=9.0
genus=nereida, num_x=1221, num_y=1221, elbow_x=53.0, elbow_y=2.0
genus=undibacterium, num_x=4750, num_y=4750, elbow_x=1568.0, elbow_y=3.0
genus=catenovulum, num_x=3090, num_y=3090, elbow_x=631.0, elbow_y=2.0
genus=streptobacillus, num_x=495, num_y=495, elbow_x=57.0, elbow_y=4.0
genus=pseudactinotalea, num_x=1487, num_y=1487, elbow_x=27.0, elbow_y=2.0
genus=magnetospira, num_x=1615, num_y=1615, elbow_x=11.0, elbow_y=2.0
genus=azospira, num_x=1836, num_y=1836, elbow_x=106.0, elbow_y=4.0
genus=dermabacter, num_x=1271, num_y=1271, elbow_x=627.0, elbow_y=4.0
genus=roseateles, num_x=3229, num_y=3229, elbow_x=28.0, elbow_y=2.0
genus=flammeovirga, num_x=3086, num_y=3086, elbow_x=54.0, elbow_y=3.0
genus=humibacter, num_x=3419, num_y=3419, elbow_x=40.0, elbow_y=2.0
genus=anaeroplasma, num_x=670, num_y=670, elbow_x=73.0, elbow_y=1.0
genus=dermacoccus, num_x=2340, num_y=2340, elbow_x=940.0, elbow_y=2.0
genus=amycolatopsis, num_x=18865, num_y=18865, elbow_x=3564.0, elbow_y=6.0
genus=hoyosella, num_x=2214, num_y=2214, elbow_x=135.0, elbow_y=2.0
genus=gallaecimonas, num_x=1695, num_y=1695, elbow_x=143.0, elbow_y=2.0
genus=tenacibaculum, num_x=3621, num_y=3621, elbow_x=959.0, elbow_y=4.0
genus=brevibacterium, num_x=5747, num_y=5747, elbow_x=1830.0, elbow_y=7.0
genus=streptacidiphilus, num_x=2858, num_y=2858, elbow_x=48.0, elbow_y=2.0
genus=carnobacterium, num_x=4415, num_y=4415, elbow_x=1101.0, elbow_y=5.0
genus=aerococcus, num_x=3223, num_y=3223, elbow_x=782.0, elbow_y=4.0
genus=maribius, num_x=2753, num_y=2753, elbow_x=56.0, elbow_y=2.0
genus=geodermatophilus, num_x=2274, num_y=2274, elbow_x=127.0, elbow_y=2.0
genus=candidatus mikella, num_x=37, num_y=37, elbow_x=4.0, elbow_y=2.0
genus=fructobacillus, num_x=1119, num_y=1119, elbow_x=413.0, elbow_y=2.0
genus=leminorella, num_x=1506, num_y=1506, elbow_x=147.0, elbow_y=4.0
genus=pseudodesulfovibrio, num_x=3988, num_y=3988, elbow_x=1113.0, elbow_y=2.0
genus=ancylobacter, num_x=2608, num_y=2608, elbow_x=27.0, elbow_y=2.0
genus=anaerotignum, num_x=1047, num_y=1047, elbow_x=82.0, elbow_y=1.0
genus=variibacter, num_x=2031, num_y=2031, elbow_x=47.0, elbow_y=2.0
genus=salinivibrio, num_x=1785, num_y=1785, elbow_x=82.0, elbow_y=3.0
genus=candidatus tenderia, num_x=1354, num_y=1354, elbow_x=49.0, elbow_y=1.0
genus=candidatus bipolaricaulis, num_x=772, num_y=772, elbow_x=26.0, elbow_y=2.0
genus=paucimonas, num_x=2505, num_y=2505, elbow_x=31.0, elbow_y=1.0
genus=tessaracoccus, num_x=5834, num_y=5834, elbow_x=1230.0, elbow_y=3.0
genus=neokomagataea, num_x=1480, num_y=1480, elbow_x=399.0, elbow_y=2.0
genus=apibacter, num_x=1147, num_y=1147, elbow_x=92.0, elbow_y=2.0
genus=candidatus nanopelagicus, num_x=878, num_y=878, elbow_x=396.0, elbow_y=4.0
genus=agarilytica, num_x=2282, num_y=2282, elbow_x=159.0, elbow_y=2.0
genus=maritalea, num_x=1683, num_y=1683, elbow_x=26.0, elbow_y=2.0
genus=roseimaritima, num_x=2213, num_y=2213, elbow_x=121.0, elbow_y=2.0
genus=leifsonia, num_x=11316, num_y=11316, elbow_x=2285.0, elbow_y=4.0
genus=granulicella, num_x=5996, num_y=5996, elbow_x=2031.0, elbow_y=3.0
genus=angustibacter, num_x=1748, num_y=1748, elbow_x=113.0, elbow_y=1.0
genus=hungateiclostridium, num_x=3015, num_y=3015, elbow_x=1097.0, elbow_y=3.0
genus=sodalis, num_x=4065, num_y=4065, elbow_x=1.0, elbow_y=3.0
genus=pseudolabrys, num_x=2005, num_y=2005, elbow_x=49.0, elbow_y=2.0
genus=aeromicrobium, num_x=4221, num_y=4221, elbow_x=1173.0, elbow_y=3.0
genus=aquaspirillum, num_x=2421, num_y=2421, elbow_x=999.0, elbow_y=2.0
genus=blastomonas, num_x=2186, num_y=2186, elbow_x=150.0, elbow_y=4.0
genus=methyloferula, num_x=1541, num_y=1541, elbow_x=90.0, elbow_y=1.0
genus=helicobacter, num_x=19828, num_y=19828, elbow_x=1926.0, elbow_y=26.0
genus=leptospirillum, num_x=1625, num_y=1625, elbow_x=637.0, elbow_y=4.0
genus=actinoalloteichus, num_x=6485, num_y=6485, elbow_x=47.0, elbow_y=4.0
genus=muriicola, num_x=1149, num_y=1149, elbow_x=66.0, elbow_y=2.0
genus=anseongella, num_x=1501, num_y=1501, elbow_x=115.0, elbow_y=2.0
genus=thermogutta, num_x=1243, num_y=1243, elbow_x=80.0, elbow_y=2.0
genus=oblitimonas, ERROR=Optimal parameters not found: Number of calls to function has reached maxfev = 800.
genus=chromobacterium, num_x=7452, num_y=7452, elbow_x=2384.0, elbow_y=7.0
genus=arcicella, num_x=1871, num_y=1871, elbow_x=104.0, elbow_y=1.0
genus=deferribacter, num_x=978, num_y=978, elbow_x=56.0, elbow_y=2.0
genus=salipiger, num_x=2407, num_y=2407, elbow_x=30.0, elbow_y=2.0
genus=streptomonospora, num_x=2124, num_y=2124, elbow_x=39.0, elbow_y=2.0
genus=rickettsia, num_x=2931, num_y=2931, elbow_x=732.0, elbow_y=20.0
genus=anaeromyxobacter, num_x=3908, num_y=3908, elbow_x=1541.0, elbow_y=4.0
genus=limnochorda, num_x=1471, num_y=1471, elbow_x=18.0, elbow_y=2.0
genus=calothrix, num_x=12011, num_y=12011, elbow_x=1760.0, elbow_y=3.0
genus=aquabacterium, num_x=1787, num_y=1787, elbow_x=116.0, elbow_y=2.0
genus=serratia, num_x=33314, num_y=33314, elbow_x=5081.0, elbow_y=55.0
genus=arcticibacterium, num_x=1740, num_y=1740, elbow_x=132.0, elbow_y=2.0
genus=dorea, num_x=10296, num_y=10296, elbow_x=1741.0, elbow_y=3.0
genus=zymobacter, num_x=997, num_y=997, elbow_x=32.0, elbow_y=2.0
genus=robiginitalea, num_x=1242, num_y=1242, elbow_x=20.0, elbow_y=2.0
genus=pectobacterium, num_x=6739, num_y=6739, elbow_x=2218.0, elbow_y=20.0
genus=candidatus pelagibacter, num_x=1353, num_y=1353, elbow_x=445.0, elbow_y=3.0
genus=tyzzerella, num_x=1033, num_y=1033, elbow_x=72.0, elbow_y=1.0
genus=wenzhouxiangella, num_x=1319, num_y=1319, elbow_x=62.0, elbow_y=2.0
genus=aquamicrobium, num_x=1662, num_y=1662, elbow_x=32.0, elbow_y=1.0
genus=asticcacaulis, num_x=2188, num_y=2188, elbow_x=978.0, elbow_y=3.0
genus=methylocystis, num_x=5633, num_y=5633, elbow_x=1394.0, elbow_y=3.0
genus=candidatus desulforudis, num_x=650, num_y=650, elbow_x=43.0, elbow_y=2.0
genus=gemmatimonas, num_x=2731, num_y=2731, elbow_x=82.0, elbow_y=3.0
genus=acidothermus, num_x=935, num_y=935, elbow_x=43.0, elbow_y=2.0
genus=acidovorax, num_x=9537, num_y=9537, elbow_x=2245.0, elbow_y=6.0
genus=fodinicurvata, num_x=1660, num_y=1660, elbow_x=35.0, elbow_y=1.0
genus=dialister, num_x=2385, num_y=2385, elbow_x=697.0, elbow_y=4.0
genus=saccharibacillus, num_x=2097, num_y=2097, elbow_x=107.0, elbow_y=2.0
genus=aurantimicrobium, num_x=1064, num_y=1064, elbow_x=517.0, elbow_y=4.0
genus=candidatus symbiobacter, num_x=980, num_y=980, elbow_x=57.0, elbow_y=2.0
genus=breoghania, num_x=2017, num_y=2017, elbow_x=37.0, elbow_y=2.0
genus=actinobaculum, num_x=1798, num_y=1798, elbow_x=629.0, elbow_y=2.0
genus=xylanimonas, num_x=1525, num_y=1525, elbow_x=30.0, elbow_y=2.0
genus=globicatella, num_x=974, num_y=974, elbow_x=54.0, elbow_y=2.0
genus=aquisalimonas, num_x=1724, num_y=1724, elbow_x=91.0, elbow_y=1.0
genus=aggregatibacter, num_x=2898, num_y=2898, elbow_x=1007.0, elbow_y=11.0
genus=baekduia, num_x=2310, num_y=2310, elbow_x=226.0, elbow_y=2.0
genus=devriesea, num_x=1090, num_y=1090, elbow_x=90.0, elbow_y=2.0
genus=aureimonas, num_x=2340, num_y=2340, elbow_x=25.0, elbow_y=2.0
genus=halioglobus, num_x=4185, num_y=4185, elbow_x=1276.0, elbow_y=3.0
genus=burkholderia, num_x=91221, num_y=91221, elbow_x=7132.0, elbow_y=53.0
genus=sphingopyxis, num_x=12306, num_y=12306, elbow_x=2597.0, elbow_y=5.0
genus=cyanobacterium, num_x=3263, num_y=3263, elbow_x=358.0, elbow_y=2.0
genus=agreia, num_x=2885, num_y=2885, elbow_x=34.0, elbow_y=3.0
genus=acidihalobacter, num_x=1415, num_y=1415, elbow_x=71.0, elbow_y=2.0
genus=hoeflea, num_x=2258, num_y=2258, elbow_x=36.0, elbow_y=2.0
genus=buchnera, num_x=527, num_y=527, elbow_x=191.0, elbow_y=8.0
genus=mycetohabitans, num_x=1149, num_y=1149, elbow_x=80.0, elbow_y=1.0
genus=neomicrococcus, num_x=1121, num_y=1121, elbow_x=85.0, elbow_y=2.0
genus=austwickia, num_x=1419, num_y=1419, elbow_x=89.0, elbow_y=2.0
genus=azotobacter, num_x=4507, num_y=4507, elbow_x=1792.0, elbow_y=6.0
genus=candidatus evansia, num_x=79, num_y=79, elbow_x=4.0, elbow_y=2.0
genus=rhodococcus, num_x=35357, num_y=35357, elbow_x=4514.0, elbow_y=11.0
genus=candidatus syntrophocurvum, num_x=750, num_y=750, elbow_x=31.0, elbow_y=2.0
genus=pelagirhabdus, num_x=967, num_y=967, elbow_x=67.0, elbow_y=1.0
genus=sulfuricaulis, num_x=1014, num_y=1014, elbow_x=66.0, elbow_y=2.0
genus=planktothrix, num_x=1504, num_y=1504, elbow_x=113.0, elbow_y=1.0
genus=phytobacter, num_x=3000, num_y=3000, elbow_x=123.0, elbow_y=3.0
genus=flavisolibacter, num_x=4016, num_y=4016, elbow_x=875.0, elbow_y=3.0
genus=bartonella, num_x=5267, num_y=5267, elbow_x=1055.0, elbow_y=17.0
genus=lachnobacterium, num_x=1178, num_y=1178, elbow_x=84.0, elbow_y=2.0
genus=bauldia, num_x=2251, num_y=2251, elbow_x=16.0, elbow_y=1.0
genus=selenomonas, num_x=3074, num_y=3074, elbow_x=803.0, elbow_y=3.0
genus=anderseniella, num_x=2057, num_y=2057, elbow_x=38.0, elbow_y=2.0
genus=thalassobacter, num_x=1452, num_y=1452, elbow_x=52.0, elbow_y=2.0
genus=atopostipes, num_x=764, num_y=764, elbow_x=80.0, elbow_y=1.0
genus=polaromonas, num_x=6818, num_y=6818, elbow_x=1871.0, elbow_y=3.0
genus=comamonas, num_x=9660, num_y=9660, elbow_x=2311.0, elbow_y=5.0
genus=beutenbergia, num_x=2266, num_y=2266, elbow_x=50.0, elbow_y=2.0
genus=prochlorococcus, num_x=2045, num_y=2045, elbow_x=722.0, elbow_y=8.0
genus=microterricola, num_x=1670, num_y=1670, elbow_x=32.0, elbow_y=2.0
genus=blastochloris, ERROR=Optimal parameters not found: Number of calls to function has reached maxfev = 800.
genus=kushneria, num_x=3850, num_y=3850, elbow_x=1377.0, elbow_y=3.0
genus=beijerinckia, num_x=2585, num_y=2585, elbow_x=1076.0, elbow_y=2.0
genus=thermodesulfovibrio, num_x=823, num_y=823, elbow_x=100.0, elbow_y=2.0
genus=desulfarculus, num_x=1372, num_y=1372, elbow_x=91.0, elbow_y=2.0
genus=anoxybacillus, num_x=6815, num_y=6815, elbow_x=1727.0, elbow_y=3.0
genus=bordetella, num_x=24874, num_y=24874, elbow_x=3260.0, elbow_y=152.0
genus=streptococcus, num_x=103847, num_y=103847, elbow_x=3854.0, elbow_y=125.0
genus=rathayibacter, num_x=5914, num_y=5914, elbow_x=1558.0, elbow_y=6.0
genus=acetobacter, num_x=7795, num_y=7795, elbow_x=1873.0, elbow_y=11.0
genus=brevefilum, num_x=931, num_y=931, elbow_x=51.0, elbow_y=2.0
genus=melioribacter, num_x=1132, num_y=1132, elbow_x=94.0, elbow_y=2.0
genus=gimesia, num_x=3089, num_y=3089, elbow_x=1410.0, elbow_y=4.0
genus=pseudarthrobacter, num_x=6274, num_y=6274, elbow_x=1801.0, elbow_y=5.0
genus=suicoccus, num_x=927, num_y=927, elbow_x=85.0, elbow_y=2.0
genus=dolosigranulum, num_x=613, num_y=613, elbow_x=63.0, elbow_y=2.0
genus=altererythrobacter, num_x=5998, num_y=5998, elbow_x=1357.0, elbow_y=4.0
genus=boseongicola, num_x=1839, num_y=1839, elbow_x=33.0, elbow_y=2.0
genus=thalassococcus, num_x=3385, num_y=3385, elbow_x=25.0, elbow_y=3.0
genus=chryseolinea, num_x=2675, num_y=2675, elbow_x=79.0, elbow_y=2.0
genus=wolinella, ERROR=Optimal parameters not found: Number of calls to function has reached maxfev = 800.
genus=photorhabdus, num_x=3347, num_y=3347, elbow_x=1351.0, elbow_y=7.0
genus=candidatus paracaedibacter, num_x=835, num_y=835, elbow_x=56.0, elbow_y=2.0
genus=nonomuraea, num_x=19593, num_y=19593, elbow_x=77.0, elbow_y=3.0
genus=klebsiella, num_x=131060, num_y=131060, elbow_x=6960.0, elbow_y=120.0
genus=muribaculum, num_x=952, num_y=952, elbow_x=56.0, elbow_y=1.0
genus=syntrophobacter, num_x=1458, num_y=1458, elbow_x=58.0, elbow_y=2.0
genus=filifactor, num_x=561, num_y=561, elbow_x=50.0, elbow_y=2.0
genus=basfia, ERROR=Optimal parameters not found: Number of calls to function has reached maxfev = 800.
genus=hydrogenophaga, num_x=8898, num_y=8898, elbow_x=1974.0, elbow_y=4.0
genus=brevibacillus, num_x=13709, num_y=13709, elbow_x=3144.0, elbow_y=5.0
genus=limihaloglobus, num_x=1065, num_y=1065, elbow_x=37.0, elbow_y=2.0
genus=treponema, num_x=15355, num_y=15355, elbow_x=622.0, elbow_y=4.0
genus=akkermansia, num_x=3113, num_y=3113, elbow_x=1071.0, elbow_y=22.0
genus=geobacillus, num_x=7776, num_y=7776, elbow_x=1860.0, elbow_y=10.0
genus=salilacibacter, num_x=1352, num_y=1352, elbow_x=91.0, elbow_y=2.0
genus=thiohalobacter, num_x=1170, num_y=1170, elbow_x=48.0, elbow_y=2.0
genus=brevundimonas, num_x=7123, num_y=7123, elbow_x=1715.0, elbow_y=5.0
genus=slackia, num_x=2625, num_y=2625, elbow_x=999.0, elbow_y=3.0
genus=brochothrix, ERROR=Optimal parameters not found: Number of calls to function has reached maxfev = 800.
genus=cellulosilyticum, num_x=2038, num_y=2038, elbow_x=165.0, elbow_y=3.0
genus=rhodospirillum, num_x=1761, num_y=1761, elbow_x=26.0, elbow_y=4.0
genus=desulfosarcina, num_x=7509, num_y=7509, elbow_x=1352.0, elbow_y=3.0
genus=caenimonas, num_x=2103, num_y=2103, elbow_x=63.0, elbow_y=1.0
genus=anaerostipes, num_x=3941, num_y=3941, elbow_x=1206.0, elbow_y=5.0
genus=roseburia, num_x=2386, num_y=2386, elbow_x=672.0, elbow_y=4.0
genus=streptomyces, num_x=211753, num_y=211753, elbow_x=5732.0, elbow_y=10.0
genus=buttiauxella, num_x=2071, num_y=2071, elbow_x=81.0, elbow_y=2.0
genus=vitreoscilla, num_x=1081, num_y=1081, elbow_x=130.0, elbow_y=2.0
genus=orientia, num_x=2171, num_y=2171, elbow_x=369.0, elbow_y=9.0
genus=azomonas, num_x=1301, num_y=1301, elbow_x=105.0, elbow_y=1.0
genus=thermobifida, num_x=1382, num_y=1382, elbow_x=18.0, elbow_y=2.0
genus=thermosediminibacter, num_x=762, num_y=762, elbow_x=87.0, elbow_y=2.0
genus=beggiatoa, num_x=1583, num_y=1583, elbow_x=1.0, elbow_y=8.0
genus=caldanaerobius, num_x=1043, num_y=1043, elbow_x=79.0, elbow_y=1.0
genus=silicimonas, num_x=1876, num_y=1876, elbow_x=44.0, elbow_y=2.0
genus=butyricimonas, num_x=1100, num_y=1100, elbow_x=33.0, elbow_y=2.0
genus=devosia, num_x=7201, num_y=7201, elbow_x=37.0, elbow_y=3.0
genus=oerskovia, num_x=2692, num_y=2692, elbow_x=106.0, elbow_y=3.0
genus=saccharospirillum, num_x=1687, num_y=1687, elbow_x=42.0, elbow_y=2.0
genus=calditerrivibrio, num_x=920, num_y=920, elbow_x=37.0, elbow_y=2.0
genus=caldicellulosiruptor, num_x=2692, num_y=2692, elbow_x=914.0, elbow_y=7.0
genus=cryobacterium, num_x=5833, num_y=5833, elbow_x=1473.0, elbow_y=3.0
genus=ktedonosporobacter, num_x=4525, num_y=4525, elbow_x=432.0, elbow_y=2.0
genus=actinotignum, num_x=732, num_y=732, elbow_x=49.0, elbow_y=2.0
genus=thiobacillus, num_x=1182, num_y=1182, elbow_x=46.0, elbow_y=2.0
genus=caldisericum, num_x=548, num_y=548, elbow_x=27.0, elbow_y=2.0
genus=kangiella, num_x=1944, num_y=1944, elbow_x=811.0, elbow_y=4.0
genus=caldanaerobacter, num_x=940, num_y=940, elbow_x=63.0, elbow_y=2.0
genus=aquifex, num_x=665, num_y=665, elbow_x=7.0, elbow_y=2.0
genus=acidipropionibacterium, num_x=11058, num_y=11058, elbow_x=2432.0, elbow_y=5.0
genus=promicromonospora, num_x=2374, num_y=2374, elbow_x=38.0, elbow_y=1.0
genus=leptonema, num_x=1540, num_y=1540, elbow_x=121.0, elbow_y=1.0
genus=eggerthella, num_x=3067, num_y=3067, elbow_x=25.0, elbow_y=3.0
genus=ethanoligenens, ERROR=Optimal parameters not found: Number of calls to function has reached maxfev = 800.
genus=alcanivorax, num_x=4624, num_y=4624, elbow_x=1402.0, elbow_y=4.0
genus=lacunisphaera, num_x=1497, num_y=1497, elbow_x=28.0, elbow_y=2.0
genus=antarctobacter, num_x=2262, num_y=2262, elbow_x=43.0, elbow_y=2.0
genus=staphylococcus, num_x=137448, num_y=137448, elbow_x=4276.0, elbow_y=296.0
genus=candidatus hoaglandella, num_x=175, num_y=175, elbow_x=5.0, elbow_y=2.0
genus=chitinophaga, num_x=9887, num_y=9887, elbow_x=2167.0, elbow_y=4.0
genus=candidatus accumulibacter, num_x=1955, num_y=1955, elbow_x=8.0, elbow_y=2.0
genus=candidatus azobacteroides, num_x=392, num_y=392, elbow_x=185.0, elbow_y=2.0
genus=candidatus methylospira, num_x=1495, num_y=1495, elbow_x=107.0, elbow_y=2.0
genus=niastella, num_x=2778, num_y=2778, elbow_x=39.0, elbow_y=2.0
genus=aquisphaera, num_x=2716, num_y=2716, elbow_x=206.0, elbow_y=2.0
genus=riemerella, num_x=1913, num_y=1913, elbow_x=801.0, elbow_y=11.0
genus=candidatus carsonella, num_x=80, num_y=80, elbow_x=33.0, elbow_y=7.0
genus=methylotenera, num_x=2283, num_y=2283, elbow_x=844.0, elbow_y=3.0
genus=thalassobacillus, num_x=1616, num_y=1616, elbow_x=122.0, elbow_y=1.0
genus=candidatus blochmannia, num_x=488, num_y=488, elbow_x=213.0, elbow_y=7.0
genus=candidatus promineofilum, num_x=1859, num_y=1859, elbow_x=70.0, elbow_y=2.0
genus=arcobacter, num_x=12935, num_y=12935, elbow_x=1794.0, elbow_y=6.0
genus=caulobacter, num_x=9286, num_y=9286, elbow_x=2465.0, elbow_y=6.0
genus=desulfotalea, num_x=1108, num_y=1108, elbow_x=96.0, elbow_y=2.0
genus=chlorobium, num_x=3067, num_y=3067, elbow_x=812.0, elbow_y=3.0
genus=mycolicibacterium, num_x=25233, num_y=25233, elbow_x=3811.0, elbow_y=5.0
genus=candidatus cardinium, num_x=622, num_y=622, elbow_x=152.0, elbow_y=3.0
genus=candidatus finniella, num_x=35, num_y=35, elbow_x=4.0, elbow_y=1.0
genus=candidatus doolittlea, num_x=155, num_y=155, elbow_x=1.0, elbow_y=2.0
genus=wolbachia, num_x=2217, num_y=2217, elbow_x=422.0, elbow_y=10.0
genus=dysgonomonas, num_x=2259, num_y=2259, elbow_x=271.0, elbow_y=1.0
genus=salinicoccus, num_x=1372, num_y=1372, elbow_x=135.0, elbow_y=2.0
genus=chondrocystis, num_x=1720, num_y=1720, elbow_x=123.0, elbow_y=2.0
genus=ferriphaselus, num_x=1007, num_y=1007, elbow_x=53.0, elbow_y=2.0
genus=thermincola, num_x=1215, num_y=1215, elbow_x=75.0, elbow_y=3.0
genus=kytococcus, num_x=3816, num_y=3816, elbow_x=486.0, elbow_y=2.0
genus=candidatus viridilinea, num_x=12866, num_y=12866, elbow_x=276.0, elbow_y=1.0
genus=candidatus moranella, num_x=116, num_y=116, elbow_x=1.0, elbow_y=4.0
genus=candidatus gullanella, num_x=151, num_y=151, elbow_x=5.0, elbow_y=2.0
genus=cellulosimicrobium, num_x=3669, num_y=3669, elbow_x=1532.0, elbow_y=5.0
genus=negativicoccus, num_x=511, num_y=511, elbow_x=40.0, elbow_y=2.0
genus=intrasporangium, num_x=1945, num_y=1945, elbow_x=31.0, elbow_y=4.0
genus=thauera, num_x=6172, num_y=6172, elbow_x=1609.0, elbow_y=4.0
genus=agrococcus, num_x=1398, num_y=1398, elbow_x=89.0, elbow_y=2.0
genus=cellulophaga, num_x=3430, num_y=3430, elbow_x=1268.0, elbow_y=6.0
genus=chthonomonas, num_x=1411, num_y=1411, elbow_x=91.0, elbow_y=2.0
genus=streptoalloteichus, num_x=2856, num_y=2856, elbow_x=42.0, elbow_y=1.0
genus=woeseia, num_x=1579, num_y=1579, elbow_x=83.0, elbow_y=2.0
genus=candidatus nasuia, num_x=30, num_y=30, elbow_x=13.0, elbow_y=3.0
genus=gulbenkiania, num_x=1302, num_y=1302, elbow_x=68.0, elbow_y=1.0
genus=erysipelothrix, num_x=2236, num_y=2236, elbow_x=800.0, elbow_y=17.0
genus=sedimentitalea, num_x=2158, num_y=2158, elbow_x=33.0, elbow_y=2.0
genus=heliobacterium, num_x=860, num_y=860, elbow_x=37.0, elbow_y=2.0
genus=aminipila, num_x=991, num_y=991, elbow_x=68.0, elbow_y=2.0
genus=halobacillus, num_x=3131, num_y=3131, elbow_x=1193.0, elbow_y=4.0
genus=amphibacillus, num_x=1050, num_y=1050, elbow_x=65.0, elbow_y=2.0
genus=candidatus endolissoclinum, ERROR=Optimal parameters not found: Number of calls to function has reached maxfev = 800.
genus=litoricola, num_x=1132, num_y=1132, elbow_x=37.0, elbow_y=2.0
genus=lentzea, num_x=17712, num_y=17712, elbow_x=4302.0, elbow_y=3.0
genus=candidatus paracaedimonas, num_x=721, num_y=721, elbow_x=23.0, elbow_y=1.0
genus=sulfurospirillum, num_x=3875, num_y=3875, elbow_x=1325.0, elbow_y=6.0
genus=caldimicrobium, num_x=658, num_y=658, elbow_x=30.0, elbow_y=2.0
genus=candidatus planktophila, num_x=1856, num_y=1856, elbow_x=689.0, elbow_y=9.0
genus=kroppenstedtia, num_x=1221, num_y=1221, elbow_x=62.0, elbow_y=1.0
genus=kordiimonas, num_x=1698, num_y=1698, elbow_x=113.0, elbow_y=1.0
genus=ekhidna, num_x=1368, num_y=1368, elbow_x=103.0, elbow_y=1.0
genus=siansivirga, num_x=1069, num_y=1069, elbow_x=47.0, elbow_y=2.0
genus=dietzia, num_x=5745, num_y=5745, elbow_x=1835.0, elbow_y=5.0
genus=thermosporothrix, num_x=2603, num_y=2603, elbow_x=266.0, elbow_y=1.0
genus=hymenobacter, num_x=10425, num_y=10425, elbow_x=1949.0, elbow_y=4.0
genus=leucobacter, num_x=2226, num_y=2226, elbow_x=47.0, elbow_y=3.0
genus=candidatus purcelliella, num_x=119, num_y=119, elbow_x=9.0, elbow_y=2.0
genus=candidatus kinetoplastibacterium, num_x=550, num_y=550, elbow_x=251.0, elbow_y=8.0
genus=candidatus portiera, num_x=105, num_y=105, elbow_x=50.0, elbow_y=10.0
genus=mobiluncus, num_x=766, num_y=766, elbow_x=85.0, elbow_y=2.0
genus=desulfoglaeba, num_x=1000, num_y=1000, elbow_x=59.0, elbow_y=2.0
genus=synechocystis, num_x=3732, num_y=3732, elbow_x=1514.0, elbow_y=7.0
genus=nitrobacter, num_x=2212, num_y=2212, elbow_x=7.0, elbow_y=3.0
genus=aurantimonas, num_x=4366, num_y=4366, elbow_x=35.0, elbow_y=1.0
genus=salinispora, num_x=13239, num_y=13239, elbow_x=3206.0, elbow_y=8.0
genus=bacillus, num_x=135755, num_y=135755, elbow_x=7875.0, elbow_y=34.0
genus=chelativorans, num_x=2065, num_y=2065, elbow_x=29.0, elbow_y=2.0
genus=miniimonas, num_x=1416, num_y=1416, elbow_x=25.0, elbow_y=2.0
genus=candidatus kuenenia, num_x=1334, num_y=1334, elbow_x=13.0, elbow_y=2.0
genus=parascardovia, num_x=668, num_y=668, elbow_x=76.0, elbow_y=2.0
genus=glutamicibacter, num_x=3969, num_y=3969, elbow_x=1347.0, elbow_y=5.0
genus=fischerella, num_x=1906, num_y=1906, elbow_x=172.0, elbow_y=4.0
genus=ketogulonicigenium, num_x=2211, num_y=2211, elbow_x=28.0, elbow_y=9.0
genus=candidatus solibacter, num_x=3150, num_y=3150, elbow_x=122.0, elbow_y=2.0
genus=limnohabitans, num_x=9931, num_y=9931, elbow_x=2120.0, elbow_y=3.0
genus=thiocapsa, num_x=1734, num_y=1734, elbow_x=19.0, elbow_y=1.0
genus=desulfocapsa, num_x=1379, num_y=1379, elbow_x=70.0, elbow_y=2.0
genus=caproiciproducens, num_x=1193, num_y=1193, elbow_x=75.0, elbow_y=2.0
genus=chlorobaculum, num_x=1550, num_y=1550, elbow_x=636.0, elbow_y=3.0
genus=trichormus, num_x=5174, num_y=5174, elbow_x=6.0, elbow_y=3.0
genus=raoultella, num_x=7058, num_y=7058, elbow_x=2463.0, elbow_y=12.0
genus=rhodopirellula, num_x=1853, num_y=1853, elbow_x=99.0, elbow_y=2.0
genus=finegoldia, num_x=2056, num_y=2056, elbow_x=670.0, elbow_y=3.0
genus=hydrogenimonas, num_x=1443, num_y=1443, elbow_x=498.0, elbow_y=1.0
genus=campylobacter, num_x=111940, num_y=111940, elbow_x=3285.0, elbow_y=145.0
genus=lysinimonas, num_x=1862, num_y=1862, elbow_x=574.0, elbow_y=3.0
genus=candidatus tachikawaea, num_x=185, num_y=185, elbow_x=7.0, elbow_y=2.0
genus=marinovum, num_x=2310, num_y=2310, elbow_x=29.0, elbow_y=2.0
genus=aromatoleum, num_x=1732, num_y=1732, elbow_x=91.0, elbow_y=2.0
genus=conexibacter, num_x=2922, num_y=2922, elbow_x=30.0, elbow_y=2.0
genus=pseudothermotoga, num_x=1780, num_y=1780, elbow_x=24.0, elbow_y=5.0
genus=acetobacterium, num_x=1444, num_y=1444, elbow_x=60.0, elbow_y=2.0
genus=mitsuaria, num_x=2491, num_y=2491, elbow_x=102.0, elbow_y=2.0
genus=marinobacter, num_x=10949, num_y=10949, elbow_x=2433.0, elbow_y=6.0
genus=acaryochloris, num_x=2588, num_y=2588, elbow_x=237.0, elbow_y=2.0
genus=prosthecochloris, num_x=2240, num_y=2240, elbow_x=706.0, elbow_y=3.0
genus=lautropia, num_x=1139, num_y=1139, elbow_x=72.0, elbow_y=2.0
genus=candidatus nitrosoglobus, num_x=763, num_y=763, elbow_x=35.0, elbow_y=2.0
genus=archangium, num_x=3952, num_y=3952, elbow_x=219.0, elbow_y=3.0
genus=pradoshia, num_x=1490, num_y=1490, elbow_x=127.0, elbow_y=2.0
genus=coprobacter, num_x=1064, num_y=1064, elbow_x=53.0, elbow_y=1.0
genus=caldithrix, num_x=1451, num_y=1451, elbow_x=21.0, elbow_y=2.0
genus=desulfobulbus, num_x=2006, num_y=2006, elbow_x=6.0, elbow_y=2.0
genus=castellaniella, num_x=1716, num_y=1716, elbow_x=21.0, elbow_y=2.0
genus=ornithinimicrobium, num_x=3802, num_y=3802, elbow_x=685.0, elbow_y=3.0
genus=sphaerobacter, num_x=1574, num_y=1574, elbow_x=22.0, elbow_y=2.0
genus=geminocystis, num_x=2939, num_y=2939, elbow_x=1040.0, elbow_y=3.0
genus=sanguibacter, num_x=3746, num_y=3746, elbow_x=59.0, elbow_y=2.0
genus=roseovarius, num_x=6456, num_y=6456, elbow_x=1507.0, elbow_y=5.0
genus=delftia, num_x=4536, num_y=4536, elbow_x=36.0, elbow_y=8.0
genus=candidatus protochlamydia, num_x=768, num_y=768, elbow_x=71.0, elbow_y=2.0
genus=pandoraea, num_x=9700, num_y=9700, elbow_x=2890.0, elbow_y=13.0
genus=roseinatronobacter, num_x=1454, num_y=1454, elbow_x=48.0, elbow_y=1.0
genus=taylorella, ERROR=Optimal parameters not found: Number of calls to function has reached maxfev = 800.
genus=cutibacterium, num_x=3420, num_y=3420, elbow_x=1163.0, elbow_y=40.0
genus=catenulispora, num_x=4282, num_y=4282, elbow_x=113.0, elbow_y=2.0
genus=runella, num_x=6240, num_y=6240, elbow_x=1834.0, elbow_y=2.0
genus=sedimenticola, num_x=1565, num_y=1565, elbow_x=66.0, elbow_y=2.0
genus=halomicronema, num_x=1742, num_y=1742, elbow_x=87.0, elbow_y=4.0
genus=phaeobacter, num_x=7268, num_y=7268, elbow_x=2309.0, elbow_y=22.0
genus=atlantibacter, num_x=2303, num_y=2303, elbow_x=218.0, elbow_y=3.0
genus=sphingomonas, num_x=48759, num_y=48759, elbow_x=3381.0, elbow_y=4.0
genus=neisseria, num_x=25134, num_y=25134, elbow_x=2413.0, elbow_y=34.0
genus=hathewaya, num_x=907, num_y=907, elbow_x=100.0, elbow_y=2.0
genus=draconibacterium, num_x=1674, num_y=1674, elbow_x=87.0, elbow_y=3.0
genus=thermodesulfobacterium, num_x=1158, num_y=1158, elbow_x=450.0, elbow_y=3.0
genus=ureibacillus, num_x=1194, num_y=1194, elbow_x=75.0, elbow_y=2.0
genus=halotalea, num_x=1898, num_y=1898, elbow_x=43.0, elbow_y=2.0
genus=thiobacimonas, num_x=2252, num_y=2252, elbow_x=36.0, elbow_y=1.0
genus=shimia, num_x=2801, num_y=2801, elbow_x=63.0, elbow_y=1.0
genus=thermovibrio, num_x=653, num_y=653, elbow_x=38.0, elbow_y=2.0
genus=sphingorhabdus, num_x=3513, num_y=3513, elbow_x=1229.0, elbow_y=4.0
genus=candidatus hamiltonella, num_x=588, num_y=588, elbow_x=53.0, elbow_y=2.0
genus=rhodoplanes, num_x=3280, num_y=3280, elbow_x=100.0, elbow_y=2.0
genus=propionispira, num_x=1521, num_y=1521, elbow_x=91.0, elbow_y=1.0
genus=paraeggerthella, num_x=1056, num_y=1056, elbow_x=20.0, elbow_y=1.0
genus=oceanisphaera, num_x=1683, num_y=1683, elbow_x=48.0, elbow_y=3.0
genus=morganella, num_x=5258, num_y=5258, elbow_x=1867.0, elbow_y=20.0
genus=acetomicrobium, num_x=1044, num_y=1044, elbow_x=27.0, elbow_y=3.0
genus=turneriella, num_x=1446, num_y=1446, elbow_x=7.0, elbow_y=2.0
genus=chryseobacterium, num_x=15861, num_y=15861, elbow_x=2752.0, elbow_y=10.0
genus=tannerella, num_x=1839, num_y=1839, elbow_x=767.0, elbow_y=4.0
genus=ruegeria, num_x=28671, num_y=28671, elbow_x=3827.0, elbow_y=5.0
genus=corynebacterium, num_x=41044, num_y=41044, elbow_x=2700.0, elbow_y=23.0
genus=anaerobutyricum, num_x=1149, num_y=1149, elbow_x=83.0, elbow_y=2.0
genus=chloracidobacterium, num_x=1344, num_y=1344, elbow_x=94.0, elbow_y=2.0
genus=aquitalea, num_x=3468, num_y=3468, elbow_x=1519.0, elbow_y=5.0
genus=serpentinomonas, num_x=1617, num_y=1617, elbow_x=678.0, elbow_y=3.0
genus=nautilia, num_x=1077, num_y=1077, elbow_x=520.0, elbow_y=3.0
genus=clostridium, num_x=83171, num_y=83171, elbow_x=4557.0, elbow_y=10.0
genus=janthinobacterium, num_x=15127, num_y=15127, elbow_x=3637.0, elbow_y=5.0
genus=prauserella, num_x=7040, num_y=7040, elbow_x=1990.0, elbow_y=4.0
genus=auritidibacter, num_x=1046, num_y=1046, elbow_x=51.0, elbow_y=2.0
genus=wenyingzhuangia, num_x=1041, num_y=1041, elbow_x=52.0, elbow_y=2.0
genus=pseudogulbenkiania, num_x=1967, num_y=1967, elbow_x=142.0, elbow_y=2.0
genus=tepidibacter, num_x=1196, num_y=1196, elbow_x=449.0, elbow_y=1.0
genus=teredinibacter, num_x=1680, num_y=1680, elbow_x=72.0, elbow_y=2.0
genus=xenorhabdus, num_x=5011, num_y=5011, elbow_x=1436.0, elbow_y=4.0
genus=parvibaculum, num_x=1869, num_y=1869, elbow_x=169.0, elbow_y=2.0
genus=lawsonia, num_x=596, num_y=596, elbow_x=4.0, elbow_y=4.0
genus=pseudonocardia, num_x=14675, num_y=14675, elbow_x=3279.0, elbow_y=4.0
genus=bibersteinia, ERROR=Optimal parameters not found: Number of calls to function has reached maxfev = 800.
genus=salimicrobium, num_x=1080, num_y=1080, elbow_x=105.0, elbow_y=2.0
genus=blastococcus, num_x=1998, num_y=1998, elbow_x=35.0, elbow_y=2.0
genus=arcanobacterium, num_x=799, num_y=799, elbow_x=57.0, elbow_y=4.0
genus=cronobacter, num_x=9509, num_y=9509, elbow_x=2582.0, elbow_y=13.0
genus=geoalkalibacter, num_x=2075, num_y=2075, elbow_x=865.0, elbow_y=2.0
genus=lactonifactor, num_x=2075, num_y=2075, elbow_x=160.0, elbow_y=1.0
genus=aliivibrio, num_x=4006, num_y=4006, elbow_x=1482.0, elbow_y=5.0
genus=alloiococcus, num_x=622, num_y=622, elbow_x=43.0, elbow_y=1.0
genus=tolumonas, num_x=1346, num_y=1346, elbow_x=30.0, elbow_y=2.0
genus=planomicrobium, num_x=3391, num_y=3391, elbow_x=910.0, elbow_y=2.0
genus=thalassolituus, num_x=1826, num_y=1826, elbow_x=79.0, elbow_y=5.0
genus=symbiobacterium, num_x=1245, num_y=1245, elbow_x=27.0, elbow_y=2.0
genus=citrobacter, num_x=19283, num_y=19283, elbow_x=3729.0, elbow_y=33.0
genus=limimonas, num_x=1278, num_y=1278, elbow_x=43.0, elbow_y=1.0
genus=thioalkalivibrio, num_x=3921, num_y=3921, elbow_x=1009.0, elbow_y=3.0
genus=edwardsiella, num_x=3432, num_y=3432, elbow_x=1414.0, elbow_y=13.0
genus=butyrivibrio, num_x=2234, num_y=2234, elbow_x=596.0, elbow_y=2.0
genus=candidatus arthromitus, ERROR=Optimal parameters not found: Number of calls to function has reached maxfev = 800.
genus=blautia, num_x=6684, num_y=6684, elbow_x=808.0, elbow_y=4.0
genus=dehalobacter, num_x=3666, num_y=3666, elbow_x=1199.0, elbow_y=4.0
genus=pseudorhodoferax, num_x=6207, num_y=6207, elbow_x=50.0, elbow_y=2.0
genus=litorilituus, num_x=1559, num_y=1559, elbow_x=62.0, elbow_y=2.0
genus=candidatus fukatsuia, num_x=901, num_y=901, elbow_x=56.0, elbow_y=2.0
genus=thiolapillus, num_x=1172, num_y=1172, elbow_x=64.0, elbow_y=2.0
genus=verrucosispora, num_x=2744, num_y=2744, elbow_x=37.0, elbow_y=2.0
genus=candidatus methylomirabilis, num_x=946, num_y=946, elbow_x=53.0, elbow_y=1.0
genus=cloacibacterium, num_x=981, num_y=981, elbow_x=35.0, elbow_y=3.0
genus=pelagibaca, num_x=2270, num_y=2270, elbow_x=31.0, elbow_y=2.0
genus=actinomadura, num_x=13038, num_y=13038, elbow_x=43.0, elbow_y=2.0
genus=mesoplasma, num_x=519, num_y=519, elbow_x=140.0, elbow_y=11.0
genus=desulfohalobium, num_x=1005, num_y=1005, elbow_x=54.0, elbow_y=2.0
genus=cnuibacter, num_x=1948, num_y=1948, elbow_x=13.0, elbow_y=2.0
genus=candidatus phytoplasma, num_x=372, num_y=372, elbow_x=115.0, elbow_y=5.0
genus=candidatus peribacter, num_x=285, num_y=285, elbow_x=20.0, elbow_y=5.0
genus=duncaniella, num_x=952, num_y=952, elbow_x=66.0, elbow_y=2.0
genus=micavibrio, ERROR=Optimal parameters not found: Number of calls to function has reached maxfev = 800.
genus=cobetia, num_x=2125, num_y=2125, elbow_x=104.0, elbow_y=4.0
genus=oenococcus, num_x=1692, num_y=1692, elbow_x=660.0, elbow_y=6.0
genus=haemophilus, num_x=14302, num_y=14302, elbow_x=1884.0, elbow_y=28.0
genus=erwinia, num_x=7729, num_y=7729, elbow_x=2147.0, elbow_y=10.0
genus=azospirillum, num_x=10566, num_y=10566, elbow_x=41.0, elbow_y=5.0
genus=acidiferrobacter, num_x=1217, num_y=1217, elbow_x=108.0, elbow_y=2.0
genus=trueperella, num_x=3850, num_y=3850, elbow_x=1174.0, elbow_y=7.0
genus=desulfurobacterium, num_x=617, num_y=617, elbow_x=54.0, elbow_y=2.0
genus=geitlerinema, num_x=1535, num_y=1535, elbow_x=110.0, elbow_y=2.0
genus=dechloromonas, num_x=2393, num_y=2393, elbow_x=872.0, elbow_y=3.0
genus=changchengzhania, num_x=1462, num_y=1462, elbow_x=111.0, elbow_y=2.0
genus=microbulbifer, num_x=7520, num_y=7520, elbow_x=1856.0, elbow_y=4.0
genus=peptoclostridium, num_x=1078, num_y=1078, elbow_x=103.0, elbow_y=2.0
genus=izhakiella, num_x=2018, num_y=2018, elbow_x=156.0, elbow_y=2.0
genus=collimonas, num_x=6184, num_y=6184, elbow_x=2079.0, elbow_y=6.0
genus=dichelobacter, num_x=557, num_y=557, elbow_x=30.0, elbow_y=2.0
genus=rubrivivax, num_x=2250, num_y=2250, elbow_x=133.0, elbow_y=2.0
genus=jonesia, num_x=1108, num_y=1108, elbow_x=82.0, elbow_y=6.0
genus=bhargavaea, num_x=1641, num_y=1641, elbow_x=92.0, elbow_y=2.0
genus=veillonella, num_x=4394, num_y=4394, elbow_x=1095.0, elbow_y=6.0
genus=enterobacteriaceae, num_x=4888, num_y=4888, elbow_x=1951.0, elbow_y=5.0
genus=niveispirillum, num_x=2566, num_y=2566, elbow_x=223.0, elbow_y=2.0
genus=sandaracinus, num_x=3263, num_y=3263, elbow_x=228.0, elbow_y=2.0
genus=chania, num_x=2023, num_y=2023, elbow_x=42.0, elbow_y=2.0
genus=eggerthellaceae, num_x=453, num_y=453, elbow_x=32.0, elbow_y=1.0
genus=parashewanella, num_x=2381, num_y=2381, elbow_x=613.0, elbow_y=3.0
genus=ehrlichia, ERROR=Optimal parameters not found: Number of calls to function has reached maxfev = 800.
genus=candidatus cyclonatronum, num_x=1106, num_y=1106, elbow_x=42.0, elbow_y=2.0
genus=kosakonia, num_x=5023, num_y=5023, elbow_x=1870.0, elbow_y=10.0
genus=poseidonocella, num_x=2342, num_y=2342, elbow_x=40.0, elbow_y=1.0
genus=kluyvera, num_x=9138, num_y=9138, elbow_x=2604.0, elbow_y=7.0
genus=lysinibacillus, num_x=9512, num_y=9512, elbow_x=2309.0, elbow_y=6.0
genus=colwellia, num_x=7232, num_y=7232, elbow_x=1664.0, elbow_y=4.0
genus=filomicrobium, num_x=1480, num_y=1480, elbow_x=103.0, elbow_y=4.0
genus=leuconostoc, num_x=5353, num_y=5353, elbow_x=1307.0, elbow_y=16.0
genus=acidisphaera, num_x=1612, num_y=1612, elbow_x=10.0, elbow_y=2.0
genus=paenarthrobacter, num_x=2297, num_y=2297, elbow_x=168.0, elbow_y=2.0
genus=chroococcidiopsis, num_x=2381, num_y=2381, elbow_x=197.0, elbow_y=2.0
genus=eubacterium, num_x=3500, num_y=3500, elbow_x=22.0, elbow_y=5.0
genus=ramlibacter, num_x=4694, num_y=4694, elbow_x=35.0, elbow_y=2.0
genus=pelistega, num_x=928, num_y=928, elbow_x=70.0, elbow_y=2.0
genus=qipengyuania, num_x=1026, num_y=1026, elbow_x=53.0, elbow_y=2.0
genus=fontibacter, num_x=1552, num_y=1552, elbow_x=74.0, elbow_y=1.0
genus=shewanella, num_x=19883, num_y=19883, elbow_x=3148.0, elbow_y=8.0
genus=corallococcus, num_x=4067, num_y=4067, elbow_x=268.0, elbow_y=3.0
genus=luteimonas, num_x=3564, num_y=3564, elbow_x=1073.0, elbow_y=4.0
genus=methylomusa, num_x=1540, num_y=1540, elbow_x=41.0, elbow_y=2.0
genus=enterococcus, num_x=47298, num_y=47298, elbow_x=3643.0, elbow_y=44.0
genus=seonamhaeicola, num_x=1255, num_y=1255, elbow_x=77.0, elbow_y=2.0
genus=fermentimonas, num_x=963, num_y=963, elbow_x=29.0, elbow_y=2.0
genus=dehalococcoides, num_x=1140, num_y=1140, elbow_x=478.0, elbow_y=24.0
genus=propionimicrobium, num_x=756, num_y=756, elbow_x=21.0, elbow_y=2.0
genus=sediminispirochaeta, num_x=1853, num_y=1853, elbow_x=10.0, elbow_y=2.0
genus=gilliamella, num_x=1144, num_y=1144, elbow_x=6.0, elbow_y=2.0
genus=rubrobacter, num_x=3370, num_y=3370, elbow_x=946.0, elbow_y=3.0
genus=tatlockia, num_x=1423, num_y=1423, elbow_x=52.0, elbow_y=5.0
genus=curtobacterium, num_x=4156, num_y=4156, elbow_x=1242.0, elbow_y=4.0
genus=lutibacter, num_x=3748, num_y=3748, elbow_x=1030.0, elbow_y=2.0
genus=ferrovibrio, num_x=2174, num_y=2174, elbow_x=29.0, elbow_y=2.0
genus=thermoactinomyces, num_x=934, num_y=934, elbow_x=62.0, elbow_y=4.0
genus=asanoa, num_x=5426, num_y=5426, elbow_x=61.0, elbow_y=2.0
genus=desulfurivibrio, num_x=1074, num_y=1074, elbow_x=88.0, elbow_y=2.0
genus=herpetosiphon, num_x=2375, num_y=2375, elbow_x=228.0, elbow_y=1.0
genus=truepera, num_x=1309, num_y=1309, elbow_x=27.0, elbow_y=2.0
genus=aeromonas, num_x=25296, num_y=25296, elbow_x=4002.0, elbow_y=30.0
genus=luteipulveratus, num_x=2565, num_y=2565, elbow_x=50.0, elbow_y=2.0
genus=thermobispora, num_x=1648, num_y=1648, elbow_x=96.0, elbow_y=2.0
genus=listeria, num_x=41634, num_y=41634, elbow_x=3703.0, elbow_y=272.0
genus=cyanobium, num_x=2073, num_y=2073, elbow_x=814.0, elbow_y=3.0
genus=thioflavicoccus, num_x=1280, num_y=1280, elbow_x=74.0, elbow_y=2.0
genus=mucilaginibacter, num_x=18504, num_y=18504, elbow_x=3080.0, elbow_y=4.0
genus=halothermothrix, num_x=887, num_y=887, elbow_x=53.0, elbow_y=2.0
genus=salinispira, num_x=1412, num_y=1412, elbow_x=7.0, elbow_y=2.0
genus=flavihumibacter, num_x=1298, num_y=1298, elbow_x=132.0, elbow_y=2.0
genus=mesonia, num_x=1664, num_y=1664, elbow_x=612.0, elbow_y=1.0
genus=celeribacter, num_x=6801, num_y=6801, elbow_x=1526.0, elbow_y=4.0
genus=lacimicrobium, num_x=1661, num_y=1661, elbow_x=19.0, elbow_y=2.0
genus=cohnella, num_x=4244, num_y=4244, elbow_x=95.0, elbow_y=3.0
genus=thermosulfidibacter, num_x=746, num_y=746, elbow_x=48.0, elbow_y=2.0
genus=methylosinus, num_x=4424, num_y=4424, elbow_x=1467.0, elbow_y=3.0
genus=budvicia, num_x=1859, num_y=1859, elbow_x=142.0, elbow_y=1.0
genus=pelotomaculum, num_x=957, num_y=957, elbow_x=61.0, elbow_y=1.0
genus=gynuella, num_x=2226, num_y=2226, elbow_x=25.0, elbow_y=2.0
genus=defluviimonas, num_x=4756, num_y=4756, elbow_x=43.0, elbow_y=2.0
genus=stanieria, num_x=3009, num_y=3009, elbow_x=1270.0, elbow_y=3.0
genus=tepidiforma, num_x=1245, num_y=1245, elbow_x=7.0, elbow_y=2.0
genus=neoasaia, num_x=1419, num_y=1419, elbow_x=73.0, elbow_y=2.0
genus=flintibacter, num_x=1163, num_y=1163, elbow_x=105.0, elbow_y=2.0
genus=vibrio, num_x=104832, num_y=104832, elbow_x=5748.0, elbow_y=76.0
genus=algibacter, num_x=2763, num_y=2763, elbow_x=928.0, elbow_y=3.0
genus=desulfopila, num_x=1959, num_y=1959, elbow_x=78.0, elbow_y=1.0
genus=dactylococcopsis, num_x=1143, num_y=1143, elbow_x=76.0, elbow_y=2.0
genus=arsenicicoccus, num_x=1549, num_y=1549, elbow_x=88.0, elbow_y=2.0
genus=lacinutrix, num_x=2198, num_y=2198, elbow_x=841.0, elbow_y=3.0
genus=oceanicola, num_x=1732, num_y=1732, elbow_x=37.0, elbow_y=2.0
genus=vulgatibacter, num_x=1439, num_y=1439, elbow_x=103.0, elbow_y=2.0
genus=candidatus ishikawaella, num_x=184, num_y=184, elbow_x=10.0, elbow_y=1.0
genus=candidatus babela, num_x=285, num_y=285, elbow_x=64.0, elbow_y=2.0
genus=hasllibacter, num_x=1190, num_y=1190, elbow_x=79.0, elbow_y=1.0
genus=rhodobaca, num_x=1535, num_y=1535, elbow_x=51.0, elbow_y=2.0
genus=lysinimicrobium, num_x=1240, num_y=1240, elbow_x=34.0, elbow_y=1.0
genus=desulfatibacillum, num_x=2211, num_y=2211, elbow_x=145.0, elbow_y=2.0
genus=allochromatium, num_x=1283, num_y=1283, elbow_x=78.0, elbow_y=2.0
genus=asaia, num_x=1290, num_y=1290, elbow_x=66.0, elbow_y=2.0
genus=antarcticibacterium, num_x=1962, num_y=1962, elbow_x=721.0, elbow_y=3.0
genus=fontibacillus, num_x=2068, num_y=2068, elbow_x=94.0, elbow_y=1.0
genus=deinococcus, num_x=14798, num_y=14798, elbow_x=1678.0, elbow_y=4.0
genus=lonsdalea, num_x=1513, num_y=1513, elbow_x=38.0, elbow_y=2.0
genus=iodobacter, num_x=1381, num_y=1381, elbow_x=65.0, elbow_y=2.0
genus=nodularia, num_x=1615, num_y=1615, elbow_x=142.0, elbow_y=2.0
genus=zhongshania, num_x=1705, num_y=1705, elbow_x=112.0, elbow_y=2.0
genus=gardnerella, num_x=4915, num_y=4915, elbow_x=905.0, elbow_y=5.0
genus=singulisphaera, num_x=2578, num_y=2578, elbow_x=193.0, elbow_y=2.0
genus=mycolicibacter, num_x=2933, num_y=2933, elbow_x=310.0, elbow_y=2.0
genus=denitrobacterium, num_x=770, num_y=770, elbow_x=13.0, elbow_y=2.0
genus=diaphorobacter, num_x=1743, num_y=1743, elbow_x=105.0, elbow_y=2.0
genus=saprospira, num_x=1034, num_y=1034, elbow_x=59.0, elbow_y=2.0
genus=caminibacter, num_x=764, num_y=764, elbow_x=37.0, elbow_y=2.0
genus=cloacibacillus, num_x=1194, num_y=1194, elbow_x=58.0, elbow_y=2.0
genus=psychroserpens, num_x=1308, num_y=1308, elbow_x=66.0, elbow_y=2.0
genus=frateuria, num_x=3948, num_y=3948, elbow_x=1232.0, elbow_y=2.0
genus=geotoga, num_x=809, num_y=809, elbow_x=43.0, elbow_y=1.0
genus=arenitalea, num_x=1221, num_y=1221, elbow_x=77.0, elbow_y=1.0
genus=sporolactobacillus, num_x=1474, num_y=1474, elbow_x=31.0, elbow_y=5.0
genus=clostridioides, num_x=30680, num_y=30680, elbow_x=3604.0, elbow_y=116.0
genus=denitrovibrio, num_x=1370, num_y=1370, elbow_x=75.0, elbow_y=2.0
genus=nitrosococcus, num_x=2722, num_y=2722, elbow_x=926.0, elbow_y=4.0
genus=sporosarcina, num_x=4888, num_y=4888, elbow_x=1360.0, elbow_y=5.0
genus=friedmanniella, num_x=2250, num_y=2250, elbow_x=134.0, elbow_y=1.0
genus=desulfuromusa, num_x=1342, num_y=1342, elbow_x=66.0, elbow_y=1.0
genus=thermodesulfobium, ERROR=Optimal parameters not found: Number of calls to function has reached maxfev = 800.
genus=lentibacter, num_x=1480, num_y=1480, elbow_x=32.0, elbow_y=1.0
genus=sulfuricurvum, num_x=1224, num_y=1224, elbow_x=79.0, elbow_y=2.0
genus=defluviitoga, num_x=767, num_y=767, elbow_x=17.0, elbow_y=2.0
genus=brucella, num_x=11373, num_y=11373, elbow_x=2556.0, elbow_y=160.0
genus=candidatus phycorickettsia, num_x=559, num_y=559, elbow_x=70.0, elbow_y=2.0
genus=desulfobacca, num_x=1059, num_y=1059, elbow_x=87.0, elbow_y=2.0
genus=polaribacter, num_x=4136, num_y=4136, elbow_x=1189.0, elbow_y=4.0
genus=arsenophonus, num_x=1777, num_y=1777, elbow_x=130.0, elbow_y=3.0
genus=marinithermus, num_x=1001, num_y=1001, elbow_x=68.0, elbow_y=2.0
genus=candidatus cloacimonas, num_x=620, num_y=620, elbow_x=35.0, elbow_y=2.0
genus=ahniella, num_x=1725, num_y=1725, elbow_x=24.0, elbow_y=2.0
genus=fabibacter, num_x=1522, num_y=1522, elbow_x=107.0, elbow_y=2.0
genus=fusicatenibacter, num_x=4689, num_y=4689, elbow_x=113.0, elbow_y=2.0
genus=collinsella, num_x=2346, num_y=2346, elbow_x=847.0, elbow_y=6.0
genus=nocardia, num_x=31481, num_y=31481, elbow_x=4224.0, elbow_y=6.0
genus=dyella, num_x=4729, num_y=4729, elbow_x=1297.0, elbow_y=3.0
genus=desulfobacula, num_x=2177, num_y=2177, elbow_x=186.0, elbow_y=2.0
genus=tindallia, num_x=1382, num_y=1382, elbow_x=55.0, elbow_y=2.0
genus=dictyoglomus, num_x=910, num_y=910, elbow_x=16.0, elbow_y=3.0
genus=aminobacterium, num_x=673, num_y=673, elbow_x=35.0, elbow_y=2.0
genus=candidatus tremblaya, num_x=76, num_y=76, elbow_x=24.0, elbow_y=3.0
genus=isobaculum, num_x=1075, num_y=1075, elbow_x=99.0, elbow_y=1.0
genus=metakosakonia, num_x=2427, num_y=2427, elbow_x=101.0, elbow_y=2.0
genus=dermatophilus, num_x=995, num_y=995, elbow_x=50.0, elbow_y=2.0
genus=gemmata, num_x=2200, num_y=2200, elbow_x=140.0, elbow_y=2.0
genus=desulfomicrobium, num_x=3166, num_y=3166, elbow_x=991.0, elbow_y=3.0
genus=pelomonas, num_x=5011, num_y=5011, elbow_x=1715.0, elbow_y=3.0
genus=tropicibacter, num_x=3219, num_y=3219, elbow_x=32.0, elbow_y=2.0
genus=megamonas, num_x=816, num_y=816, elbow_x=42.0, elbow_y=2.0
genus=persephonella, num_x=749, num_y=749, elbow_x=42.0, elbow_y=2.0
genus=emticicia, num_x=1884, num_y=1884, elbow_x=103.0, elbow_y=1.0
genus=methylovorus, num_x=1371, num_y=1371, elbow_x=102.0, elbow_y=4.0
genus=mycoavidus, num_x=781, num_y=781, elbow_x=42.0, elbow_y=2.0
genus=ezakiella, num_x=647, num_y=647, elbow_x=51.0, elbow_y=2.0
genus=fictibacillus, num_x=2553, num_y=2553, elbow_x=963.0, elbow_y=3.0
genus=gibbsiella, num_x=2307, num_y=2307, elbow_x=47.0, elbow_y=2.0
genus=zoogloea, num_x=243, num_y=243, elbow_x=16.0, elbow_y=1.0
genus=psychromicrobium, num_x=1730, num_y=1730, elbow_x=119.0, elbow_y=2.0
genus=fimbriimonas, num_x=1783, num_y=1783, elbow_x=73.0, elbow_y=2.0
genus=owenweeksia, num_x=1368, num_y=1368, elbow_x=15.0, elbow_y=2.0
genus=ochrobactrum, num_x=4726, num_y=4726, elbow_x=37.0, elbow_y=7.0
genus=bradyrhizobium, num_x=27722, num_y=27722, elbow_x=4444.0, elbow_y=10.0
genus=mahella, num_x=1059, num_y=1059, elbow_x=80.0, elbow_y=2.0
genus=oleiphilus, num_x=2449, num_y=2449, elbow_x=114.0, elbow_y=2.0
genus=glycocaulis, num_x=1277, num_y=1277, elbow_x=120.0, elbow_y=2.0
genus=pontibacter, num_x=5631, num_y=5631, elbow_x=1613.0, elbow_y=4.0
genus=rhizobium, num_x=66775, num_y=66775, elbow_x=4667.0, elbow_y=14.0
genus=tamlana, num_x=1216, num_y=1216, elbow_x=70.0, elbow_y=2.0
genus=desulfovibrio, num_x=15763, num_y=15763, elbow_x=1464.0, elbow_y=3.0
genus=candidatus profftella, num_x=84, num_y=84, elbow_x=1.0, elbow_y=4.0
genus=jeongeupia, num_x=1738, num_y=1738, elbow_x=152.0, elbow_y=2.0
genus=edaphobacillus, num_x=1120, num_y=1120, elbow_x=16.0, elbow_y=1.0
genus=frankia, num_x=9803, num_y=9803, elbow_x=1345.0, elbow_y=3.0
genus=sediminimonas, num_x=1586, num_y=1586, elbow_x=56.0, elbow_y=1.0
genus=sulfurivermis, num_x=1185, num_y=1185, elbow_x=64.0, elbow_y=2.0
genus=gottschalkia, num_x=1441, num_y=1441, elbow_x=148.0, elbow_y=2.0
genus=propionispora, num_x=1970, num_y=1970, elbow_x=122.0, elbow_y=2.0
genus=methylorubrum, num_x=5301, num_y=5301, elbow_x=2028.0, elbow_y=8.0
genus=thermocrinis, num_x=1230, num_y=1230, elbow_x=281.0, elbow_y=2.0
genus=tumebacillus, num_x=2357, num_y=2357, elbow_x=118.0, elbow_y=3.0
genus=crinalium, num_x=1709, num_y=1709, elbow_x=164.0, elbow_y=2.0
genus=desulfuromonas, num_x=2369, num_y=2369, elbow_x=808.0, elbow_y=3.0
genus=muricauda, num_x=1946, num_y=1946, elbow_x=646.0, elbow_y=3.0
genus=bacteriovorax, num_x=1495, num_y=1495, elbow_x=108.0, elbow_y=4.0
genus=aneurinibacillus, num_x=2273, num_y=2273, elbow_x=653.0, elbow_y=2.0
genus=candidatus xiphinematobacter, num_x=282, num_y=282, elbow_x=11.0, elbow_y=2.0
genus=micromonospora, num_x=7700, num_y=7700, elbow_x=2504.0, elbow_y=6.0
genus=geosporobacter, num_x=1958, num_y=1958, elbow_x=52.0, elbow_y=2.0
genus=salmonella, num_x=290344, num_y=290344, elbow_x=7563.0, elbow_y=273.0
genus=cryptobacterium, num_x=545, num_y=545, elbow_x=32.0, elbow_y=2.0
genus=gramella, num_x=2861, num_y=2861, elbow_x=1022.0, elbow_y=4.0
genus=tetragenococcus, num_x=2528, num_y=2528, elbow_x=889.0, elbow_y=6.0
genus=ndongobacter, num_x=620, num_y=620, elbow_x=9.0, elbow_y=2.0
genus=acidaminococcus, num_x=1416, num_y=1416, elbow_x=398.0, elbow_y=3.0
genus=eikenella, num_x=1519, num_y=1519, elbow_x=564.0, elbow_y=3.0
genus=roseospirillum, num_x=1419, num_y=1419, elbow_x=83.0, elbow_y=1.0
genus=immundisolibacter, num_x=1358, num_y=1358, elbow_x=92.0, elbow_y=2.0
genus=pseudoalteromonas, num_x=18238, num_y=18238, elbow_x=2744.0, elbow_y=8.0
genus=mitsuokella, num_x=816, num_y=816, elbow_x=65.0, elbow_y=1.0
genus=acetoanaerobium, num_x=1358, num_y=1358, elbow_x=60.0, elbow_y=3.0
genus=sneathia, num_x=467, num_y=467, elbow_x=58.0, elbow_y=2.0
genus=cellvibrio, num_x=8825, num_y=8825, elbow_x=2162.0, elbow_y=3.0
genus=glaesserella, num_x=2700, num_y=2700, elbow_x=994.0, elbow_y=8.0
genus=cardiobacterium, num_x=1034, num_y=1034, elbow_x=67.0, elbow_y=2.0
genus=thermomicrobium, num_x=1149, num_y=1149, elbow_x=32.0, elbow_y=2.0
genus=herminiimonas, num_x=2291, num_y=2291, elbow_x=854.0, elbow_y=3.0
genus=gryllotalpicola, num_x=1785, num_y=1785, elbow_x=35.0, elbow_y=2.0
genus=rummeliibacillus, num_x=1305, num_y=1305, elbow_x=127.0, elbow_y=2.0
genus=nitrincola, num_x=1696, num_y=1696, elbow_x=73.0, elbow_y=2.0
genus=parageobacillus, ERROR=Optimal parameters not found: Number of calls to function has reached maxfev = 800.
genus=pseudobutyrivibrio, num_x=1305, num_y=1305, elbow_x=68.0, elbow_y=2.0
genus=desulfallas, num_x=1409, num_y=1409, elbow_x=118.0, elbow_y=2.0
genus=saccharothrix, num_x=6835, num_y=6835, elbow_x=44.0, elbow_y=3.0
genus=chloroflexus, num_x=2420, num_y=2420, elbow_x=1116.0, elbow_y=4.0
genus=elizabethkingia, num_x=9641, num_y=9641, elbow_x=2451.0, elbow_y=25.0
genus=gordonibacter, num_x=2274, num_y=2274, elbow_x=19.0, elbow_y=6.0
genus=coprobacillus, num_x=1408, num_y=1408, elbow_x=166.0, elbow_y=2.0
genus=oceanispirochaeta, num_x=1559, num_y=1559, elbow_x=23.0, elbow_y=2.0
genus=aeribacillus, num_x=1477, num_y=1477, elbow_x=60.0, elbow_y=2.0
genus=mariniflexile, num_x=1438, num_y=1438, elbow_x=110.0, elbow_y=2.0
genus=haematobacter, num_x=1843, num_y=1843, elbow_x=40.0, elbow_y=2.0
genus=sporanaerobacter, num_x=1318, num_y=1318, elbow_x=86.0, elbow_y=2.0
genus=roseiflexus, num_x=2724, num_y=2724, elbow_x=938.0, elbow_y=3.0
genus=tropheryma, num_x=257, num_y=257, elbow_x=11.0, elbow_y=4.0
genus=entomoplasma, num_x=383, num_y=383, elbow_x=35.0, elbow_y=3.0
genus=halorhodospira, num_x=1581, num_y=1581, elbow_x=641.0, elbow_y=3.0
genus=intestinimonas, num_x=1404, num_y=1404, elbow_x=89.0, elbow_y=4.0
genus=permianibacter, num_x=1637, num_y=1637, elbow_x=74.0, elbow_y=2.0
genus=emcibacter, num_x=2569, num_y=2569, elbow_x=744.0, elbow_y=3.0
genus=desulfobacterium, num_x=1910, num_y=1910, elbow_x=78.0, elbow_y=2.0
genus=candidatus riesia, num_x=214, num_y=214, elbow_x=91.0, elbow_y=2.0
genus=heliorestis, num_x=893, num_y=893, elbow_x=88.0, elbow_y=2.0
genus=providencia, num_x=7284, num_y=7284, elbow_x=2211.0, elbow_y=11.0
genus=marinobacterium, num_x=2057, num_y=2057, elbow_x=71.0, elbow_y=2.0
genus=mesorhizobium, num_x=169516, num_y=169516, elbow_x=6082.0, elbow_y=7.0
genus=candidatus puniceispirillum, num_x=1117, num_y=1117, elbow_x=49.0, elbow_y=2.0
genus=xylanimicrobium, num_x=1549, num_y=1549, elbow_x=21.0, elbow_y=2.0
genus=macrococcus, num_x=1972, num_y=1972, elbow_x=787.0, elbow_y=5.0
genus=fuerstia, num_x=2413, num_y=2413, elbow_x=607.0, elbow_y=2.0
genus=endomicrobium, num_x=675, num_y=675, elbow_x=172.0, elbow_y=2.0
genus=starkeya, num_x=2118, num_y=2118, elbow_x=22.0, elbow_y=2.0
genus=domibacillus, num_x=3765, num_y=3765, elbow_x=1088.0, elbow_y=2.0
genus=ottowia, num_x=4773, num_y=4773, elbow_x=34.0, elbow_y=2.0
genus=sideroxydans, num_x=1163, num_y=1163, elbow_x=64.0, elbow_y=2.0
genus=hydrogenophilus, num_x=944, num_y=944, elbow_x=36.0, elbow_y=2.0
genus=egicoccus, num_x=1634, num_y=1634, elbow_x=107.0, elbow_y=2.0
genus=serinicoccus, num_x=4669, num_y=4669, elbow_x=1278.0, elbow_y=4.0
genus=methyloversatilis, num_x=1599, num_y=1599, elbow_x=86.0, elbow_y=2.0
genus=nitratiruptor, num_x=825, num_y=825, elbow_x=48.0, elbow_y=2.0
genus=hartmannibacter, num_x=2336, num_y=2336, elbow_x=31.0, elbow_y=2.0
genus=georgenia, num_x=3897, num_y=3897, elbow_x=39.0, elbow_y=3.0
genus=frondihabitans, num_x=3612, num_y=3612, elbow_x=948.0, elbow_y=3.0
genus=insolitispirillum, num_x=1928, num_y=1928, elbow_x=77.0, elbow_y=1.0
genus=pleomorphomonas, num_x=2164, num_y=2164, elbow_x=23.0, elbow_y=2.0
genus=formosa, num_x=3382, num_y=3382, elbow_x=999.0, elbow_y=3.0
genus=timonella, num_x=1154, num_y=1154, elbow_x=17.0, elbow_y=1.0
genus=zunongwangia, num_x=1598, num_y=1598, elbow_x=50.0, elbow_y=2.0
genus=flavivirga, num_x=1707, num_y=1707, elbow_x=111.0, elbow_y=2.0
genus=paraliobacillus, num_x=1478, num_y=1478, elbow_x=151.0, elbow_y=2.0
genus=ensifer, num_x=11012, num_y=11012, elbow_x=40.0, elbow_y=8.0
genus=hydrogenobacter, num_x=731, num_y=731, elbow_x=44.0, elbow_y=4.0
genus=propionibacterium, num_x=4638, num_y=4638, elbow_x=1385.0, elbow_y=15.0
genus=sphingobium, num_x=15983, num_y=15983, elbow_x=2910.0, elbow_y=7.0
genus=ketobacter, num_x=1934, num_y=1934, elbow_x=144.0, elbow_y=2.0
genus=rothia, num_x=2190, num_y=2190, elbow_x=754.0, elbow_y=5.0
genus=gluconobacter, num_x=3346, num_y=3346, elbow_x=1255.0, elbow_y=7.0
genus=granulicatella, num_x=1773, num_y=1773, elbow_x=629.0, elbow_y=2.0
genus=glaciecola, num_x=5172, num_y=5172, elbow_x=1142.0, elbow_y=2.0
genus=alkalibacter, num_x=800, num_y=800, elbow_x=47.0, elbow_y=1.0
genus=parolsenella, num_x=585, num_y=585, elbow_x=40.0, elbow_y=2.0
genus=euhalothece, num_x=1247, num_y=1247, elbow_x=77.0, elbow_y=2.0
genus=anaplasma, num_x=624, num_y=624, elbow_x=266.0, elbow_y=8.0
genus=kerstersia, num_x=1716, num_y=1716, elbow_x=32.0, elbow_y=2.0
genus=proteiniphilum, num_x=1324, num_y=1324, elbow_x=65.0, elbow_y=2.0
genus=coraliomargarita, num_x=1196, num_y=1196, elbow_x=67.0, elbow_y=2.0
genus=kurthia, num_x=1743, num_y=1743, elbow_x=632.0, elbow_y=3.0
genus=haematospirillum, num_x=932, num_y=932, elbow_x=89.0, elbow_y=2.0
genus=francisella, num_x=6537, num_y=6537, elbow_x=1454.0, elbow_y=29.0
genus=idiomarina, num_x=2112, num_y=2112, elbow_x=922.0, elbow_y=6.0
genus=turicibacter, num_x=840, num_y=840, elbow_x=93.0, elbow_y=2.0
genus=herbaspirillum, num_x=7546, num_y=7546, elbow_x=2337.0, elbow_y=7.0
genus=salinarimonas, num_x=2204, num_y=2204, elbow_x=29.0, elbow_y=1.0
genus=faecalibaculum, num_x=792, num_y=792, elbow_x=53.0, elbow_y=2.0
genus=caloramator, num_x=940, num_y=940, elbow_x=14.0, elbow_y=2.0
genus=murdochiella, num_x=569, num_y=569, elbow_x=34.0, elbow_y=4.0
genus=mastigocladopsis, num_x=2736, num_y=2736, elbow_x=129.0, elbow_y=1.0
genus=ornithobacterium, ERROR=Optimal parameters not found: Number of calls to function has reached maxfev = 800.
genus=hippea, num_x=735, num_y=735, elbow_x=41.0, elbow_y=2.0
genus=desulfofarcimen, num_x=1261, num_y=1261, elbow_x=85.0, elbow_y=2.0
genus=xanthomonas, num_x=44054, num_y=44054, elbow_x=4590.0, elbow_y=25.0
genus=pricia, num_x=1580, num_y=1580, elbow_x=102.0, elbow_y=1.0
genus=labilibaculum, num_x=1532, num_y=1532, elbow_x=43.0, elbow_y=2.0
genus=methyloceanibacter, num_x=1688, num_y=1688, elbow_x=68.0, elbow_y=3.0
genus=oxalobacter, num_x=919, num_y=919, elbow_x=78.0, elbow_y=6.0
genus=zymomonas, num_x=1505, num_y=1505, elbow_x=743.0, elbow_y=19.0
genus=fastidiosipila, num_x=534, num_y=534, elbow_x=36.0, elbow_y=2.0
genus=marichromatium, num_x=1790, num_y=1790, elbow_x=11.0, elbow_y=2.0
genus=candidatus tokpelaia, num_x=812, num_y=812, elbow_x=54.0, elbow_y=1.0
genus=spongiibacterium, num_x=1484, num_y=1484, elbow_x=81.0, elbow_y=1.0
genus=salinicola, num_x=1811, num_y=1811, elbow_x=170.0, elbow_y=2.0
genus=borreliella, num_x=541, num_y=541, elbow_x=206.0, elbow_y=34.0
genus=spiribacter, num_x=1691, num_y=1691, elbow_x=661.0, elbow_y=4.0
genus=labilithrix, num_x=3688, num_y=3688, elbow_x=1.0, elbow_y=2.0
genus=rugosibacter, num_x=1159, num_y=1159, elbow_x=83.0, elbow_y=1.0
genus=dysosmobacter, num_x=1255, num_y=1255, elbow_x=30.0, elbow_y=2.0
genus=ferrimonas, num_x=1638, num_y=1638, elbow_x=85.0, elbow_y=2.0
genus=haliangium, num_x=2631, num_y=2631, elbow_x=168.0, elbow_y=2.0
genus=pigmentiphaga, num_x=4926, num_y=4926, elbow_x=23.0, elbow_y=3.0
genus=novosphingobium, num_x=12845, num_y=12845, elbow_x=2078.0, elbow_y=4.0
genus=nitrosospira, num_x=4640, num_y=4640, elbow_x=1340.0, elbow_y=5.0
genus=weeksella, num_x=808, num_y=808, elbow_x=40.0, elbow_y=4.0
genus=candidatus fonsibacter, num_x=496, num_y=496, elbow_x=31.0, elbow_y=2.0
genus=anabaena, num_x=5426, num_y=5426, elbow_x=1164.0, elbow_y=3.0
genus=labrys, num_x=3484, num_y=3484, elbow_x=31.0, elbow_y=2.0
genus=laribacter, ERROR=Optimal parameters not found: Number of calls to function has reached maxfev = 800.
genus=nostoc, num_x=15972, num_y=15972, elbow_x=2714.0, elbow_y=4.0
genus=oryzomicrobium, num_x=1475, num_y=1475, elbow_x=80.0, elbow_y=2.0
genus=virgibacillus, num_x=7390, num_y=7390, elbow_x=1492.0, elbow_y=4.0
genus=pirellula, num_x=3264, num_y=3264, elbow_x=226.0, elbow_y=2.0
genus=gluconacetobacter, num_x=1854, num_y=1854, elbow_x=134.0, elbow_y=4.0
genus=fervidobacterium, num_x=1861, num_y=1861, elbow_x=701.0, elbow_y=5.0
genus=clavibacter, num_x=2876, num_y=2876, elbow_x=1192.0, elbow_y=11.0
genus=bosea, num_x=16222, num_y=16222, elbow_x=59.0, elbow_y=4.0
genus=candidatus saccharimonas, num_x=261, num_y=261, elbow_x=11.0, elbow_y=2.0
genus=arenimonas, num_x=2026, num_y=2026, elbow_x=51.0, elbow_y=1.0
genus=pelosinus, num_x=3779, num_y=3779, elbow_x=1135.0, elbow_y=3.0
genus=sulfitobacter, num_x=11544, num_y=11544, elbow_x=1993.0, elbow_y=4.0
genus=piscirickettsia, num_x=3137, num_y=3137, elbow_x=959.0, elbow_y=63.0
genus=leptolyngbya, num_x=7413, num_y=7413, elbow_x=2336.0, elbow_y=4.0
genus=microbacterium, num_x=32308, num_y=32308, elbow_x=2527.0, elbow_y=6.0
genus=fibrella, num_x=2109, num_y=2109, elbow_x=137.0, elbow_y=2.0
genus=anaerococcus, num_x=1161, num_y=1161, elbow_x=60.0, elbow_y=3.0
genus=opitutus, num_x=1882, num_y=1882, elbow_x=56.0, elbow_y=2.0
genus=echinicola, num_x=2981, num_y=2981, elbow_x=1145.0, elbow_y=4.0
genus=trichodesmium, num_x=1470, num_y=1470, elbow_x=15.0, elbow_y=2.0
genus=rhodanobacter, num_x=2795, num_y=2795, elbow_x=763.0, elbow_y=3.0
genus=propionicicella, num_x=1380, num_y=1380, elbow_x=50.0, elbow_y=1.0
genus=cellulomonas, num_x=7121, num_y=7121, elbow_x=1612.0, elbow_y=4.0
genus=xylophilus, num_x=2472, num_y=2472, elbow_x=25.0, elbow_y=2.0
genus=rhodomicrobium, num_x=1513, num_y=1513, elbow_x=78.0, elbow_y=2.0
genus=citromicrobium, num_x=1393, num_y=1393, elbow_x=92.0, elbow_y=2.0
genus=fibrobacter, num_x=1057, num_y=1057, elbow_x=95.0, elbow_y=4.0
genus=pararhodospirillum, num_x=1460, num_y=1460, elbow_x=100.0, elbow_y=2.0
genus=cycloclasticus, ERROR=Optimal parameters not found: Number of calls to function has reached maxfev = 800.
genus=kingella, num_x=1054, num_y=1054, elbow_x=9.0, elbow_y=3.0
genus=fusobacterium, num_x=12865, num_y=12865, elbow_x=1512.0, elbow_y=7.0
genus=amphritea, num_x=2999, num_y=2999, elbow_x=1081.0, elbow_y=2.0
genus=candidatus hodgkinia, num_x=110, num_y=110, elbow_x=20.0, elbow_y=3.0
genus=polymorphum, num_x=2000, num_y=2000, elbow_x=20.0, elbow_y=2.0
genus=marivivens, num_x=1422, num_y=1422, elbow_x=58.0, elbow_y=2.0
genus=psychroflexus, num_x=1322, num_y=1322, elbow_x=89.0, elbow_y=2.0
genus=coprothermobacter, num_x=532, num_y=532, elbow_x=31.0, elbow_y=2.0
genus=leptospira, num_x=5916, num_y=5916, elbow_x=1537.0, elbow_y=9.0
genus=caldicoprobacter, num_x=861, num_y=861, elbow_x=74.0, elbow_y=1.0
genus=yangia, num_x=3373, num_y=3373, elbow_x=38.0, elbow_y=3.0
genus=flagellimonas, num_x=1247, num_y=1247, elbow_x=78.0, elbow_y=2.0
genus=cedecea, num_x=3648, num_y=3648, elbow_x=1594.0, elbow_y=6.0
genus=halobacteriovorax, num_x=1962, num_y=1962, elbow_x=761.0, elbow_y=3.0
genus=coprococcus, num_x=5040, num_y=5040, elbow_x=1500.0, elbow_y=5.0
genus=cytophaga, num_x=1340, num_y=1340, elbow_x=17.0, elbow_y=2.0
genus=nibribacter, num_x=1375, num_y=1375, elbow_x=77.0, elbow_y=2.0
genus=saccharopolyspora, num_x=4791, num_y=4791, elbow_x=165.0, elbow_y=2.0
genus=komagataeibacter, num_x=4541, num_y=4541, elbow_x=1379.0, elbow_y=6.0
genus=pontimonas, num_x=765, num_y=765, elbow_x=16.0, elbow_y=2.0
genus=luteibacter, num_x=4650, num_y=4650, elbow_x=1651.0, elbow_y=3.0
genus=flaviflexus, num_x=1632, num_y=1632, elbow_x=563.0, elbow_y=3.0
genus=coxiella, num_x=9669, num_y=9669, elbow_x=1620.0, elbow_y=4.0
genus=streptosporangium, num_x=8629, num_y=8629, elbow_x=52.0, elbow_y=2.0
genus=pseudopedobacter, num_x=1436, num_y=1436, elbow_x=98.0, elbow_y=2.0
genus=dehalogenimonas, num_x=1301, num_y=1301, elbow_x=372.0, elbow_y=2.0
genus=marisediminicola, num_x=1331, num_y=1331, elbow_x=36.0, elbow_y=2.0
genus=sphaerotilus, num_x=1937, num_y=1937, elbow_x=40.0, elbow_y=2.0
genus=nocardioides, num_x=16663, num_y=16663, elbow_x=2026.0, elbow_y=4.0
genus=neptunomonas, num_x=3088, num_y=3088, elbow_x=1134.0, elbow_y=2.0
genus=gallionella, num_x=1172, num_y=1172, elbow_x=65.0, elbow_y=2.0
genus=gemmobacter, num_x=5187, num_y=5187, elbow_x=47.0, elbow_y=2.0
genus=thermobacillus, num_x=1687, num_y=1687, elbow_x=129.0, elbow_y=2.0
genus=commensalibacter, num_x=853, num_y=853, elbow_x=40.0, elbow_y=4.0
genus=dickeya, num_x=6097, num_y=6097, elbow_x=2024.0, elbow_y=14.0
genus=flavobacterium, num_x=27249, num_y=27249, elbow_x=2711.0, elbow_y=6.0
genus=guyparkeria, num_x=997, num_y=997, elbow_x=24.0, elbow_y=2.0
genus=pseudoxanthomonas, num_x=6993, num_y=6993, elbow_x=1715.0, elbow_y=3.0
genus=microlunatus, num_x=6179, num_y=6179, elbow_x=46.0, elbow_y=3.0
genus=bdellovibrio, num_x=5243, num_y=5243, elbow_x=1444.0, elbow_y=4.0
genus=thermochromatium, num_x=1052, num_y=1052, elbow_x=69.0, elbow_y=2.0
genus=meiothermus, num_x=2769, num_y=2769, elbow_x=503.0, elbow_y=3.0
genus=pragia, num_x=3623, num_y=3623, elbow_x=1391.0, elbow_y=4.0
genus=geovibrio, num_x=1230, num_y=1230, elbow_x=69.0, elbow_y=2.0
genus=granulibacter, ERROR=Optimal parameters not found: Number of calls to function has reached maxfev = 800.
genus=hydromonas, num_x=1045, num_y=1045, elbow_x=57.0, elbow_y=2.0
genus=olsenella, num_x=2390, num_y=2390, elbow_x=480.0, elbow_y=3.0
genus=desulfosporosinus, num_x=3952, num_y=3952, elbow_x=769.0, elbow_y=3.0
genus=nitrospira, num_x=3890, num_y=3890, elbow_x=1046.0, elbow_y=3.0
genus=lelliottia, num_x=5574, num_y=5574, elbow_x=1961.0, elbow_y=7.0
genus=cohaesibacter, num_x=2072, num_y=2072, elbow_x=27.0, elbow_y=1.0
genus=robinsoniella, num_x=4100, num_y=4100, elbow_x=77.0, elbow_y=1.0
genus=mesotoga, num_x=1641, num_y=1641, elbow_x=25.0, elbow_y=2.0
genus=pyrinomonas, num_x=1315, num_y=1315, elbow_x=93.0, elbow_y=1.0
genus=novibacillus, num_x=1445, num_y=1445, elbow_x=186.0, elbow_y=2.0
genus=brachybacterium, num_x=6881, num_y=6881, elbow_x=1628.0, elbow_y=4.0
genus=thioclava, num_x=7491, num_y=7491, elbow_x=2020.0, elbow_y=2.0
genus=grimontia, num_x=2626, num_y=2626, elbow_x=1243.0, elbow_y=6.0
genus=paraphotobacterium, num_x=1018, num_y=1018, elbow_x=79.0, elbow_y=2.0
genus=rhodovulum, num_x=3509, num_y=3509, elbow_x=1316.0, elbow_y=5.0
genus=flexistipes, num_x=1007, num_y=1007, elbow_x=61.0, elbow_y=2.0
genus=hafnia, ERROR=Optimal parameters not found: Number of calls to function has reached maxfev = 800.
genus=stappia, num_x=2363, num_y=2363, elbow_x=34.0, elbow_y=2.0
genus=actinosynnema, num_x=4451, num_y=4451, elbow_x=73.0, elbow_y=5.0
genus=laceyella, num_x=1050, num_y=1050, elbow_x=87.0, elbow_y=2.0
genus=ralstonia, num_x=22452, num_y=22452, elbow_x=4303.0, elbow_y=15.0
genus=desulfurella, num_x=780, num_y=780, elbow_x=46.0, elbow_y=2.0
genus=methylibium, num_x=7626, num_y=7626, elbow_x=2127.0, elbow_y=2.0
genus=basilea, num_x=775, num_y=775, elbow_x=62.0, elbow_y=2.0
genus=roseivivax, num_x=2738, num_y=2738, elbow_x=40.0, elbow_y=4.0
genus=hydrocarboniclastica, num_x=1661, num_y=1661, elbow_x=94.0, elbow_y=2.0
genus=pasteurella, num_x=2924, num_y=2924, elbow_x=1076.0, elbow_y=43.0
genus=pedobacter, num_x=9121, num_y=9121, elbow_x=1687.0, elbow_y=3.0
genus=acidimicrobium, num_x=869, num_y=869, elbow_x=49.0, elbow_y=2.0
genus=sedimentisphaera, num_x=1352, num_y=1352, elbow_x=43.0, elbow_y=3.0
genus=euzebyella, num_x=1704, num_y=1704, elbow_x=93.0, elbow_y=2.0
genus=methylobacillus, num_x=1131, num_y=1131, elbow_x=145.0, elbow_y=2.0
genus=candidatus koribacter, num_x=1863, num_y=1863, elbow_x=159.0, elbow_y=2.0
genus=saccharibacter, num_x=806, num_y=806, elbow_x=45.0, elbow_y=1.0
genus=rhodopseudomonas, num_x=7189, num_y=7189, elbow_x=2135.0, elbow_y=6.0
genus=simplicispira, num_x=1770, num_y=1770, elbow_x=58.0, elbow_y=2.0
genus=kribbella, num_x=3642, num_y=3642, elbow_x=84.0, elbow_y=2.0
genus=alloactinosynnema, num_x=3020, num_y=3020, elbow_x=9.0, elbow_y=2.0
genus=halomonas, num_x=18594, num_y=18594, elbow_x=2788.0, elbow_y=6.0
genus=methylovirgula, num_x=1390, num_y=1390, elbow_x=68.0, elbow_y=2.0
genus=agrobacterium, num_x=19598, num_y=19598, elbow_x=2948.0, elbow_y=11.0
genus=pelolinea, num_x=1354, num_y=1354, elbow_x=10.0, elbow_y=2.0
genus=alicyclobacillus, num_x=2679, num_y=2679, elbow_x=1045.0, elbow_y=4.0
genus=methylocaldum, num_x=1992, num_y=1992, elbow_x=136.0, elbow_y=2.0
genus=candidatus nucleicultrix, num_x=741, num_y=741, elbow_x=46.0, elbow_y=2.0
genus=yersinia, num_x=26399, num_y=26399, elbow_x=3685.0, elbow_y=36.0
genus=diaminobutyricimonas, num_x=1425, num_y=1425, elbow_x=28.0, elbow_y=2.0
genus=histophilus, num_x=1430, num_y=1430, elbow_x=697.0, elbow_y=35.0
genus=thiomicrospira, num_x=1820, num_y=1820, elbow_x=612.0, elbow_y=3.0
genus=anaerorhabdus, num_x=939, num_y=939, elbow_x=39.0, elbow_y=1.0
genus=thalassospira, num_x=5429, num_y=5429, elbow_x=40.0, elbow_y=4.0
genus=candidatus methylopumilus, num_x=1044, num_y=1044, elbow_x=356.0, elbow_y=3.0
genus=minicystis, num_x=4201, num_y=4201, elbow_x=256.0, elbow_y=2.0
genus=methylomicrobium, num_x=2523, num_y=2523, elbow_x=1024.0, elbow_y=4.0
genus=melissococcus, num_x=11894, num_y=11894, elbow_x=1782.0, elbow_y=3.0
genus=steroidobacter, num_x=1421, num_y=1421, elbow_x=93.0, elbow_y=2.0
genus=desulfocurvus, num_x=1292, num_y=1292, elbow_x=78.0, elbow_y=1.0
genus=nesterenkonia, num_x=1205, num_y=1205, elbow_x=72.0, elbow_y=2.0
genus=magnetococcus, num_x=1346, num_y=1346, elbow_x=104.0, elbow_y=2.0
genus=granulosicoccus, num_x=3077, num_y=3077, elbow_x=31.0, elbow_y=2.0
genus=candidatus izimaplasma, num_x=673, num_y=673, elbow_x=85.0, elbow_y=2.0
genus=knoellia, num_x=1666, num_y=1666, elbow_x=103.0, elbow_y=1.0
genus=thermomonospora, num_x=2163, num_y=2163, elbow_x=9.0, elbow_y=2.0
genus=hungatella, num_x=7379, num_y=7379, elbow_x=110.0, elbow_y=3.0
genus=roseibacterium, num_x=1468, num_y=1468, elbow_x=38.0, elbow_y=2.0
genus=rhodospira, num_x=1521, num_y=1521, elbow_x=30.0, elbow_y=1.0
genus=methylomonas, num_x=5593, num_y=5593, elbow_x=1452.0, elbow_y=4.0
genus=ilyobacter, num_x=1046, num_y=1046, elbow_x=32.0, elbow_y=2.0
genus=oscillatoria, num_x=3766, num_y=3766, elbow_x=537.0, elbow_y=2.0
genus=sunxiuqinia, num_x=1627, num_y=1627, elbow_x=60.0, elbow_y=1.0
genus=aquibacillus, num_x=1554, num_y=1554, elbow_x=167.0, elbow_y=2.0
genus=psychrobacillus, num_x=5254, num_y=5254, elbow_x=1338.0, elbow_y=3.0
genus=pseudovibrio, num_x=4028, num_y=4028, elbow_x=41.0, elbow_y=2.0
genus=petrimonas, num_x=1765, num_y=1765, elbow_x=106.0, elbow_y=2.0
genus=saccharophagus, num_x=1715, num_y=1715, elbow_x=100.0, elbow_y=2.0
genus=moorea, num_x=2154, num_y=2154, elbow_x=153.0, elbow_y=2.0
genus=microcoleus, num_x=2284, num_y=2284, elbow_x=23.0, elbow_y=2.0
genus=hypericibacter, num_x=3810, num_y=3810, elbow_x=43.0, elbow_y=3.0
genus=afipia, num_x=4186, num_y=4186, elbow_x=22.0, elbow_y=1.0
genus=hirschia, num_x=1499, num_y=1499, elbow_x=101.0, elbow_y=2.0
genus=brachyspira, num_x=5949, num_y=5949, elbow_x=1636.0, elbow_y=5.0
genus=asaccharobacter, num_x=1945, num_y=1945, elbow_x=11.0, elbow_y=2.0
genus=ruania, num_x=2403, num_y=2403, elbow_x=65.0, elbow_y=2.0
genus=sagittula, num_x=2373, num_y=2373, elbow_x=24.0, elbow_y=2.0
genus=shimwellia, num_x=1720, num_y=1720, elbow_x=7.0, elbow_y=6.0
genus=rhodoferax, num_x=9165, num_y=9165, elbow_x=1259.0, elbow_y=3.0
genus=panacibacter, num_x=1886, num_y=1886, elbow_x=102.0, elbow_y=2.0
genus=ichthyobacterium, num_x=434, num_y=434, elbow_x=20.0, elbow_y=2.0
genus=borrelia, num_x=561, num_y=561, elbow_x=252.0, elbow_y=25.0
genus=micropruina, num_x=1518, num_y=1518, elbow_x=108.0, elbow_y=2.0
genus=nakamurella, num_x=3493, num_y=3493, elbow_x=99.0, elbow_y=2.0
genus=candidatus amoebophilus, num_x=517, num_y=517, elbow_x=27.0, elbow_y=2.0
genus=tetrasphaera, num_x=3660, num_y=3660, elbow_x=996.0, elbow_y=2.0
genus=pisciglobus, num_x=860, num_y=860, elbow_x=72.0, elbow_y=1.0
genus=methylovulum, num_x=1461, num_y=1461, elbow_x=96.0, elbow_y=2.0
genus=williamsia, num_x=5564, num_y=5564, elbow_x=1530.0, elbow_y=2.0
genus=stackebrandtia, num_x=4569, num_y=4569, elbow_x=45.0, elbow_y=2.0
genus=ignavibacterium, num_x=1187, num_y=1187, elbow_x=62.0, elbow_y=2.0
genus=oceanimonas, num_x=2116, num_y=2116, elbow_x=55.0, elbow_y=2.0
genus=nibricoccus, num_x=1634, num_y=1634, elbow_x=97.0, elbow_y=2.0
genus=phoenicibacter, num_x=452, num_y=452, elbow_x=32.0, elbow_y=3.0
genus=salinibacterium, num_x=2888, num_y=2888, elbow_x=574.0, elbow_y=3.0
genus=candidatus sulcia, num_x=134, num_y=134, elbow_x=53.0, elbow_y=19.0
genus=candidatus vidania, num_x=32, num_y=32, elbow_x=1.0, elbow_y=1.0
genus=indioceanicola, num_x=2149, num_y=2149, elbow_x=148.0, elbow_y=2.0
genus=paludisphaera, num_x=2094, num_y=2094, elbow_x=139.0, elbow_y=2.0
genus=agromyces, num_x=5069, num_y=5069, elbow_x=1180.0, elbow_y=4.0
genus=terriglobus, num_x=4976, num_y=4976, elbow_x=846.0, elbow_y=2.0
genus=caldilinea, num_x=1847, num_y=1847, elbow_x=37.0, elbow_y=2.0
genus=spirochaeta, num_x=6084, num_y=6084, elbow_x=1024.0, elbow_y=2.0
genus=rahnella, num_x=3777, num_y=3777, elbow_x=1706.0, elbow_y=10.0
genus=croceicoccus, num_x=2658, num_y=2658, elbow_x=721.0, elbow_y=3.0
genus=nocardiopsis, num_x=6209, num_y=6209, elbow_x=2154.0, elbow_y=5.0
genus=salinimonas, num_x=3784, num_y=3784, elbow_x=1211.0, elbow_y=3.0
genus=bernardetia, num_x=1263, num_y=1263, elbow_x=80.0, elbow_y=2.0
genus=jeotgalibaca, num_x=2071, num_y=2071, elbow_x=605.0, elbow_y=3.0
genus=thermosipho, num_x=1326, num_y=1326, elbow_x=549.0, elbow_y=6.0
genus=pimelobacter, num_x=2564, num_y=2564, elbow_x=41.0, elbow_y=2.0
genus=nonlabens, num_x=3229, num_y=3229, elbow_x=1032.0, elbow_y=4.0
genus=cyanothece, num_x=8414, num_y=8414, elbow_x=1670.0, elbow_y=3.0
genus=hyphomicrobium, num_x=4403, num_y=4403, elbow_x=1239.0, elbow_y=3.0
genus=gallibacterium, num_x=1010, num_y=1010, elbow_x=12.0, elbow_y=2.0
genus=ammonifex, num_x=683, num_y=683, elbow_x=38.0, elbow_y=2.0
genus=alkaliphilus, num_x=2370, num_y=2370, elbow_x=75.0, elbow_y=2.0
genus=stenotrophomonas, num_x=132768, num_y=132768, elbow_x=6234.0, elbow_y=9.0
genus=variovorax, num_x=10041, num_y=10041, elbow_x=45.0, elbow_y=5.0
genus=flavonifractor, num_x=6488, num_y=6488, elbow_x=973.0, elbow_y=4.0
genus=kibdelosporangium, num_x=8311, num_y=8311, elbow_x=63.0, elbow_y=2.0
genus=cyclobacterium, num_x=1929, num_y=1929, elbow_x=62.0, elbow_y=2.0
genus=oceanihabitans, num_x=1113, num_y=1113, elbow_x=28.0, elbow_y=2.0
genus=leadbetterella, num_x=1559, num_y=1559, elbow_x=5.0, elbow_y=2.0
genus=gemmatirosa, num_x=2392, num_y=2392, elbow_x=170.0, elbow_y=2.0
genus=mycobacterium, num_x=153885, num_y=153885, elbow_x=7436.0, elbow_y=189.0
genus=athalassotoga, num_x=801, num_y=801, elbow_x=17.0, elbow_y=2.0
genus=kiloniellales, num_x=92, num_y=92, elbow_x=8.0, elbow_y=1.0
genus=aminiphilus, num_x=989, num_y=989, elbow_x=14.0, elbow_y=1.0
genus=kiritimatiella, num_x=934, num_y=934, elbow_x=67.0, elbow_y=2.0
genus=oleispira, num_x=1636, num_y=1636, elbow_x=100.0, elbow_y=2.0
genus=alteromonas, num_x=10786, num_y=10786, elbow_x=2609.0, elbow_y=13.0
genus=otariodibacter, num_x=738, num_y=738, elbow_x=57.0, elbow_y=2.0
genus=magnetospirillum, num_x=4358, num_y=4358, elbow_x=1490.0, elbow_y=5.0
genus=litorimicrobium, num_x=1801, num_y=1801, elbow_x=58.0, elbow_y=1.0
genus=bacterioplanes, num_x=1839, num_y=1839, elbow_x=122.0, elbow_y=2.0
genus=leisingera, num_x=7974, num_y=7974, elbow_x=2282.0, elbow_y=5.0
genus=barnesiella, num_x=1000, num_y=1000, elbow_x=77.0, elbow_y=2.0
genus=moritella, num_x=3337, num_y=3337, elbow_x=1162.0, elbow_y=3.0
genus=chlamydia, num_x=45190, num_y=45190, elbow_x=1409.0, elbow_y=6.0
genus=kocuria, num_x=5524, num_y=5524, elbow_x=1581.0, elbow_y=6.0
genus=oscillibacter, num_x=2441, num_y=2441, elbow_x=85.0, elbow_y=2.0
genus=desulfotomaculum, num_x=2920, num_y=2920, elbow_x=756.0, elbow_y=3.0
genus=candidatus midichloria, num_x=365, num_y=365, elbow_x=21.0, elbow_y=2.0
genus=thiohalospira, num_x=1095, num_y=1095, elbow_x=65.0, elbow_y=1.0
genus=parvibacter, num_x=788, num_y=788, elbow_x=10.0, elbow_y=2.0
genus=desulfurispirillum, num_x=1133, num_y=1133, elbow_x=8.0, elbow_y=2.0
genus=thermotoga, num_x=2350, num_y=2350, elbow_x=786.0, elbow_y=10.0
genus=croceibacter, num_x=1067, num_y=1067, elbow_x=59.0, elbow_y=2.0
genus=kosmotoga, num_x=1350, num_y=1350, elbow_x=32.0, elbow_y=3.0
genus=pantoea, num_x=13093, num_y=13093, elbow_x=2910.0, elbow_y=10.0
genus=paenalcaligenes, num_x=1218, num_y=1218, elbow_x=90.0, elbow_y=2.0
genus=ectothiorhodospira, num_x=2525, num_y=2525, elbow_x=944.0, elbow_y=2.0
genus=egibacter, num_x=1847, num_y=1847, elbow_x=27.0, elbow_y=2.0
genus=frischella, num_x=906, num_y=906, elbow_x=89.0, elbow_y=2.0
genus=algoriphagus, num_x=8421, num_y=8421, elbow_x=1941.0, elbow_y=3.0
genus=tatumella, num_x=3126, num_y=3126, elbow_x=1152.0, elbow_y=4.0
genus=kozakia, num_x=1610, num_y=1610, elbow_x=50.0, elbow_y=3.0
genus=jannaschia, num_x=2001, num_y=2001, elbow_x=28.0, elbow_y=2.0
genus=parasaccharibacter, num_x=725, num_y=725, elbow_x=34.0, elbow_y=2.0
genus=jeotgalibacillus, num_x=1496, num_y=1496, elbow_x=99.0, elbow_y=2.0
genus=sediminibacillus, num_x=2154, num_y=2154, elbow_x=137.0, elbow_y=1.0
genus=anaerohalosphaera, num_x=1223, num_y=1223, elbow_x=96.0, elbow_y=2.0
genus=aquicella, num_x=1713, num_y=1713, elbow_x=519.0, elbow_y=2.0
genus=kineococcus, num_x=2159, num_y=2159, elbow_x=44.0, elbow_y=3.0
genus=parvimonas, num_x=1152, num_y=1152, elbow_x=524.0, elbow_y=6.0
genus=sulfuritortus, num_x=1083, num_y=1083, elbow_x=59.0, elbow_y=2.0
genus=pseudanabaena, num_x=3103, num_y=3103, elbow_x=314.0, elbow_y=2.0
genus=kutzneria, num_x=8072, num_y=8072, elbow_x=159.0, elbow_y=2.0
genus=anoxybacter, num_x=1143, num_y=1143, elbow_x=83.0, elbow_y=2.0
genus=marinilactibacillus, num_x=1150, num_y=1150, elbow_x=106.0, elbow_y=2.0
genus=christensenella, num_x=2347, num_y=2347, elbow_x=13.0, elbow_y=3.0
genus=paucibacter, num_x=1991, num_y=1991, elbow_x=34.0, elbow_y=2.0
genus=thermosynechococcus, num_x=2080, num_y=2080, elbow_x=972.0, elbow_y=4.0
genus=pseudoflavonifractor, num_x=1405, num_y=1405, elbow_x=90.0, elbow_y=4.0
genus=snodgrassella, ERROR=Optimal parameters not found: Number of calls to function has reached maxfev = 800.
genus=arenibacter, num_x=2021, num_y=2021, elbow_x=84.0, elbow_y=2.0
genus=kyrpidia, num_x=1256, num_y=1256, elbow_x=87.0, elbow_y=2.0
genus=reinekea, num_x=1469, num_y=1469, elbow_x=29.0, elbow_y=2.0
genus=halothiobacillus, num_x=1647, num_y=1647, elbow_x=589.0, elbow_y=3.0
genus=thermus, num_x=3933, num_y=3933, elbow_x=1113.0, elbow_y=7.0
genus=sulfuricella, num_x=1273, num_y=1273, elbow_x=81.0, elbow_y=2.0
genus=methylobacterium, num_x=37897, num_y=37897, elbow_x=4012.0, elbow_y=5.0
genus=peptoniphilus, num_x=3228, num_y=3228, elbow_x=773.0, elbow_y=4.0
genus=selenihalanaerobacter, num_x=947, num_y=947, elbow_x=90.0, elbow_y=1.0
genus=salinivirga, num_x=1392, num_y=1392, elbow_x=47.0, elbow_y=2.0
genus=capnocytophaga, num_x=6684, num_y=6684, elbow_x=1521.0, elbow_y=6.0
genus=enterobacter, num_x=62168, num_y=62168, elbow_x=5353.0, elbow_y=52.0
genus=anaerolinea, num_x=1293, num_y=1293, elbow_x=49.0, elbow_y=2.0
genus=sulfurihydrogenibium, num_x=1089, num_y=1089, elbow_x=324.0, elbow_y=2.0
genus=phascolarctobacterium, num_x=1015, num_y=1015, elbow_x=101.0, elbow_y=4.0
genus=lachnoclostridium, num_x=13862, num_y=13862, elbow_x=20.0, elbow_y=3.0
genus=syntrophomonas, num_x=956, num_y=956, elbow_x=55.0, elbow_y=2.0
genus=winogradskyella, num_x=3244, num_y=3244, elbow_x=1076.0, elbow_y=2.0
genus=nitrosomonas, num_x=11055, num_y=11055, elbow_x=1679.0, elbow_y=4.0
genus=belliella, num_x=1340, num_y=1340, elbow_x=26.0, elbow_y=2.0
genus=dehalobacterium, num_x=1179, num_y=1179, elbow_x=99.0, elbow_y=2.0
genus=acetohalobium, num_x=797, num_y=797, elbow_x=56.0, elbow_y=2.0
genus=phreatobacter, num_x=4527, num_y=4527, elbow_x=37.0, elbow_y=3.0
genus=lachnospira, num_x=3494, num_y=3494, elbow_x=963.0, elbow_y=2.0
genus=erythrobacter, num_x=6477, num_y=6477, elbow_x=1659.0, elbow_y=5.0
genus=escherichia, num_x=239244, num_y=239244, elbow_x=7137.0, elbow_y=95.0
genus=yoonia, num_x=1700, num_y=1700, elbow_x=42.0, elbow_y=2.0
genus=pseudohongiella, num_x=1325, num_y=1325, elbow_x=34.0, elbow_y=2.0
genus=dokdonella, num_x=1669, num_y=1669, elbow_x=120.0, elbow_y=2.0
genus=candidatus, num_x=5838, num_y=5838, elbow_x=1045.0, elbow_y=2.0
genus=phycisphaera, num_x=1345, num_y=1345, elbow_x=98.0, elbow_y=2.0
genus=leeia, num_x=1772, num_y=1772, elbow_x=94.0, elbow_y=1.0
genus=anaeromusa, num_x=1231, num_y=1231, elbow_x=75.0, elbow_y=1.0
genus=saccharomonospora, num_x=2987, num_y=2987, elbow_x=1240.0, elbow_y=4.0
genus=haloactinobacterium, num_x=2646, num_y=2646, elbow_x=44.0, elbow_y=2.0
genus=georhizobium, num_x=1864, num_y=1864, elbow_x=39.0, elbow_y=2.0
genus=pilibacter, num_x=907, num_y=907, elbow_x=78.0, elbow_y=1.0
genus=pediococcus, num_x=6187, num_y=6187, elbow_x=1361.0, elbow_y=13.0
genus=solitalea, num_x=1693, num_y=1693, elbow_x=101.0, elbow_y=2.0
genus=zobellia, num_x=2115, num_y=2115, elbow_x=128.0, elbow_y=3.0
genus=azoarcus, num_x=8479, num_y=8479, elbow_x=2081.0, elbow_y=5.0
genus=haliscomenobacter, num_x=2604, num_y=2604, elbow_x=120.0, elbow_y=2.0
genus=noviherbaspirillum, num_x=3694, num_y=3694, elbow_x=1401.0, elbow_y=2.0
genus=hydrogenobaculum, ERROR=Optimal parameters not found: Number of calls to function has reached maxfev = 800.
genus=plesiomonas, num_x=1481, num_y=1481, elbow_x=46.0, elbow_y=4.0
genus=bradymonas, num_x=1423, num_y=1423, elbow_x=114.0, elbow_y=2.0
genus=phycicoccus, num_x=4206, num_y=4206, elbow_x=1352.0, elbow_y=2.0
genus=ureaplasma, ERROR=Optimal parameters not found: Number of calls to function has reached maxfev = 800.
genus=actinophytocola, num_x=4028, num_y=4028, elbow_x=40.0, elbow_y=1.0
genus=cetia, num_x=800, num_y=800, elbow_x=58.0, elbow_y=2.0
genus=xylella, num_x=1862, num_y=1862, elbow_x=780.0, elbow_y=16.0
genus=intestinibaculum, num_x=1069, num_y=1069, elbow_x=14.0, elbow_y=2.0
genus=polynucleobacter, num_x=3930, num_y=3930, elbow_x=1053.0, elbow_y=6.0
genus=hahella, num_x=3305, num_y=3305, elbow_x=158.0, elbow_y=5.0
genus=candidatus nardonella, num_x=78, num_y=78, elbow_x=24.0, elbow_y=3.0
genus=candidatus fokinia, num_x=216, num_y=216, elbow_x=1.0, elbow_y=2.0
genus=desulfatirhabdium, num_x=1500, num_y=1500, elbow_x=92.0, elbow_y=1.0
genus=carboxydocella, num_x=1000, num_y=1000, elbow_x=74.0, elbow_y=4.0
genus=lachnoanaerobaculum, num_x=2724, num_y=2724, elbow_x=933.0, elbow_y=5.0
genus=isoptericola, num_x=3395, num_y=3395, elbow_x=1030.0, elbow_y=3.0
genus=prevotella, num_x=5976, num_y=5976, elbow_x=1280.0, elbow_y=7.0
genus=parvularcula, num_x=1171, num_y=1171, elbow_x=75.0, elbow_y=2.0
genus=desulfofundulus, num_x=1041, num_y=1041, elbow_x=78.0, elbow_y=1.0
genus=halocella, num_x=1481, num_y=1481, elbow_x=15.0, elbow_y=2.0
genus=lactobacillus, num_x=70670, num_y=70670, elbow_x=3909.0, elbow_y=22.0
genus=janibacter, num_x=2838, num_y=2838, elbow_x=1181.0, elbow_y=3.0
genus=lysobacter, num_x=7910, num_y=7910, elbow_x=2041.0, elbow_y=5.0
genus=pseudobacter, num_x=2209, num_y=2209, elbow_x=27.0, elbow_y=2.0
genus=mycoplasma, num_x=4335, num_y=4335, elbow_x=406.0, elbow_y=17.0
genus=dokdonia, num_x=1875, num_y=1875, elbow_x=869.0, elbow_y=5.0
genus=halocynthiibacter, num_x=1745, num_y=1745, elbow_x=44.0, elbow_y=2.0
genus=candidatus thioglobus, num_x=1457, num_y=1457, elbow_x=494.0, elbow_y=3.0
genus=lawsonella, num_x=695, num_y=695, elbow_x=66.0, elbow_y=4.0
genus=paeniclostridium, num_x=1245, num_y=1245, elbow_x=108.0, elbow_y=2.0
genus=neorickettsia, num_x=418, num_y=418, elbow_x=199.0, elbow_y=5.0
genus=empedobacter, num_x=1452, num_y=1452, elbow_x=78.0, elbow_y=4.0
genus=oligotropha, num_x=1537, num_y=1537, elbow_x=98.0, elbow_y=6.0
genus=parabacteroides, num_x=3220, num_y=3220, elbow_x=1362.0, elbow_y=5.0
genus=pseudopropionibacterium, num_x=1638, num_y=1638, elbow_x=816.0, elbow_y=7.0
genus=proteus, num_x=8432, num_y=8432, elbow_x=2338.0, elbow_y=26.0
genus=pseudorhodobacter, num_x=3215, num_y=3215, elbow_x=33.0, elbow_y=2.0
genus=leclercia, num_x=6074, num_y=6074, elbow_x=2150.0, elbow_y=11.0
genus=gloeocapsa, num_x=2262, num_y=2262, elbow_x=18.0, elbow_y=2.0
genus=pannonibacter, num_x=3059, num_y=3059, elbow_x=30.0, elbow_y=4.0
genus=pseudorhodoplanes, num_x=2583, num_y=2583, elbow_x=46.0, elbow_y=2.0
genus=thioploca, num_x=1494, num_y=1494, elbow_x=86.0, elbow_y=2.0
genus=raineyella, num_x=1420, num_y=1420, elbow_x=102.0, elbow_y=2.0
genus=kordia, num_x=2222, num_y=2222, elbow_x=670.0, elbow_y=3.0
genus=tateyamaria, num_x=1939, num_y=1939, elbow_x=33.0, elbow_y=2.0
genus=synechococcus, num_x=19099, num_y=19099, elbow_x=3354.0, elbow_y=4.0
genus=tistrella, num_x=3950, num_y=3950, elbow_x=28.0, elbow_y=3.0
genus=pusillimonas, num_x=2486, num_y=2486, elbow_x=46.0, elbow_y=3.0
genus=rhizobacter, num_x=2976, num_y=2976, elbow_x=15.0, elbow_y=4.0
genus=tomitella, num_x=1721, num_y=1721, elbow_x=161.0, elbow_y=2.0
genus=marivirga, num_x=2125, num_y=2125, elbow_x=80.0, elbow_y=2.0
genus=gloeobacter, num_x=2973, num_y=2973, elbow_x=686.0, elbow_y=2.0
genus=pustulibacterium, num_x=1391, num_y=1391, elbow_x=123.0, elbow_y=1.0
genus=atopobium, num_x=2193, num_y=2193, elbow_x=596.0, elbow_y=3.0
genus=alicycliphilus, num_x=3377, num_y=3377, elbow_x=48.0, elbow_y=3.0
genus=legionella, num_x=40568, num_y=40568, elbow_x=3845.0, elbow_y=63.0
genus=renibacterium, num_x=1529, num_y=1529, elbow_x=165.0, elbow_y=7.0
genus=halanaerobium, num_x=1452, num_y=1452, elbow_x=26.0, elbow_y=2.0
genus=marvinbryantia, num_x=1696, num_y=1696, elbow_x=134.0, elbow_y=1.0
genus=casimicrobium, num_x=1853, num_y=1853, elbow_x=50.0, elbow_y=2.0
genus=lentibacillus, num_x=1378, num_y=1378, elbow_x=135.0, elbow_y=2.0
genus=catelliglobosispora, num_x=3419, num_y=3419, elbow_x=79.0, elbow_y=1.0
genus=paraprevotella, num_x=979, num_y=979, elbow_x=63.0, elbow_y=2.0
genus=rhodoluna, num_x=1107, num_y=1107, elbow_x=474.0, elbow_y=5.0
genus=hydrogenovibrio, num_x=1513, num_y=1513, elbow_x=662.0, elbow_y=4.0
genus=rhodothermus, ERROR=Optimal parameters not found: Number of calls to function has reached maxfev = 800.
genus=leptothrix, num_x=2066, num_y=2066, elbow_x=18.0, elbow_y=2.0
genus=acinetobacter, num_x=191305, num_y=191305, elbow_x=6419.0, elbow_y=38.0
genus=epidermidibacterium, num_x=1959, num_y=1959, elbow_x=71.0, elbow_y=1.0
genus=pelagibacterium, num_x=1823, num_y=1823, elbow_x=36.0, elbow_y=2.0
genus=mageeibacillus, num_x=587, num_y=587, elbow_x=22.0, elbow_y=2.0
genus=rickettsiella, num_x=555, num_y=555, elbow_x=55.0, elbow_y=2.0
genus=gordonia, num_x=12633, num_y=12633, elbow_x=2800.0, elbow_y=6.0
genus=liberibacter, num_x=1109, num_y=1109, elbow_x=408.0, elbow_y=8.0
genus=flexibacter, num_x=1378, num_y=1378, elbow_x=45.0, elbow_y=1.0
genus=planifilum, num_x=1197, num_y=1197, elbow_x=90.0, elbow_y=1.0
genus=orenia, num_x=847, num_y=847, elbow_x=17.0, elbow_y=1.0
genus=rivularia, num_x=2452, num_y=2452, elbow_x=210.0, elbow_y=2.0
genus=geobacter, num_x=9958, num_y=9958, elbow_x=1903.0, elbow_y=4.0
genus=photobacterium, num_x=6908, num_y=6908, elbow_x=1915.0, elbow_y=5.0
genus=limnobaculum, num_x=1261, num_y=1261, elbow_x=78.0, elbow_y=2.0
genus=planktomarina, num_x=1509, num_y=1509, elbow_x=27.0, elbow_y=1.0
genus=paenisporosarcina, num_x=2032, num_y=2032, elbow_x=526.0, elbow_y=3.0
genus=mannheimia, num_x=2853, num_y=2853, elbow_x=1139.0, elbow_y=68.0
genus=tabrizicola, num_x=1991, num_y=1991, elbow_x=34.0, elbow_y=2.0
genus=ruminiclostridium, num_x=7123, num_y=7123, elbow_x=1734.0, elbow_y=2.0
genus=pseudoclostridium, num_x=1579, num_y=1579, elbow_x=85.0, elbow_y=2.0
genus=thiocystis, num_x=1630, num_y=1630, elbow_x=23.0, elbow_y=2.0
genus=longibaculum, num_x=1067, num_y=1067, elbow_x=124.0, elbow_y=2.0
genus=nitratireductor, num_x=3275, num_y=3275, elbow_x=35.0, elbow_y=2.0
genus=candidatus stammera, num_x=35, num_y=35, elbow_x=6.0, elbow_y=1.0
genus=salinihabitans, num_x=1752, num_y=1752, elbow_x=31.0, elbow_y=1.0
genus=luteitalea, num_x=2483, num_y=2483, elbow_x=146.0, elbow_y=2.0
genus=schwartzia, num_x=905, num_y=905, elbow_x=67.0, elbow_y=1.0
genus=paracoccus, num_x=29414, num_y=29414, elbow_x=2949.0, elbow_y=7.0
genus=lutimaribacter, num_x=2641, num_y=2641, elbow_x=29.0, elbow_y=2.0
genus=segniliparus, num_x=1271, num_y=1271, elbow_x=93.0, elbow_y=2.0
genus=porphyromonas, num_x=3266, num_y=3266, elbow_x=963.0, elbow_y=11.0
genus=paraburkholderia, num_x=27680, num_y=27680, elbow_x=4331.0, elbow_y=7.0
genus=lutispora, num_x=1282, num_y=1282, elbow_x=26.0, elbow_y=1.0
genus=shinella, num_x=3236, num_y=3236, elbow_x=40.0, elbow_y=2.0
genus=schaalia, num_x=1598, num_y=1598, elbow_x=576.0, elbow_y=4.0
genus=parachlamydia, num_x=872, num_y=872, elbow_x=92.0, elbow_y=2.0
genus=maribacter, num_x=4158, num_y=4158, elbow_x=1219.0, elbow_y=4.0
genus=sulfuritalea, num_x=1588, num_y=1588, elbow_x=76.0, elbow_y=2.0
genus=sinomonas, num_x=1969, num_y=1969, elbow_x=135.0, elbow_y=2.0
genus=mariniblastus, num_x=1818, num_y=1818, elbow_x=130.0, elbow_y=2.0
genus=algoriella, num_x=1166, num_y=1166, elbow_x=49.0, elbow_y=1.0
genus=marinitoga, num_x=855, num_y=855, elbow_x=47.0, elbow_y=4.0
genus=epibacterium, num_x=2308, num_y=2308, elbow_x=39.0, elbow_y=4.0
genus=mariprofundus, num_x=1380, num_y=1380, elbow_x=615.0, elbow_y=3.0
genus=ilumatobacter, num_x=2066, num_y=2066, elbow_x=24.0, elbow_y=2.0
genus=marivita, num_x=1864, num_y=1864, elbow_x=21.0, elbow_y=1.0
genus=sinorhizobium, num_x=45167, num_y=45167, elbow_x=5186.0, elbow_y=11.0
genus=marininema, num_x=1679, num_y=1679, elbow_x=81.0, elbow_y=1.0
genus=martelella, num_x=4915, num_y=4915, elbow_x=20.0, elbow_y=3.0
genus=spiroplasma, num_x=1768, num_y=1768, elbow_x=228.0, elbow_y=7.0
genus=pseudomonas, num_x=279325, num_y=279325, elbow_x=10577.0, elbow_y=60.0
genus=octadecabacter, num_x=4539, num_y=4539, elbow_x=936.0, elbow_y=3.0
genus=megasphaera, num_x=2400, num_y=2400, elbow_x=797.0, elbow_y=4.0
genus=ruminococcus, num_x=2639, num_y=2639, elbow_x=378.0, elbow_y=2.0
genus=planctopirus, num_x=1332, num_y=1332, elbow_x=82.0, elbow_y=2.0
genus=spirosoma, num_x=11210, num_y=11210, elbow_x=2505.0, elbow_y=3.0
genus=melaminivora, num_x=2326, num_y=2326, elbow_x=78.0, elbow_y=3.0
genus=sulfobacillus, num_x=2344, num_y=2344, elbow_x=85.0, elbow_y=2.0
genus=shigella, num_x=175571, num_y=175571, elbow_x=6311.0, elbow_y=63.0
genus=staphylospora, num_x=937, num_y=937, elbow_x=84.0, elbow_y=2.0
genus=rheinheimera, num_x=2644, num_y=2644, elbow_x=25.0, elbow_y=2.0
genus=melittangium, num_x=3253, num_y=3253, elbow_x=184.0, elbow_y=2.0
genus=sulfurovum, num_x=1275, num_y=1275, elbow_x=540.0, elbow_y=3.0
genus=xanthobacter, num_x=2825, num_y=2825, elbow_x=205.0, elbow_y=3.0
genus=stella, num_x=4952, num_y=4952, elbow_x=36.0, elbow_y=4.0
genus=methylacidiphilum, num_x=1111, num_y=1111, elbow_x=522.0, elbow_y=4.0
genus=solibacillus, num_x=3054, num_y=3054, elbow_x=1058.0, elbow_y=3.0
genus=sutterellaceae, num_x=878, num_y=878, elbow_x=56.0, elbow_y=1.0
genus=methylococcus, num_x=1127, num_y=1127, elbow_x=55.0, elbow_y=2.0
genus=tissierellia, num_x=1765, num_y=1765, elbow_x=147.0, elbow_y=1.0
genus=swingsia, num_x=1261, num_y=1261, elbow_x=483.0, elbow_y=3.0
genus=methylophaga, num_x=2503, num_y=2503, elbow_x=946.0, elbow_y=2.0
genus=zhouia, num_x=1380, num_y=1380, elbow_x=78.0, elbow_y=1.0
genus=methylophilus, num_x=1276, num_y=1276, elbow_x=78.0, elbow_y=2.0
genus=syntrophus, num_x=1768, num_y=1768, elbow_x=727.0, elbow_y=2.0
genus=thermomonas, num_x=1234, num_y=1234, elbow_x=53.0, elbow_y=2.0
genus=microcella, num_x=1124, num_y=1124, elbow_x=15.0, elbow_y=2.0
genus=thermovirga, num_x=666, num_y=666, elbow_x=53.0, elbow_y=2.0
genus=microcystis, num_x=4677, num_y=4677, elbow_x=1482.0, elbow_y=6.0
genus=thiomicrorhabdus, num_x=2174, num_y=2174, elbow_x=598.0, elbow_y=3.0
genus=moraxella, num_x=10015, num_y=10015, elbow_x=1953.0, elbow_y=18.0
genus=thorselliaceae, num_x=1030, num_y=1030, elbow_x=23.0, elbow_y=1.0
genus=mordavella, num_x=973, num_y=973, elbow_x=94.0, elbow_y=2.0
genus=tissierella, num_x=2476, num_y=2476, elbow_x=41.0, elbow_y=1.0
genus=mucinivorans, num_x=919, num_y=919, elbow_x=77.0, elbow_y=2.0
genus=vagococcus, num_x=2262, num_y=2262, elbow_x=543.0, elbow_y=3.0
genus=mycetocola, num_x=2170, num_y=2170, elbow_x=35.0, elbow_y=2.0
genus=zobellella, num_x=1631, num_y=1631, elbow_x=77.0, elbow_y=2.0
genus=myroides, num_x=6171, num_y=6171, elbow_x=1852.0, elbow_y=9.0
genus=myxococcus, num_x=6662, num_y=6662, elbow_x=2655.0, elbow_y=7.0
genus=natranaerobius, num_x=1019, num_y=1019, elbow_x=15.0, elbow_y=2.0
genus=neochlamydia, num_x=662, num_y=662, elbow_x=11.0, elbow_y=2.0
genus=niabella, num_x=2650, num_y=2650, elbow_x=110.0, elbow_y=3.0
genus=nitrospirillum, num_x=3057, num_y=3057, elbow_x=254.0, elbow_y=2.0
genus=oceanicoccus, num_x=1859, num_y=1859, elbow_x=151.0, elbow_y=2.0
genus=oceanithermus, num_x=906, num_y=906, elbow_x=38.0, elbow_y=2.0
genus=oceanobacillus, num_x=4586, num_y=4586, elbow_x=987.0, elbow_y=3.0
genus=oligella, num_x=2970, num_y=2970, elbow_x=1085.0, elbow_y=3.0
genus=olivibacter, num_x=2187, num_y=2187, elbow_x=53.0, elbow_y=2.0
genus=olleya, num_x=2373, num_y=2373, elbow_x=1013.0, elbow_y=3.0
genus=oribacterium, num_x=3320, num_y=3320, elbow_x=937.0, elbow_y=2.0
genus=orrella, num_x=2273, num_y=2273, elbow_x=28.0, elbow_y=2.0
genus=paenibacillus, num_x=85397, num_y=85397, elbow_x=3048.0, elbow_y=6.0
genus=paludibacter, num_x=1209, num_y=1209, elbow_x=79.0, elbow_y=2.0
genus=pelobacter, num_x=3124, num_y=3124, elbow_x=633.0, elbow_y=2.0
genus=pelodictyon, num_x=1584, num_y=1584, elbow_x=470.0, elbow_y=2.0
genus=petrotoga, num_x=791, num_y=791, elbow_x=20.0, elbow_y=2.0
genus=phenylobacterium, num_x=5635, num_y=5635, elbow_x=1516.0, elbow_y=2.0
genus=phyllobacterium, num_x=2738, num_y=2738, elbow_x=37.0, elbow_y=2.0
genus=pistricoccus, num_x=1447, num_y=1447, elbow_x=87.0, elbow_y=2.0
genus=plantactinospora, num_x=5847, num_y=5847, elbow_x=41.0, elbow_y=4.0
genus=plantibacter, num_x=2262, num_y=2262, elbow_x=33.0, elbow_y=4.0
genus=pleurocapsa, num_x=1760, num_y=1760, elbow_x=110.0, elbow_y=2.0
genus=pontibacillus, num_x=1417, num_y=1417, elbow_x=127.0, elbow_y=2.0
genus=pseudoflavitalea, num_x=2577, num_y=2577, elbow_x=67.0, elbow_y=2.0
genus=pseudozobellia, num_x=1661, num_y=1661, elbow_x=87.0, elbow_y=1.0
genus=psychrobacter, num_x=5029, num_y=5029, elbow_x=1420.0, elbow_y=7.0
genus=reichenbachiella, num_x=2766, num_y=2766, elbow_x=729.0, elbow_y=1.0
genus=rhizorhabdus, num_x=2399, num_y=2399, elbow_x=202.0, elbow_y=2.0
genus=rodentibacter, num_x=883, num_y=883, elbow_x=168.0, elbow_y=2.0
genus=roseobacter, num_x=2470, num_y=2470, elbow_x=44.0, elbow_y=5.0
genus=rufibacter, num_x=2887, num_y=2887, elbow_x=1023.0, elbow_y=3.0
genus=ruthenibacterium, num_x=1601, num_y=1601, elbow_x=203.0, elbow_y=2.0
genus=salinibacter, num_x=1990, num_y=1990, elbow_x=979.0, elbow_y=10.0
genus=salinisphaera, num_x=1728, num_y=1728, elbow_x=31.0, elbow_y=2.0
genus=sebaldella, num_x=1290, num_y=1290, elbow_x=10.0, elbow_y=2.0
genus=sediminicola, num_x=1269, num_y=1269, elbow_x=79.0, elbow_y=2.0
genus=simiduia, num_x=1693, num_y=1693, elbow_x=74.0, elbow_y=2.0
genus=simkania, num_x=703, num_y=703, elbow_x=79.0, elbow_y=2.0
genus=simonsiella, num_x=6, num_y=6, elbow_x=1.0, elbow_y=1.0
genus=sinimarinibacterium, num_x=1292, num_y=1292, elbow_x=101.0, elbow_y=2.0
genus=skermanella, num_x=2307, num_y=2307, elbow_x=34.0, elbow_y=2.0
genus=soehngenia, num_x=874, num_y=874, elbow_x=59.0, elbow_y=2.0
genus=solimonas, num_x=2279, num_y=2279, elbow_x=195.0, elbow_y=2.0
genus=sphingobacterium, num_x=12634, num_y=12634, elbow_x=1938.0, elbow_y=4.0
genus=sphingosinicella, num_x=3865, num_y=3865, elbow_x=687.0, elbow_y=2.0
genus=spongiibacter, num_x=1386, num_y=1386, elbow_x=84.0, elbow_y=2.0
genus=sporolituus, num_x=982, num_y=982, elbow_x=66.0, elbow_y=1.0
genus=sporomusa, num_x=1816, num_y=1816, elbow_x=151.0, elbow_y=2.0
genus=sulfuriferula, num_x=2965, num_y=2965, elbow_x=770.0, elbow_y=3.0
genus=sulfuriflexus, num_x=1201, num_y=1201, elbow_x=55.0, elbow_y=2.0
genus=sulfurifustis, num_x=1501, num_y=1501, elbow_x=99.0, elbow_y=2.0
genus=sulfurimonas, num_x=2837, num_y=2837, elbow_x=828.0, elbow_y=4.0
genus=sutterella, num_x=1758, num_y=1758, elbow_x=419.0, elbow_y=3.0
genus=synergistes, num_x=1373, num_y=1373, elbow_x=545.0, elbow_y=3.0
genus=syntrophobotulus, num_x=1172, num_y=1172, elbow_x=64.0, elbow_y=2.0
genus=tardiphaga, num_x=2922, num_y=2922, elbow_x=39.0, elbow_y=1.0
genus=tepidanaerobacter, num_x=935, num_y=935, elbow_x=71.0, elbow_y=4.0
genus=tepidiphilus, num_x=989, num_y=989, elbow_x=42.0, elbow_y=1.0
genus=terasakiella, num_x=1596, num_y=1596, elbow_x=96.0, elbow_y=2.0
genus=terribacillus, num_x=1667, num_y=1667, elbow_x=121.0, elbow_y=2.0
genus=thalassotalea, num_x=2932, num_y=2932, elbow_x=886.0, elbow_y=3.0
genus=thermacetogenium, num_x=898, num_y=898, elbow_x=43.0, elbow_y=2.0
genus=thermaerobacter, num_x=1280, num_y=1280, elbow_x=39.0, elbow_y=3.0
genus=thermanaerovibrio, num_x=626, num_y=626, elbow_x=35.0, elbow_y=2.0
genus=thermoanaerobacter, num_x=2851, num_y=2851, elbow_x=933.0, elbow_y=7.0
genus=thermoanaerobacterium, num_x=2111, num_y=2111, elbow_x=811.0, elbow_y=5.0
genus=thermoclostridium, num_x=1302, num_y=1302, elbow_x=129.0, elbow_y=4.0
genus=thermodesulfatator, num_x=857, num_y=857, elbow_x=68.0, elbow_y=2.0
genus=thermoleophilum, num_x=876, num_y=876, elbow_x=51.0, elbow_y=1.0
genus=thiodictyon, num_x=1958, num_y=1958, elbow_x=94.0, elbow_y=2.0
genus=trabulsiella, num_x=1903, num_y=1903, elbow_x=92.0, elbow_y=4.0
genus=tsukamurella, num_x=4598, num_y=4598, elbow_x=1847.0, elbow_y=5.0
genus=vampirococcus, num_x=674, num_y=674, elbow_x=66.0, elbow_y=2.0
genus=verminephrobacter, num_x=2204, num_y=2204, elbow_x=36.0, elbow_y=2.0
genus=waddlia, num_x=597, num_y=597, elbow_x=45.0, elbow_y=2.0
genus=weissella, num_x=5670, num_y=5670, elbow_x=1277.0, elbow_y=8.0
genus=wigglesworthia, num_x=358, num_y=358, elbow_x=175.0, elbow_y=3.0
genus=xylanibacterium, num_x=1548, num_y=1548, elbow_x=86.0, elbow_y=2.0
genus=youhaiella, num_x=2153, num_y=2153, elbow_x=31.0, elbow_y=2.0
completed in 51.46 seconds


SELECT
  COUNT(1) AS NUM_ROWS,
  COUNT(DISTINCT GENUS_NAME) AS NUM_DISTINCT_GENERA
  FROM
    GENUS_MINIMUM_CUTOFF_THRESHOLD

+--------+-------------------+
|NUM_ROWS|NUM_DISTINCT_GENERA|
+--------+-------------------+
|1400    |1400               |
+--------+-------------------+

completed in 0.64 seconds


SELECT *
  FROM
    GENUS_MINIMUM_CUTOFF_THRESHOLD
    ORDER BY 1
    LIMIT 10

+---------------+---------+
|GENUS_NAME     |THRESHOLD|
+---------------+---------+
|abiotrophia    |2.0      |
|acaryochloris  |2.0      |
|acetoanaerobium|3.0      |
|acetobacter    |11.0     |
|acetobacterium |2.0      |
|acetohalobium  |2.0      |
|acetomicrobium |3.0      |
|acholeplasma   |3.0      |
|achromobacter  |17.0     |
|acidaminococcus|3.0      |
+---------------+---------+

completed in 0.22 seconds


real  1m19.208s
user  4m34.458s
sys  1m5.295s
```
