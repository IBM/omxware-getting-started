#!/usr/bin/env python3.7

import argparse
import csv
import gzip
import hashlib
import logging
import math
from typing import List, Tuple

import pandas as pd
from Bio import SeqIO
from Bio import pairwise2
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio.SubsMat import MatrixInfo as matlist

logging.basicConfig(level=logging.INFO)


def load_references(ref_path: str) -> pd.DataFrame:
    logging.info("Loading references")

    protein_names_for_extraction = ['ORF9b protein', 'ORF10 protein', 'Envelope small membrane protein']
    uniprot_ids_for_extraction = ['P0DTD2', 'A0A663DJA2', 'P0DTC4']  # use refs for SARS-CoV-2 only, not SARS

    known_ref_for_extraction = {}
    for i in range(len(uniprot_ids_for_extraction)):
        known_ref_for_extraction[uniprot_ids_for_extraction[i]] = protein_names_for_extraction[i]

    covid_ref_proteins = []
    with open(ref_path, 'r') as fasta_file:
        for record in SeqIO.parse(fasta_file, 'fasta'):
            md5 = hashlib.md5(str(record.seq).encode('utf-8')).hexdigest()
            name_field = record.description
            uniprot_id, short_name, long_name, discard = name_field.split('~~~')  # parse extended name field
            uniprot_id = uniprot_id.rstrip()
            if uniprot_id in known_ref_for_extraction.keys():
                covid_ref_proteins.append({
                    'md5': md5,
                    'uniprot_id': uniprot_id,
                    'short_name': short_name,
                    'long_name': long_name,
                    'seq': str(record.seq),
                    'len': len(record.seq)
                })
            else:
                logging.warning("Additional unused reference sequences detected for extraction.")

    ref_seqs = pd.DataFrame(covid_ref_proteins)

    if all(ref_seqs['uniprot_id'].isin(known_ref_for_extraction.keys())):
        logging.info(
            f"All expected protein references observed for UniProt IDs: {known_ref_for_extraction.keys()}")
    else:
        logging.error(f"Missing expected reference protein sequences")

    return ref_seqs


def load_fna(file_name: str) -> SeqRecord:
    if file_name.endswith('.gz'):
        with gzip.open(file_name, 'rt') as fna_file:
            return next(SeqIO.parse(fna_file, 'fasta'))
    with open(file_name, 'r') as fna_file:
        return next(SeqIO.parse(fna_file, 'fasta'))


def load_potentials(file_name: str) -> List[Tuple[int, int, str, float]]:
    with open(file_name, 'r') as input_file:
        csv_reader = csv.reader(input_file, delimiter='\t')

        # return start, stop, strand, score
        return [(int(row[0]), int(row[1]), str(row[2]), float(row[3])) for row in csv_reader if
                csv_reader.line_num > 5 and row]


def calculate_length_bounds(protein_lengths: List[int]) -> Tuple[int, int]:
    # calculate max min of gene lengths from protein reference sequence lengths
    min_protein_length = math.floor((min(protein_lengths) * 3) * 0.9)
    max_protein_length = math.ceil((max(protein_lengths) * 3) * 1.1)

    return min_protein_length, max_protein_length


def select_prot_seq(refs: pd.DataFrame, accession: str, p_seq_records_param: List[SeqRecord],
                    n_seq_records_param: List[SeqRecord]) -> \
        pd.DataFrame:
    logging.info("Checking Prodigal potential sequences")
    refs_found = refs

    refs_found['p_md5'] = ""
    refs_found['extracted_seq'] = ""
    refs_found['same_as_ref'] = False
    refs_found['extracted_seq_len'] = 0

    n_seq_records = set()
    duplicate_gene_seqs = False
    for record in n_seq_records_param:
        if record.id in n_seq_records:
            logging.warning(f"Duplicate md5 in parsed gene potentials {record.id}, inspect input files")
            duplicate_gene_seqs = True
        else:
            n_seq_records.add(record.id)

    dict_p_seq_records = {}
    for record in p_seq_records_param:
        id = record.id
        sequence = str(record.seq)

        if id in dict_p_seq_records:
            if duplicate_gene_seqs is False:
                # since gene sequences are confirmed as unique, any duplicated proteins are synonymous mutations
                logging.info(f"Duplicate md5 in parsed protein potentials due to synonymous mutations, {id}")
        else:
            dict_p_seq_records[id] = sequence

    n_exact_matches = 0
    n_closest_matches = 0
    for i in range(len(refs)):
        logging.info(f"Searching ref {refs['long_name'][i]}: {refs['md5'][i]}")

        # search reference md5 in all seq records
        if refs['md5'][i] in dict_p_seq_records:
            logging.info(f"Found exact match: {refs['long_name'][i]}, {refs['md5'][i]}")
            refs_found.loc[i, 'p_md5'] = refs['md5'][i]
            refs_found.loc[i, 'extracted_seq'] = refs['seq'][i]
            refs_found.loc[i, 'extracted_seq_len'] = len(refs['seq'][i])
            refs_found.loc[i, 'same_as_ref'] = True
            n_exact_matches = n_exact_matches + 1
        else:
            logging.info("No exact match found, searching Prodigal potentials.")

            # set gap penalties
            gap_open = -2
            gap_extend = -1
            # note: not much consensus in literature or bioinformatics forums
            # aside from heavier penalty on creation of gap than there is for extension of gap

            # calculate alignment score possible for perfect identity match to reference
            identity_score = pairwise2.align.globalds(refs['seq'][i], refs['seq'][i], matlist.blosum62,
                                                      gap_open, gap_extend, score_only=True)
            # print(f"Identity score: {identity_score}")

            best_sequence = ""
            best_sequence_md5 = ""
            best_score = float(0)
            for md5, potential_seq in dict_p_seq_records.items():
                aln_score = pairwise2.align.globalds(refs['seq'][i],
                                                     potential_seq,
                                                     matlist.blosum62,
                                                     gap_open,
                                                     gap_extend,
                                                     score_only=True
                                                     )
                # if isinstance(aln_score, list):
                #     aln_score = float(-1)
                # TODO uncomment above if we need type control

                # print("Aligning:")
                # print(f"REF:\t{refs['seq'][i]}")
                # print(f"SEQ:\t{potential_seq}")
                # print(aln_score)

                if best_score < aln_score:
                    best_score = aln_score
                    best_sequence = potential_seq
                    best_sequence_md5 = md5

            minimum_score_similarity = 0.9
            if best_score / identity_score > minimum_score_similarity:
                refs_found.loc[i, 'p_md5'] = best_sequence_md5
                refs_found.loc[i, 'extracted_seq'] = best_sequence
                refs_found.loc[i, 'extracted_seq_len'] = len(best_sequence)
                logging.info(
                    f"High scoring extracted match: {best_score / identity_score * 100:.2f}% alignment score similarity")
                logging.info(f"Reference: {refs['seq'][i]}\n\t  Potential: {best_sequence}")
                n_closest_matches = n_closest_matches + 1
            else:
                logging.warning(f"No high scoring sequence found for {refs['long_name'][i]}: {refs['seq'][i]}")
                logging.info(
                    f"Best scoring extracted match: {best_score / identity_score * 100:.2f}% alignment score similarity")

    logging.info(
        f"Summary stat {accession}: Found {n_exact_matches} exact matches, {n_closest_matches} closest matches\n")

    return refs_found


def do_parse(
        genome_file: str,
        prodigal_potentials: str,
        protein_ref_path: str,
        accession: str,
        output_type: str,
        output_dir: str) -> None:
    fna_file_name = genome_file
    potential_file_name = prodigal_potentials

    fna = load_fna(fna_file_name)
    potentials = load_potentials(potential_file_name)

    # TODO Ed, what do we want to do for accession parsing?
    # accession = potential_file_name.replace('_potential_genes.out', '')

    # note: logs will be written to the location of the potentials file, unless accession parsing is modified
    logging.basicConfig(filename=f'{output_dir}/{accession}_covid19_prodigal_parser.log',
                        filemode='w', level=logging.INFO
                        )

    refs = load_references(protein_ref_path)

    (min_gene_size, max_gene_size) = calculate_length_bounds(refs['len'])

    # length filter potentials
    fna_sequence = str(fna.seq)
    n_seq_records = []
    p_seq_records = []
    potential_coordinates = {}
    for potential in potentials:

        # locate and extract gene sequence from genome
        start_idx, end_idx, strand, score = potential
        gene_length = end_idx - start_idx
        sequence = fna_sequence[start_idx - 1:end_idx - 1]
        seq = Seq(sequence)
        md5 = hashlib.md5(str(sequence).encode('utf-8')).hexdigest()
        n_seq_record = SeqRecord(seq, id=md5, description=f'prodigal_wrapper.sh s={start_idx}, e={end_idx}',
                                 annotations={"molecule_type": "DNA"})

        # gene and protein length logic:
        # since a protein product can only be created if a gene is valid biologically
        # gene conditions must be met in order to output a protein sequence
        # if gene conditions are met, then protein conditions are evaluated

        # is gene length within range?
        if gene_length < min_gene_size or gene_length > max_gene_size:
            # note if min gene length requirement is not met then protein sequence should not be generated
            continue

        # translate gene sequence to protein sequence
        p_seq_record = n_seq_record.translate(table=1, to_stop=True)
        md5 = hashlib.md5(str(p_seq_record.seq).encode('utf-8')).hexdigest()
        p_seq_record.id = md5
        p_seq_record.seq_len = len(
            p_seq_record)  # length here does not count white space which is correct for the sequence length
        p_seq_record.description = f'prodigal_wrapper.sh s={start_idx}, e={end_idx}, len={p_seq_record.seq_len}, score={score}'

        potential_coordinates[p_seq_record.id] = f"{start_idx}_{end_idx}_{strand}"

        n_seq_records.append(n_seq_record)
        p_seq_records.append(p_seq_record)

    logging.info(f"{accession} completed:\n \
                     N Length Similar Gene Candidates Identified:\t {len(n_seq_records)}\n \
                     N Length Similar Protein Candidates Identified:\t {len(p_seq_records)}\n"
                 )

    # check potential proteins against known references
    matching_proteins_df = select_prot_seq(refs, accession, p_seq_records, n_seq_records)

    # output tuple of start stop and strand for downstream prokka parsing
    if output_type == "coordinates_only":
        for matching_p_md5 in matching_proteins_df['p_md5']:
            if matching_p_md5:
                print('1_' + str(potential_coordinates[matching_p_md5]))

    # TODO for ed, generate index based on number of other observed sequences by prodigal_wrapper.sh

    if output_type == 'protein_csv':
        # print(f"Finished processing {accession}")
        matching_proteins_df['accession'] = accession
        matching_proteins_df.to_csv(f"{output_dir}/{accession}_extracted_proteins_all.csv", index=False)

    if output_type == "protein_fasta" or output_type == "protein_fasta_w_ref":
        for i in range(len(matching_proteins_df)):
            with open(f"{output_dir}/{accession}_extracted-{matching_proteins_df['long_name'][i]}.fasta", 'w') as ofile:
                if output_type == "protein_fasta_w_ref":
                    ofile.write(">" + "uniprot_id:" + matching_proteins_df['uniprot_id'][i] + " " +
                                matching_proteins_df['long_name'][i] + "\n" +
                                matching_proteins_df['seq'][i] + "\n")

                ofile.write(">uid_key:" + matching_proteins_df['p_md5'][i] + "|genome_accession:" + accession + " " +
                            matching_proteins_df['long_name'][i] + "\n" +
                            matching_proteins_df['extracted_seq'][i] + "\n"
                            )

    logging.shutdown()


def main() -> None:
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
                        help='Potential gene coordinates and scores output by Prodigal')
    parser.add_argument('--protein_references_path',
                        dest='protein_ref_path',
                        type=str,
                        required=True,
                        help='Fasta formatted file containing protein reference sequences to be extracted')
    parser.add_argument('--accession',
                        dest='accession',
                        type=str,
                        required=True,
                        help='Genome accession')
    parser.add_argument('--output_type',
                        dest='output_type',
                        type=str,
                        required=True,
                        default='coordinates_only',
                        choices=['coordinates_only', 'protein_csv', 'protein_fasta', 'protein_fasta_w_ref'],
                        help="Specify output format type.\n"
                             "coordinates_only: output gene coordinates\n"
                             "protein_csv: output protein sequence and summary statistics in comparison to references\n"
                             "protein_fasta: output each predicted protein sequences as a fasta\n"
                             "protein_fasta_w_ref: same as protein_fasta with the reference sequence prepended to each fasta"
                        )
    parser.add_argument('--output_dir',
                        dest='output_dir',
                        type=str,
                        required=False,
                        default='./',
                        help="Base path for output files including log file and any desired protein outputs"
                        )
    args = parser.parse_args()

    do_parse(
        args.genome_file,
        args.prodigal_potentials,
        args.protein_ref_path,
        args.accession,
        args.output_type,
        args.output_dir
    )


if __name__ == '__main__':
    main()
