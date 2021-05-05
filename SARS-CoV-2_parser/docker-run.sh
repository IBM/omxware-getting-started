#! /usr/bin/env bash

KINGDOM=Viruses
GENUS=betacoronavirus
ACCESSION=NC_045512.2
FASTA_FILE=${ACCESSION}.fasta
INPUTS_DIR="${PWD}/inputs"
OUTPUTS_DIR="${PWD}/outputs"
NCBI_URL="https://www.ncbi.nlm.nih.gov/sviewer/viewer.fcgi?id=1798174254&db=nuccore&report=fasta&retmode=text&withmarkup=on&tool=portal&log$=seqview&maxdownloadsize=1000000"

if ! test -f "${INPUTS_DIR}/${FASTA_FILE}"; then
	mkdir -p "${INPUTS_DIR}" && mkdir -p "${OUTPUTS_DIR}"
	(which wget && wget -O "${INPUTS_DIR}/${FASTA_FILE}" "${NCBI_URL}") || {
		echo "unable to download genome ${ACCESSION}."
		exit 1
	}
fi

docker run \
	--rm \
	--interactive \
	--tty \
	--volume "${PWD}/inputs:/inputs:ro" \
	--volume "${PWD}/outputs:/outputs:rw" \
		fgp-sars-cov-2-genome-annotation \
			/inputs/${FASTA_FILE} \
			--kingdom ${KINGDOM} \
			--genus ${GENUS} \
			--locustag ${ACCESSION} \
			--prefix ${ACCESSION}_annotated \
			--rfam \
			--force \
			--outdir /outputs
