#!/bin/bash
# cpus-per-task=24
#SBATCH --mem=100G

/home/stromjoe/foldseek/build_createinterfacedb/src/foldseek createdb /fsimb/groups/imb-luckgr/projects/interface_clustering/datasets/benchmarking/DMI /home/stromjoe/dmidb
/home/stromjoe/foldseek/build_createinterfacedb/src/foldseek createdimerdb /home/stromjoe/dmidb /home/stromjoe/dmidimerdb /home/stromjoe/tmp
/home/stromjoe/foldseek/build_createinterfacedb/src/foldseek createinterfacedb /home/stromjoe/dmidimerdb /home/stromjoe/dmiintdb
/home/stromjoe/foldseek/build_createinterfacedb/src/foldseek easy-multimersearch /home/stromjoe/dmiintdb /home/stromjoe/dmiintdb /fsimb/groups/imb-luckgr/projects/interface_clustering/results/benchmarking/benchmark_alignment/foldseek_dmi_aln $TMPDIR --exhaustive-search 1 -e 10000000 --lddt-threshold 0.20 --min-assigned-chains-ratio 1.0 --threads 1

rm /home/stromjoe/dmidb*
rm /home/stromjoe/dmidimerdb*
rm /home/stromjoe/dmiintdb*