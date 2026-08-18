#!/bin/bash
# cpus-per-task=24
#SBATCH --mem=100G

/home/stromjoe/foldseek/build_createinterfacedb/src/foldseek createdb /fsimb/groups/imb-luckgr/projects/interface_clustering/datasets/benchmarking/DDI /home/stromjoe/ddidb
/home/stromjoe/foldseek/build_createinterfacedb/src/foldseek createdimerdb /home/stromjoe/ddidb /home/stromjoe/ddidimerdb /home/stromjoe/tmp

/home/stromjoe/foldseek/build_createinterfacedb/src/foldseek easy-multimercluster /home/stromjoe/ddidimerdb /fsimb/groups/imb-luckgr/projects/interface_clustering/results/benchmarking/benchmark_cluster/ddidimer /home/stromjoe/tmp --multimer-tm-threshold 0.9 --chain-tm-threshold 0.5 --interface-lddt-threshold 0 --cov-mode 0 --cluster-mode 0 -c 0 --remove-tmp-files 0

/home/stromjoe/foldseek/build_createinterfacedb/src/foldseek createsubdb /home/stromjoe/tmp/latest/multimer_rep_seqs.index /home/stromjoe/ddidimerdb /home/stromjoe/ddisubdb
/home/stromjoe/foldseek/build_createinterfacedb/src/foldseek createinterfacedb /home/stromjoe/ddisubdb /home/stromjoe/ddisubintdb

/home/stromjoe/foldseek/build_createinterfacedb/src/foldseek easy-multimercluster /home/stromjoe/ddisubintdb /fsimb/groups/imb-luckgr/projects/interface_clustering/results/benchmarking/benchmark_cluster/ddidimerrepint_0.3 /home/stromjoe/tmp -e 10000000 --exhaustive-search --lddt-threshold 0.20 --multimer-tm-threshold 0.3 --chain-tm-threshold 0 --interface-lddt-threshold 0 --cov-mode 0 --cluster-mode 0 -c 0

/home/stromjoe/foldseek/build_createinterfacedb/src/foldseek easy-multimercluster /home/stromjoe/ddisubintdb /fsimb/groups/imb-luckgr/projects/interface_clustering/results/benchmarking/benchmark_cluster/ddidimerrepint_0.4 /home/stromjoe/tmp -e 10000000 --exhaustive-search --lddt-threshold 0.20 --multimer-tm-threshold 0.4 --chain-tm-threshold 0 --interface-lddt-threshold 0 --cov-mode 0 --cluster-mode 0 -c 0

/home/stromjoe/foldseek/build_createinterfacedb/src/foldseek easy-multimercluster /home/stromjoe/ddisubintdb /fsimb/groups/imb-luckgr/projects/interface_clustering/results/benchmarking/benchmark_cluster/ddidimerrepint_0.5 /home/stromjoe/tmp -e 10000000 --exhaustive-search --lddt-threshold 0.20 --multimer-tm-threshold 0.5 --chain-tm-threshold 0 --interface-lddt-threshold 0 --cov-mode 0 --cluster-mode 0 -c 0