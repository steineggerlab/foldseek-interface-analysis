#!/bin/bash
#SBATCH --cpus-per-task=64
#SBATCH --mem=1T

/home/stromjoe/foldseek/build_b927a71/src/foldseek createdb /fsimb/groups/imb-luckgr/imb-luckgr2/projects/interface_clustering/pdb-assemblies_download_20250313/ /fsimb/groups/imb-luckgr/imb-luckgr2/projects/interface_clustering/foldseek_dbs/pdb_20250911/pdb --save-res-index
/home/stromjoe/foldseek/build_b927a71/src/foldseek createdimerdb /fsimb/groups/imb-luckgr/imb-luckgr2/projects/interface_clustering/foldseek_dbs/pdb_20250911/pdb /fsimb/groups/imb-luckgr/imb-luckgr2/projects/interface_clustering/foldseek_dbs/pdb_20250911/dimerpdb /fsimb/groups/imb-luckgr/imb-luckgr2/projects/interface_clustering/tmp
/home/stromjoe/foldseek/build_b927a71/src/foldseek createinterfacedb /fsimb/groups/imb-luckgr/imb-luckgr2/projects/interface_clustering/foldseek_dbs/pdb_20250911/dimerpdb /fsimb/groups/imb-luckgr/imb-luckgr2/projects/interface_clustering/foldseek_dbs/pdb_20250911/intpdb
