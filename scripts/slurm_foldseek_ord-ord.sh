#!/bin/bash
# cpus-per-task=24
#SBATCH --mem=100G

/home/stromjoe/foldseek/build_createinterfacedb/src/foldseek createdb /fsimb/groups/imb-luckgr/projects/interface_clustering/datasets/benchmarking/DDI /home/stromjoe/ddidb
/home/stromjoe/foldseek/build_createinterfacedb/src/foldseek createdimerdb /home/stromjoe/ddidb /home/stromjoe/ddidimerdb /home/stromjoe/tmp
/home/stromjoe/foldseek/build_createinterfacedb/src/foldseek createinterfacedb /home/stromjoe/ddidimerdb /home/stromjoe/ddiintdb
/home/stromjoe/foldseek/build_createinterfacedb/src/foldseek easy-multimersearch /home/stromjoe/ddiintdb /home/stromjoe/ddiintdb /fsimb/groups/imb-luckgr/projects/interface_clustering/results/benchmarking/benchmark_alignment/foldseek_ddi_aln $TMPDIR --exhaustive-search 1 -e 10000000 --lddt-threshold 0.20 --min-assigned-chains-ratio 1.0 --threads 1

rm /home/stromjoe/ddidb*
rm /home/stromjoe/ddidimerdb*
rm /home/stromjoe/ddiintdb*