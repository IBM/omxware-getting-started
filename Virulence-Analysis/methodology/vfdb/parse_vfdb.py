#! /usr/bin/env python

import csv
import hashlib
import os
import re
from collections import defaultdict
from dataclasses import dataclass

from Bio import SeqIO

ORGANISM_PATTERN = re.compile(r'^([\w\S]+)\s*(?:([\w\S]+))?\s*(?:(.+))?$')
SEQ_RECORD_PATTERN = re.compile(r'^.+?\s\((.+?)\)\s(.+?(?= \[))\s\[(.+?)\]\s\[(.+?)\]$')


class Organism(object):

    def __init__(self, full_name: str) -> None:
        names = re.search(ORGANISM_PATTERN, full_name)
        if not names:
            raise Exception(f'bad match: {full_name}')
        self.genus_name, self.species_name, self.strain = names.groups()


@dataclass
class SeqObj(object):
    md5: str
    short_name: str
    full_name: str
    factor_name: str
    organism: Organism
    length: int
    sequence: str

    @classmethod
    def parse_seq_record(cls, seq_record: SeqIO.SeqRecord) -> 'SeqObj':
        md5 = hashlib.md5(str(seq_record.seq).encode('utf-8')).hexdigest()
        matches = re.search(SEQ_RECORD_PATTERN, seq_record.description)
        if matches is None or len(matches.groups()) != 4:
            raise Exception(f'bad match: {seq_record.description}')
        short_name, full_name, factor_name, organism_name = matches.groups()
        return SeqObj(
            md5=md5,
            short_name=short_name.strip(),
            full_name=full_name.strip(),
            factor_name=factor_name.strip(),
            organism=Organism(organism_name),
            length=len(seq_record.seq),
            sequence=str(seq_record.seq))


class MaxLenCounter(object):

    def __init__(self) -> None:
        self.max_length = 0
        self.num_nulls = 0

    def add(self, s: str) -> None:
        if not s:
            self.num_nulls += 1
        else:
            self.max_length = max([len(s), self.max_length])


def main():
    counters = defaultdict(MaxLenCounter)
    fasta_files = ['VFDB_setB_nt.fas', 'VFDB_setB_pro.fas']

    for fasta_file in fasta_files:
        output_type = 'gene' if '_nt' in fasta_file else 'protein'
        csv_file_name = f'{output_type}.csv'
        csv_file_path = os.path.join('outputs', csv_file_name)
        os.makedirs('outputs', exist_ok=True)

        with open(csv_file_path, 'w') as csv_file:
            csv_writer = csv.writer(csv_file, quoting=csv.QUOTE_MINIMAL)
            vfdb_file_path = os.path.join('vfdb', fasta_file)

            for seq_record in SeqIO.parse(vfdb_file_path, 'fasta'):
                seq_obj = SeqObj.parse_seq_record(seq_record)

                counters['sequence'].add(seq_obj.sequence)
                counters['short_name'].add(seq_obj.short_name)
                counters['full_name'].add(seq_obj.full_name)
                counters['factor_name'].add(seq_obj.factor_name)
                counters['genus_name'].add(seq_obj.organism.genus_name)
                counters['species_name'].add(seq_obj.organism.species_name)
                counters['strain'].add(seq_obj.organism.strain)

                csv_writer.writerow([
                    seq_obj.md5,
                    seq_obj.short_name,
                    seq_obj.full_name,
                    seq_obj.factor_name,
                    seq_obj.organism.genus_name,
                    seq_obj.organism.species_name,
                    seq_obj.organism.strain
                ])

    for key, value in counters.items():
        print(f'{key} - max_length={value.max_length}, num_nulls={value.num_nulls}')


if __name__ == '__main__':
    main()
