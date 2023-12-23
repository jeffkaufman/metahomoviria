#!/usr/bin/env bash

if [ ! -e human-viruses.tsv ]; then
  # TSV format is "ncbi taxid \t scientific name"
  # 9606 is the taxid for humans
  curl -sS https://www.genome.jp/ftp/db/virushostdb/virushostdb.tsv \
    | awk -F'\t' '$8=="9606"{print $1"\t"$2}' \
    | sort -n \
           > human-viruses.tsv
fi

if [ ! -e names.dmp ] ; then
  wget https://ftp.ncbi.nlm.nih.gov/pub/taxonomy/taxdump_archive/taxdmp_2023-12-01.zip
  unzip taxdmp_2023-12-01.zip
  rm taxdmp_2023-12-01.zip
fi
