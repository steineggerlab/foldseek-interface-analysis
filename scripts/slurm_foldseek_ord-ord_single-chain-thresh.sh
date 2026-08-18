#!/bin/bash
#SBATCH --cpus-per-task=24
#SBATCH --mem=256G

/home/stromjoe/foldseek/build_createinterfacedb/src/foldseek createdb /fsimb/groups/imb-luckgr/projects/interface_clustering/datasets/benchmarking/DDI /home/stromjoe/ddidb
/home/stromjoe/foldseek/build_createinterfacedb/src/foldseek createdimerdb /home/stromjoe/ddidb /home/stromjoe/ddidimerdb /home/stromjoe/tmp
/home/stromjoe/foldseek/build_createinterfacedb/src/foldseek createinterfacedb /home/stromjoe/ddidimerdb /home/stromjoe/ddiintdb

/home/stromjoe/foldseek/build_createinterfacedb/src/foldseek easy-multimersearch /home/stromjoe/ddiintdb /home/stromjoe/ddiintdb /fsimb/groups/imb-luckgr/projects/interface_clustering/results/benchmarking/test_scaling/ddi_lddt10 $TMPDIR --exhaustive-search 1 -e 10000000 --min-assigned-chains-ratio 1.0 --lddt-threshold 0.10

/home/stromjoe/foldseek/build_createinterfacedb/src/foldseek easy-multimersearch /home/stromjoe/ddiintdb /home/stromjoe/ddiintdb /fsimb/groups/imb-luckgr/projects/interface_clustering/results/benchmarking/test_scaling/ddi_lddt20 $TMPDIR --exhaustive-search 1 -e 10000000 --min-assigned-chains-ratio 1.0 --lddt-threshold 0.20

/home/stromjoe/foldseek/build_createinterfacedb/src/foldseek easy-multimersearch /home/stromjoe/ddiintdb /home/stromjoe/ddiintdb /fsimb/groups/imb-luckgr/projects/interface_clustering/results/benchmarking/test_scaling/ddi_lddt30 $TMPDIR --exhaustive-search 1 -e 10000000 --min-assigned-chains-ratio 1.0 --lddt-threshold 0.30

/home/stromjoe/foldseek/build_createinterfacedb/src/foldseek easy-multimersearch /home/stromjoe/ddiintdb /home/stromjoe/ddiintdb /fsimb/groups/imb-luckgr/projects/interface_clustering/results/benchmarking/test_scaling/ddi_lddt40 $TMPDIR --exhaustive-search 1 -e 10000000 --min-assigned-chains-ratio 1.0 --lddt-threshold 0.40

/home/stromjoe/foldseek/build_createinterfacedb/src/foldseek easy-multimersearch /home/stromjoe/ddiintdb /home/stromjoe/ddiintdb /fsimb/groups/imb-luckgr/projects/interface_clustering/results/benchmarking/test_scaling/ddi_lddt50 $TMPDIR --exhaustive-search 1 -e 10000000 --min-assigned-chains-ratio 1.0 --lddt-threshold 0.50

/home/stromjoe/foldseek/build_createinterfacedb/src/foldseek easy-multimersearch /home/stromjoe/ddiintdb /home/stromjoe/ddiintdb /fsimb/groups/imb-luckgr/projects/interface_clustering/results/benchmarking/test_scaling/ddi_lddt60 $TMPDIR --exhaustive-search 1 -e 10000000 --min-assigned-chains-ratio 1.0 --lddt-threshold 0.60

/home/stromjoe/foldseek/build_createinterfacedb/src/foldseek easy-multimersearch /home/stromjoe/ddiintdb /home/stromjoe/ddiintdb /fsimb/groups/imb-luckgr/projects/interface_clustering/results/benchmarking/test_scaling/ddi_lddt70 $TMPDIR --exhaustive-search 1 -e 10000000 --min-assigned-chains-ratio 1.0 --lddt-threshold 0.70

/home/stromjoe/foldseek/build_createinterfacedb/src/foldseek easy-multimersearch /home/stromjoe/ddiintdb /home/stromjoe/ddiintdb /fsimb/groups/imb-luckgr/projects/interface_clustering/results/benchmarking/test_scaling/ddi_lddt80 $TMPDIR --exhaustive-search 1 -e 10000000 --min-assigned-chains-ratio 1.0 --lddt-threshold 0.80

/home/stromjoe/foldseek/build_createinterfacedb/src/foldseek easy-multimersearch /home/stromjoe/ddiintdb /home/stromjoe/ddiintdb /fsimb/groups/imb-luckgr/projects/interface_clustering/results/benchmarking/test_scaling/ddi_lddt90 $TMPDIR --exhaustive-search 1 -e 10000000 --min-assigned-chains-ratio 1.0 --lddt-threshold 0.90

/home/stromjoe/foldseek/build_createinterfacedb/src/foldseek easy-multimersearch /home/stromjoe/ddiintdb /home/stromjoe/ddiintdb /fsimb/groups/imb-luckgr/projects/interface_clustering/results/benchmarking/test_scaling/ddi_tmscore10 $TMPDIR --exhaustive-search 1 -e 10000000 --min-assigned-chains-ratio 1.0 --tmscore-threshold 0.10

/home/stromjoe/foldseek/build_createinterfacedb/src/foldseek easy-multimersearch /home/stromjoe/ddiintdb /home/stromjoe/ddiintdb /fsimb/groups/imb-luckgr/projects/interface_clustering/results/benchmarking/test_scaling/ddi_tmscore20 $TMPDIR --exhaustive-search 1 -e 10000000 --min-assigned-chains-ratio 1.0 --tmscore-threshold 0.20

/home/stromjoe/foldseek/build_createinterfacedb/src/foldseek easy-multimersearch /home/stromjoe/ddiintdb /home/stromjoe/ddiintdb /fsimb/groups/imb-luckgr/projects/interface_clustering/results/benchmarking/test_scaling/ddi_tmscore30 $TMPDIR --exhaustive-search 1 -e 10000000 --min-assigned-chains-ratio 1.0 --tmscore-threshold 0.30

/home/stromjoe/foldseek/build_createinterfacedb/src/foldseek easy-multimersearch /home/stromjoe/ddiintdb /home/stromjoe/ddiintdb /fsimb/groups/imb-luckgr/projects/interface_clustering/results/benchmarking/test_scaling/ddi_tmscore40 $TMPDIR --exhaustive-search 1 -e 10000000 --min-assigned-chains-ratio 1.0 --tmscore-threshold 0.40

/home/stromjoe/foldseek/build_createinterfacedb/src/foldseek easy-multimersearch /home/stromjoe/ddiintdb /home/stromjoe/ddiintdb /fsimb/groups/imb-luckgr/projects/interface_clustering/results/benchmarking/test_scaling/ddi_tmscore50 $TMPDIR --exhaustive-search 1 -e 10000000 --min-assigned-chains-ratio 1.0 --tmscore-threshold 0.50

/home/stromjoe/foldseek/build_createinterfacedb/src/foldseek easy-multimersearch /home/stromjoe/ddiintdb /home/stromjoe/ddiintdb /fsimb/groups/imb-luckgr/projects/interface_clustering/results/benchmarking/test_scaling/ddi_tmscore60 $TMPDIR --exhaustive-search 1 -e 10000000 --min-assigned-chains-ratio 1.0 --tmscore-threshold 0.60

/home/stromjoe/foldseek/build_createinterfacedb/src/foldseek easy-multimersearch /home/stromjoe/ddiintdb /home/stromjoe/ddiintdb /fsimb/groups/imb-luckgr/projects/interface_clustering/results/benchmarking/test_scaling/ddi_tmscore70 $TMPDIR --exhaustive-search 1 -e 10000000 --min-assigned-chains-ratio 1.0 --tmscore-threshold 0.70

/home/stromjoe/foldseek/build_createinterfacedb/src/foldseek easy-multimersearch /home/stromjoe/ddiintdb /home/stromjoe/ddiintdb /fsimb/groups/imb-luckgr/projects/interface_clustering/results/benchmarking/test_scaling/ddi_tmscore80 $TMPDIR --exhaustive-search 1 -e 10000000 --min-assigned-chains-ratio 1.0 --tmscore-threshold 0.80

/home/stromjoe/foldseek/build_createinterfacedb/src/foldseek easy-multimersearch /home/stromjoe/ddiintdb /home/stromjoe/ddiintdb /fsimb/groups/imb-luckgr/projects/interface_clustering/results/benchmarking/test_scaling/ddi_tmscore90 $TMPDIR --exhaustive-search 1 -e 10000000 --min-assigned-chains-ratio 1.0 --tmscore-threshold 0.90

rm /home/stromjoe/ddidb*
rm /home/stromjoe/ddidimerdb*
rm /home/stromjoe/ddiintdb*