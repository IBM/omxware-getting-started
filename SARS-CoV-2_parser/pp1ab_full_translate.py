#! /usr/bin/env python3.7

import argparse
import csv
import hashlib
import logging

import pandas as pd
from Bio import SeqIO
from Bio.Seq import Seq


def load_fna(file_name: str):
    with open(file_name, 'r') as fna_file:
        return next(SeqIO.parse(fna_file, 'fasta'))


def load_potentials(file_name: str):
    potentials = []
    for fasta in SeqIO.parse(open(file_name), 'fasta'):
        desc = str(fasta.description)
        seq = str(fasta.seq)
        if 'VNN*' in seq:
            start_pot = int(desc.split('#')[1].strip())
            end_pot = int(desc.split('#')[2].strip())
            potentials.append({'Start': start_pot, 'End': end_pot, 'Type': 'pp1ab'})
        if 'FAV*' in seq:
            start_pot = int(desc.split('#')[1].strip())
            end_pot = int(desc.split('#')[2].strip())
            potentials.append({'Start': start_pot, 'End': end_pot, 'Type': 'pp1a'})
    potentials_df = pd.DataFrame(potentials)
    return potentials_df


def load_references(ref_path: str):
    logging.info("Loading references")

    ref_protein = []
    with open(ref_path, 'r') as fasta_file:
        for record in SeqIO.parse(fasta_file, 'fasta'):
            md5 = hashlib.md5(str(record.seq).encode('utf-8')).hexdigest()
            name_field = record.description
            discard, uniprot_id, long_name = name_field.split('|')
            ref_protein.append({
                'md5': md5,
                'uniprot_id': uniprot_id.rstrip(),
                'long_name': long_name,
                'seq': str(record.seq),
                'len': len(record.seq)
            })
    ref_seqs = pd.DataFrame(ref_protein)

    return ref_seqs


def get_indices(df):
    start_index = -1
    end_index = -1

    if ('pp1ab' in df['Type'].values):
        row = df.loc[df['Type'] == 'pp1ab'].iloc[0]
        end_index = int(row['End'])
        start_index = end_index - 21289
    elif ('pp1a' in df['Type'].values):
        row = df.loc[df['Type'] == 'pp1a'].iloc[0]
        end_index = int(row['End'])
        start_index = end_index - 13218
        end_index = start_index + 21289
    else:
        logging.info("No evidence of pp1ab detected by prodigal")
    return start_index, end_index


def get_full_dna(start_index: int, end_index: int, seq: str):
    # check if genome has 1 or 2 annotations of pp1ab (prodigal output?)
    # if 1 annotaion - match annotaion to genome sequence, start index = start of match - 13502, stop index = end of annotated section
    # if 2 annotations - match annotations to genome sequence, order first and second matches, start index = first start, stop_index = second end
    # correctness checks - Find ATG in seq and set to start_index, then find ATG (beg) and TAA(end)
    # pp1ab RNA sequence = genome sequence[start_index : stop_index]

    # 0 = no pp1ab found
    seq = seq.upper()
    if (seq[start_index: start_index + 3] != 'ATG') and ('ACT' in seq[start_index: end_index]):
        pos = (seq.index('ACT', start_index, end_index)) - start_index
        start_index = start_index + pos

    while seq[start_index: start_index + 3] != 'ATG':
        start_index = start_index - 1
    while seq[end_index - 3: end_index] != 'TAA':
        end_index = end_index + 1
    dna_seq = seq[start_index: end_index]

    return dna_seq, start_index, end_index


def find_slippage(seq):
    set_N = set(
        ['AAA', 'BBB', 'CCC', 'DDD', 'GGG', 'HHH', 'KKK', 'MMM', 'NNN', 'RRR', 'SSS', 'TTT', 'UUU', 'VVV', 'WWW',
         'YYY'])
    set_W = set(['AAA', 'UUU'])
    set_Z = set(['A', 'B', 'C', 'D', 'H', 'K', 'M', 'N', 'R', 'S', 'T', 'U', 'V', 'W', 'Y'])

    if (len(seq) < 7):
        return -1
    for i in range(0, len(seq) - 6):
        isSlippage = ((seq[i:i + 3] in set_N) and (seq[i + 3:i + 6] in set_W) and (seq[i + 6] in set_Z))
        if (isSlippage):
            return i

    return -1


def slippage_dna(dna_seq: str, pp1a_start: int, pp1a_end: int):
    if len(dna_seq) > 13219:
        pp1a_length = (pp1a_end - pp1a_start)
        pp1a_dna = dna_seq[:pp1a_length - 3]
        slippage_index = find_slippage(dna_seq)
        if slippage_index != -1:
            pp1b_dna = dna_seq[:slippage_index] + dna_seq[slippage_index - 1] + dna_seq[slippage_index:]
            pp1b_dna = pp1b_dna[pp1a_length-3:]
            pp1ab_dna = pp1a_dna + pp1b_dna
            return pp1ab_dna
        else:
            logging.info('No Slippage site found')

    else:
        logging.info('DNA sequence found is not long enough')

def translate(dna_seq: str):
    dna_seq = dna_seq.replace("T", "U")

    if len(dna_seq) > 13219:
        pp1a_dna = dna_seq[:13218]
        pp1a_prot = str(Seq(pp1a_dna).translate())

        slippage_index = find_slippage(dna_seq)
        if slippage_index != -1:
            pp1b_dna = dna_seq[:slippage_index] + dna_seq[slippage_index - 1] + dna_seq[slippage_index:]
            pp1b_prot = str(Seq(pp1b_dna).translate(table=1))[4405:]

            pp1ab_prot = pp1a_prot + pp1b_prot

            return pp1ab_prot
        else:
            logging.info('No Slippage site found')
    else:
        pp1a_prot = str(Seq(dna_seq).translate())
        logging.info('DNA sequence found is not long enough')

        return (pp1a_prot)
    
def get_prodigal_list_clean(coord_list, start_index, end_index):
    clean_list = []
    for coord in str(coord_list).split('\n'):
        if '>' in coord:
            temp = str(coord).split('_')
            if not (int(temp[1]) >= start_index and int(temp[2]) <= end_index):
                clean_list.append(coord)
    return clean_list

def clean_pp1a(start, end, seq):
    seq = seq.upper()
    if (seq[start: start + 3] != 'ATG') and ('ACT' in seq[start: end]):
        pos = (seq.index('ACT', start, end)) - start
        start = start + pos

    while seq[start: start + 3] != 'ATG':
        start = start - 1
    while seq[end - 3: end] != 'TAA':
        end = end + 1
    return start, end

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--genome_file',
                        dest='genome_file',
                        type=str,
                        required=True,
                        help='Assembled genome file in FASTA format')
    parser.add_argument('--prodigal_potentials',
                        dest='prodigal_potentials',
                        type=str,
                        required=True,
                        help='Potential proteins coordinates and scores output by Prodigal')
    parser.add_argument('--accession',
                        dest='accession',
                        type=str,
                        required=True,
                        help='Genome accession')
    parser.add_argument('--output_dir',
                        dest='output_dir',
                        type=str,
                        required=False,
                        default='./',
                        help="Base path for output files including log file and any desired protein outputs")
    parser.add_argument('--prodigal_output',
                        dest='prodigal_output',
                        type=str,
                        required=True,
                        help="Coordinates from prodigal")

    args = parser.parse_args()

    prodigal_output = args.prodigal_output

    fna_file_name = args.genome_file
    accession = args.accession
    fna = load_fna(fna_file_name)
    fna_sequence = str(fna.seq)

    output_dir = args.output_dir

    potentials_file_name = args.prodigal_potentials
    potentials_df = load_potentials(potentials_file_name)

    start_index_pot, end_index_pot = get_indices(potentials_df)
    dna_seq, start_idx, end_idx = get_full_dna(start_index_pot, end_index_pot, fna_sequence)

    prod_coord_list = get_prodigal_list_clean(prodigal_output, start_idx, end_idx)

    pp1a_start, pp1a_end = clean_pp1a(start_idx, start_idx + 13215, fna_sequence)
    dna_corrected = slippage_dna(dna_seq, pp1a_start, pp1a_end)

    pp1ab_coord = str(len(prod_coord_list) + 1) + '_' + str(start_idx + 1) + '_' + str(end_idx) + '_+_' + str(dna_corrected)
    pp1a_coord = str(len(prod_coord_list) + 2) + '_' + str(pp1a_start + 1) + '_' + str(pp1a_end) + '_+'

    for coord in prod_coord_list:
        print(coord.strip('>'))

    print(pp1a_coord)
    print(pp1ab_coord)


if __name__ == "__main__":
    main()
