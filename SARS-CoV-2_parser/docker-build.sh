#! /usr/bin/env bash

#
# The following items will need to be downloaded prior to running this script
#
# SWISS:Knife
# https://sourceforge.net/projects/swissknife/files/swissknife/1.80/swissknife_1.80.tar.gz/download
#
# barrnap
# https://github.com/tseemann/barrnap/archive/refs/tags/0.9.tar.gz
#
# prokka
# https://github.com/tseemann/prokka/archive/refs/tags/v1.14.5.tar.gz
#
# tbl2asn
# https://ftp.ncbi.nih.gov/toolbox/ncbi_tools/converters/by_program/tbl2asn/linux64.tbl2asn.gz
#

SWISSKNIFE_VERSION=1.80
BARRNAP_VERSION=0.9
PROKKA_VERSION=1.14.5

docker build \
	--build-arg SWISSKNIFE_VERSION=${SWISSKNIFE_VERSION} \
	--build-arg BARRNAP_VERSION=${BARRNAP_VERSION} \
	--build-arg PROKKA_VERSION=${PROKKA_VERSION} \
	-t fgp-sars-cov-2-genome-annotation . &&
docker system prune -f
