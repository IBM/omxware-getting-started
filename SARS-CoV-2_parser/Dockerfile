FROM ubuntu:bionic

LABEL maintainer="Ed Seabolt eseabolt@us.ibm.com"

ENV DEBIAN_FRONTEND=noninteractive

RUN \
	apt update && \
	apt upgrade -y && \
	apt install -y \
		bioperl \
		less \
		libdatetime-perl \
		libdigest-md5-perl \
		libxml-simple-perl \
		make \
		openjdk-8-jre \
		python3.7 \
		python3-pip wget

WORKDIR /root

ARG SWISSKNIFE_VERSION
ARG BARRNAP_VERSION
ARG PROKKA_VERSION

COPY swissknife_${SWISSKNIFE_VERSION}.tar.gz ./

RUN \
	tar xvf swissknife_${SWISSKNIFE_VERSION}.tar.gz && \
  cd swissknife_${SWISSKNIFE_VERSION} && \
  perl Makefile.PL && \
  make install && \
  cd - && \
  rm -f swissknife_${SWISSKNIFE_VERSION}.tar.gz

COPY barrnap-${BARRNAP_VERSION}.tar.gz ./

RUN \
	tar xvf barrnap-${BARRNAP_VERSION}.tar.gz && \
  rm -f barrnap-${BARRNAP_VERSION}.tar.gz

COPY prokka-${PROKKA_VERSION}.tar.gz ./

RUN \
	tar xvf prokka-${PROKKA_VERSION}.tar.gz && \
  rm -f prokka-${PROKKA_VERSION}.tar.gz

COPY *.patch ./

RUN \
	patch prokka-${PROKKA_VERSION}/bin/prokka prokka.patch && \
	patch prokka-${PROKKA_VERSION}/bin/prokka-uniprot_to_fasta_db prokka-uniprot_to_fasta_db.patch && \
	rm -f *.patch

ENV PATH "/root:/root/prokka-${PROKKA_VERSION}/bin:/root/prokka-${PROKKA_VERSION}/binaries/linux:/root/barrnap-${BARRNAP_VERSION}/bin:${PATH}"

RUN \
    wget -nv ftp://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/taxonomic_divisions/uniprot_sprot_bacteria.dat.gz && \
    wget -nv ftp://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/taxonomic_divisions/uniprot_sprot_viruses.dat.gz && \
    wget -nv ftp://ftp.uniprot.org/pub/databases/uniprot/pre_release/covid-19.dat && \
    gunzip uniprot_sprot_bacteria.dat.gz && \
    gunzip uniprot_sprot_viruses.dat.gz && \
    prokka-uniprot_to_fasta_db --term Bacteria uniprot_sprot_bacteria.dat > sprot && \
    mv sprot ./prokka-${PROKKA_VERSION}/db/kingdom/Bacteria/sprot && \
    prokka-uniprot_to_fasta_db --term Viruses uniprot_sprot_viruses.dat > sprot1 && \
    prokka-uniprot_to_fasta_db --verbose --term Viruses --evidence 4 --covid19 covid-19.dat > sprot2 && \
    cat sprot1 sprot2 > sprot && \
    mv sprot ./prokka-${PROKKA_VERSION}/db/kingdom/Viruses/sprot && \
    rm -f covid-19.dat sprot1 sprot2 uniprot_sprot_bacteria.dat uniprot_sprot_viruses.dat && \
    ./prokka-${PROKKA_VERSION}/bin/prokka --setupdb

COPY requirements.txt ./

RUN \
		python3.7 -m pip install --upgrade pip && \
		python3.7 -m pip install -r requirements.txt && \
		rm -f requirements.txt

COPY covid19_prodigal_parser.py covid19_ref_proteins.fasta pp1ab_full_translate.py pp1a_reference.fasta ./

# tbl2asn has an internal date check which will cause the program to fail if the date has passed. Therefore, instead
# of relying on the version provided by Prokka, we include it here so we can maintain it.
COPY tbl2asn ./prokka-${PROKKA_VERSION}/binaries/linux

COPY prokka.sh prodigal_wrapper.sh ./

ENTRYPOINT ["prokka.sh"]