# VFDB

[back to parent](../README.md)

The Virulence Factor Database (VFDB) is a resource consisting of known and predicted virulence factors for a number of bacterial genera.

URL: http://www.mgc.ac.cn/VFs/

The full datasets for both genes and proteins were downloaded and parsed with the script [parse_vfdb.py](parse_vfdb.py). This script generates two CSV files. One for genes and the other for proteins. The contents of these files are imported into Apache Spark for virulence analysis with FGP data.

Run the following to parse the VFDB data:

```
time ./parse_vfdb.py
```

OUTPUT

```
sequence - max_length=51060, num_nulls=0
short_name - max_length=18, num_nulls=0
full_name - max_length=187, num_nulls=0
factor_name - max_length=192, num_nulls=0
genus_name - max_length=15, num_nulls=0
species_name - max_length=21, num_nulls=0
strain - max_length=113, num_nulls=206

real	0m2.701s
user	0m4.026s
sys	0m2.021s
```

Record Totals:
* Gene - 32522
* Protein - 28616
