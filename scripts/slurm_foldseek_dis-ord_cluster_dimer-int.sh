#!/bin/bash
# cpus-per-task=24
#SBATCH --mem=100G

/home/stromjoe/foldseek/build_createinterfacedb/src/foldseek createdb /fsimb/groups/imb-luckgr/projects/interface_clustering/datasets/benchmarking/DMI /home/stromjoe/dmidb
/home/stromjoe/foldseek/build_createinterfacedb/src/foldseek createdimerdb /home/stromjoe/dmidb /home/stromjoe/dmidimerdb /home/stromjoe/tmp

/home/stromjoe/foldseek/build_createinterfacedb/src/foldseek easy-multimercluster /home/stromjoe/dmidimerdb /fsimb/groups/imb-luckgr/projects/interface_clustering/results/benchmarking/benchmark_cluster/dmidimer /home/stromjoe/tmp --multimer-tm-threshold 0.9 --chain-tm-threshold 0.5 --interface-lddt-threshold 0 --cov-mode 0 --cluster-mode 0 -c 0 --remove-tmp-files 0

/home/stromjoe/foldseek/build_createinterfacedb/src/foldseek createsubdb /home/stromjoe/tmp/latest/multimer_rep_seqs.index /home/stromjoe/dmidimerdb /home/stromjoe/dmisubdb
/home/stromjoe/foldseek/build_createinterfacedb/src/foldseek createinterfacedb /home/stromjoe/dmisubdb /home/stromjoe/dmisubintdb

/home/stromjoe/foldseek/build_createinterfacedb/src/foldseek easy-multimercluster /home/stromjoe/dmisubintdb /fsimb/groups/imb-luckgr/projects/interface_clustering/results/benchmarking/benchmark_cluster/dmidimerrepint_0.3 /home/stromjoe/tmp -e 10000000 --exhaustive-search --lddt-threshold 0.20 --multimer-tm-threshold 0.3 --chain-tm-threshold 0 --interface-lddt-threshold 0 --cov-mode 0 --cluster-mode 0 -c 0

/home/stromjoe/foldseek/build_createinterfacedb/src/foldseek easy-multimercluster /home/stromjoe/dmisubintdb /fsimb/groups/imb-luckgr/projects/interface_clustering/results/benchmarking/benchmark_cluster/dmidimerrepint_0.4 /home/stromjoe/tmp -e 10000000 --exhaustive-search --lddt-threshold 0.20 --multimer-tm-threshold 0.4 --chain-tm-threshold 0 --interface-lddt-threshold 0 --cov-mode 0 --cluster-mode 0 -c 0

/home/stromjoe/foldseek/build_createinterfacedb/src/foldseek easy-multimercluster /home/stromjoe/dmisubintdb /fsimb/groups/imb-luckgr/projects/interface_clustering/results/benchmarking/benchmark_cluster/dmidimerrepint_0.5 /home/stromjoe/tmp -e 10000000 --exhaustive-search --lddt-threshold 0.20 --multimer-tm-threshold 0.5 --chain-tm-threshold 0 --interface-lddt-threshold 0 --cov-mode 0 --cluster-mode 0 -c 0