#! /usr/bin/env bash

set -e

genus=${1}; shift
accession=${1}; shift
genome_file=${2}

if [[ "${genus,,}" != "betacoronavirus" ]]; then
	prodigal "$@"
else
	prodigal_result=$(prodigal "$@" -s /outputs/${accession}_potentials.out -a /outputs/${accession}_protein_translations.out)
	header=$(echo "${prodigal_result}" | grep "^#")
	coordinates_old=$(echo "${prodigal_result}" | grep "^[^#]")
	coordinates_pesky3="$(./covid19_prodigal_parser.py \
		--genome_file "${genome_file}" \
		--prodigal_potentials /outputs/${accession}_potentials.out \
		--protein_references_path /root/covid19_ref_proteins.fasta \
		--accession ${accession} \
		--output_type coordinates_only \
		--output_dir /outputs)"
	coordinates_pp1ab="$(./pp1ab_full_translate.py \
		--genome_file "${genome_file}" \
		--prodigal_potentials /outputs/${accession}_protein_translations.out \
		--accession ${accession} \
		--prodigal_output "${coordinates_old}" \
		--output_dir /outputs)"
	# NOTE: Score thresholds on potentials are handled in the pp1ab script above and no longer in the default prodigal processing.
	coordinates_final=$(echo -e "${coordinates_pesky3}\n${coordinates_pp1ab}" | sort -t "_" -k 2 -n | cut -d "_" -f 2- | uniq | awk '{ print ">" ++c "_" $1 }')
	echo -e "${header}\n${coordinates_final}"
fi
