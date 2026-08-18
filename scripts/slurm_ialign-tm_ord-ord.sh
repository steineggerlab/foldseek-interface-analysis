#!/bin/bash
#SBATCH --cpus-per-task=24
#SBATCH --mem=100G

find /fsimb/groups/imb-luckgr/projects/interface_clustering/datasets/benchmarking/DDI > ~/ddi.lst

perl ~/ialign/bin/ialign.pl ~/ddi.lst -w ~/ialn_ddi/ -s -n ave -e tm -o /fsimb/groups/imb-luckgr/projects/interface_clustering/results/benchmarking/benchmark_alignment/ialign-tm_ddi_results.txt -minp 2 -mini 2 -dc 5 &> /fsimb/groups/imb-luckgr/projects/interface_clustering/results/benchmarking/benchmark_alignment/ialign-tm_ddi_output.txt

rm -rf ~/ialn_ddi
rm ~/ddi.lst
