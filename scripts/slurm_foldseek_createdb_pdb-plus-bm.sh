#!/bin/bash
#SBATCH --cpus-per-task=24
#SBATCH --mem=750G

/home/stromjoe/foldseek/build_createinterfacedb/src/foldseek createdb /fsimb/groups/imb-luckgr/imb-luckgr2/projects/interface_clustering/pdb-assemblies_download_20250313/ /home/stromjoe/pdb_plusbmdb

/home/stromjoe/foldseek/build_createinterfacedb/src/foldseek createdimerdb /home/stromjoe/pdb_plusbmdb /home/stromjoe/pdb_plusbm_dimerdb /home/stromjoe/tmp

/home/stromjoe/foldseek/build_createinterfacedb/src/foldseek createinterfacedb /home/stromjoe/pdb_plusbm_dimerdb /home/stromjoe/pdb_plusbm_intdb

mv /home/stromjoe/pdb_plusbm* /fsimb/groups/imb-luckgr/projects/interface_clustering/datasets/benchmarking/test_scaling/foldseek_dbs/