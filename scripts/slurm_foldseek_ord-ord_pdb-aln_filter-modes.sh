#!/bin/bash
# cpus-per-task=24
#SBATCH --mem=1T

/home/stromjoe/foldseek/build_createinterfacedb/src/foldseek createdb /fsimb/groups/imb-luckgr/projects/interface_clustering/datasets/benchmarking/DDI /home/stromjoe/ddidb
/home/stromjoe/foldseek/build_createinterfacedb/src/foldseek createdimerdb /home/stromjoe/ddidb /home/stromjoe/ddidimerdb /home/stromjoe/tmp
/home/stromjoe/foldseek/build_createinterfacedb/src/foldseek createinterfacedb /home/stromjoe/ddidimerdb /home/stromjoe/ddiintdb

/home/stromjoe/foldseek/build_createinterfacedb/src/foldseek easy-multimersearch /home/stromjoe/ddiintdb /fsimb/groups/imb-luckgr/projects/interface_clustering/datasets/benchmarking/test_scaling/foldseek_dbs/pdb_plusbm_intdb /fsimb/groups/imb-luckgr/projects/interface_clustering/results/benchmarking/test_scaling/ddi_pdb-plus-bm_aln_no-exhaust $TMPDIR -e 10000000 --spaced-kmer-mode 0 -k 5 --min-assigned-chains-ratio 1.0

/home/stromjoe/foldseek/build_createinterfacedb/src/foldseek easy-multimersearch /home/stromjoe/ddiintdb /fsimb/groups/imb-luckgr/projects/interface_clustering/datasets/benchmarking/test_scaling/foldseek_dbs/pdb_plusbm_intdb /fsimb/groups/imb-luckgr/projects/interface_clustering/results/benchmarking/test_scaling/ddi_pdb-plus-bm_aln_ungapped $TMPDIR --prefilter-mode 1 --min-ungapped-score 0 --min-assigned-chains-ratio 1.0

/home/stromjoe/foldseek/build_createinterfacedb/src/foldseek easy-multimersearch /home/stromjoe/ddiintdb /fsimb/groups/imb-luckgr/projects/interface_clustering/datasets/benchmarking/test_scaling/foldseek_dbs/pdb_plusbm_intdb /fsimb/groups/imb-luckgr/projects/interface_clustering/results/benchmarking/test_scaling/ddi_pdb-plus-bm_aln_lddt-thresh $TMPDIR -e 10000000 --exhaustive-search --lddt-threshold 0.20 --min-assigned-chains-ratio 1.0