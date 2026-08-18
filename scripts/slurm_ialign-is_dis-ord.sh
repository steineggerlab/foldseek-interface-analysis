#!/bin/bash
#SBATCH --cpus-per-task=24
#SBATCH --mem=100G

find /fsimb/groups/imb-luckgr/projects/interface_clustering/datasets/benchmarking/DMI > ~/dmi.lst

perl ~/ialign/bin/ialign.pl ~/dmi.lst -w ~/ialn_dmi/ -s -n ave -o /fsimb/groups/imb-luckgr/projects/interface_clustering/results/benchmarking/benchmark_alignment/ialign-is_dmi_results.txt -minp 2 -mini 2 -dc 5 &> /fsimb/groups/imb-luckgr/projects/interface_clustering/results/benchmarking/benchmark_alignment/ialign-is_dmi_output.txt

rm -rf ~/ialn_dmi
rm ~/dmi.lst
