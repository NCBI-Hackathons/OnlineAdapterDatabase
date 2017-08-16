#!/bin/bash

# Thanks to Sean Davis for pointing us to this database
# (not included in AB repo because it's ~30 GB)A
# download SRAdb
curl -L -O http://gbnci.abcc.ncifcrf.gov/backup/SRAmetadb.sqlite.gz

# gunzip
gunzip SRAmetadb.sqlite.gz

# Start up sqlite3 and query
sqlite3 SRAmetadb.sqlite < sra_query.text

# Get rid of carriage returns
perl -i -pe 's/\r//' datasources/sra_query_results.csv

# Detect adapters with Atropos
OLDIFS=$IFS
IFS=$'\n'
for i in $(cat datasources/sra_query_results.csv); do
    echo -e "\n\n-------------------------------------------------------------------------------\n$i\n";
    atropos detect --sra ${i%,*} -d known
    rm ~/ncbi/public/sra/* #to keep cache files from accumulating!
done >> datasources/atropos.out
IFS=$OLDIFS

# Parse Atropos results into csv
perl scripts/parseAtropos.pl datasources/atropos.out
