#!/bin/bash
#SBATCH --cpus-per-task=24
#SBATCH --mem=750GB

/home/stromjoe/foldseek/build_cae260b/src/foldseek createdb /fsimb/groups/imb-luckgr/imb-luckgr2/projects/interface_clustering/pdb-assemblies_download_20250313/ /fsimb/groups/imb-luckgr/imb-luckgr2/projects/interface_clustering/foldseek_dbs/pdb_20250313/pdb

/home/stromjoe/foldseek/build_cae260b/src/foldseek createdimerdb /fsimb/groups/imb-luckgr/imb-luckgr2/projects/interface_clustering/foldseek_dbs/pdb_20250313/pdb /fsimb/groups/imb-luckgr/imb-luckgr2/projects/interface_clustering/foldseek_dbs/pdb_20250313/dimerpdb /fsimb/groups/imb-luckgr/imb-luckgr2/projects/interface_clustering/tmp

rm -rf /fsimb/groups/imb-luckgr/imb-luckgr2/projects/interface_clustering/tmp
