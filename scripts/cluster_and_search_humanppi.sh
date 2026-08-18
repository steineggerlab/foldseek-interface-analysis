#!/bin/bash

mkdir -p tmp

foldseek createinterfacedb humanppi_original humanppi_intdb

# filter, maximum chain length >= 13
awk '{if($3>=15){hi=1}else{hi=0}; print $1"\t"hi}' humanppi_intdb.index > tmp/index_if13
awk 'NR%2==1{hi=$2; getline;hi+=$2; if(hi!=0){print int($1/2)}}' tmp/index_if13 > tmp/source_long
awk '{print $1*2"\n"$1*2+1}' tmp/source_long > tmp/index_long

foldseek createsubdb tmp/index_long humanppi_intdb humanppi_intdb_longdb


# cluster
foldseek easy-multimercluster humanppi_intdb_longdb humanppi_intdb_longdb_clu tmp --exhaustive-search -e 10000000 --lddt-threshold 0.20 --chain-tm-threshold 0 -c 0 --interface-lddt-threshold 0 --cov-mode 0 --cluster-mode 0 --max-iterations 1 --multimer-tm-threshold 0.4

# search
# make pdb interface representative db
foldseek createsubdb PDB_int_clu PDB_int PDB_int_rep

foldseek easy-multimersearch humanppi_intdb_longdb PDB_int_rep aln tmp2 --cov-mode 0

awk '$6>=0.4 || $7 >= 0.4{print $1}' aln_report | uniq > tmp/search_yeshit
awk 'FNR==NR{name[$1]=1; next}{if($2 in name){print $0"\t1"}else{print $0"\t0"}}' tmp/search_yeshit humanppi_intdb_longdb_clu_cluster.tsv tmp/clustertsv_01.tsv
cut -f1,3 tmp/clustertsv_01.tsv | uniq -c | awk '$1==1 && $3==0{print $2}' > tmp/clusterrep_novel
awk 'FNR==NR{name[$1]=1; next}{if($1 in name){print}}' tmp/clusterrep_novel humanppi_intdb_longdb_clu_cluster.tsv > humanppi_novelinterfacecluster_members.tsv
