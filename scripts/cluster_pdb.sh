#!/bin/bash


foldseek createdimerdb PDB PDB_dimer tmp1

foldseek multimercluster PDB_dimer clu tmp2 -c 0 --multimer-tm-threshold 0.9 --chain-tm-threshold 0.5 --interface-lddt-threshold 0 --cov-mode 0 --cluster-mode 0

foldseek createsubdb clu PDB_dimer PDB_dimer_reps

foldseek createinterfacedb PDB_dimer_reps PDB_int

foldseek easy-multimercluster PDB_int PDB_int_clu tmp3 --exhaustive-search -e 10000000 --lddt-threshold 0.20 --chain-tm-threshold 0 -c 0 --interface-lddt-threshold 0 --cov-mode 0 --cluster-mode 0 --max-iterations 1 --multimer-tm-threshold 0.4

# We now have PDB_int_clu_clustser.tsv
