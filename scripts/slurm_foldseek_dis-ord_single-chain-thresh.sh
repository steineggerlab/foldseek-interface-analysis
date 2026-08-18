#!/bin/bash
#SBATCH --cpus-per-task=24
#SBATCH --mem=256G

/home/stromjoe/foldseek/build_createinterfacedb/src/foldseek createdb /fsimb/groups/imb-luckgr/projects/interface_clustering/datasets/benchmarking/DMI /home/stromjoe/dmidb
/home/stromjoe/foldseek/build_createinterfacedb/src/foldseek createdimerdb /home/stromjoe/dmidb /home/stromjoe/dmidimerdb /home/stromjoe/tmp
/home/stromjoe/foldseek/build_createinterfacedb/src/foldseek createinterfacedb /home/stromjoe/dmidimerdb /home/stromjoe/dmiintdb

/home/stromjoe/foldseek/build_createinterfacedb/src/foldseek easy-multimersearch /home/stromjoe/dmiintdb /home/stromjoe/dmiintdb /fsimb/groups/imb-luckgr/projects/interface_clustering/results/benchmarking/test_scaling/dmi_lddt10 $TMPDIR --exhaustive-search 1 -e 10000000 --min-assigned-chains-ratio 1.0 --lddt-threshold 0.10

/home/stromjoe/foldseek/build_createinterfacedb/src/foldseek easy-multimersearch /home/stromjoe/dmiintdb /home/stromjoe/dmiintdb /fsimb/groups/imb-luckgr/projects/interface_clustering/results/benchmarking/test_scaling/dmi_lddt20 $TMPDIR --exhaustive-search 1 -e 10000000 --min-assigned-chains-ratio 1.0 --lddt-threshold 0.20

/home/stromjoe/foldseek/build_createinterfacedb/src/foldseek easy-multimersearch /home/stromjoe/dmiintdb /home/stromjoe/dmiintdb /fsimb/groups/imb-luckgr/projects/interface_clustering/results/benchmarking/test_scaling/dmi_lddt30 $TMPDIR --exhaustive-search 1 -e 10000000 --min-assigned-chains-ratio 1.0 --lddt-threshold 0.30

/home/stromjoe/foldseek/build_createinterfacedb/src/foldseek easy-multimersearch /home/stromjoe/dmiintdb /home/stromjoe/dmiintdb /fsimb/groups/imb-luckgr/projects/interface_clustering/results/benchmarking/test_scaling/dmi_lddt40 $TMPDIR --exhaustive-search 1 -e 10000000 --min-assigned-chains-ratio 1.0 --lddt-threshold 0.40

/home/stromjoe/foldseek/build_createinterfacedb/src/foldseek easy-multimersearch /home/stromjoe/dmiintdb /home/stromjoe/dmiintdb /fsimb/groups/imb-luckgr/projects/interface_clustering/results/benchmarking/test_scaling/dmi_lddt50 $TMPDIR --exhaustive-search 1 -e 10000000 --min-assigned-chains-ratio 1.0 --lddt-threshold 0.50

/home/stromjoe/foldseek/build_createinterfacedb/src/foldseek easy-multimersearch /home/stromjoe/dmiintdb /home/stromjoe/dmiintdb /fsimb/groups/imb-luckgr/projects/interface_clustering/results/benchmarking/test_scaling/dmi_lddt60 $TMPDIR --exhaustive-search 1 -e 10000000 --min-assigned-chains-ratio 1.0 --lddt-threshold 0.60

/home/stromjoe/foldseek/build_createinterfacedb/src/foldseek easy-multimersearch /home/stromjoe/dmiintdb /home/stromjoe/dmiintdb /fsimb/groups/imb-luckgr/projects/interface_clustering/results/benchmarking/test_scaling/dmi_lddt70 $TMPDIR --exhaustive-search 1 -e 10000000 --min-assigned-chains-ratio 1.0 --lddt-threshold 0.70

/home/stromjoe/foldseek/build_createinterfacedb/src/foldseek easy-multimersearch /home/stromjoe/dmiintdb /home/stromjoe/dmiintdb /fsimb/groups/imb-luckgr/projects/interface_clustering/results/benchmarking/test_scaling/dmi_lddt80 $TMPDIR --exhaustive-search 1 -e 10000000 --min-assigned-chains-ratio 1.0 --lddt-threshold 0.80

/home/stromjoe/foldseek/build_createinterfacedb/src/foldseek easy-multimersearch /home/stromjoe/dmiintdb /home/stromjoe/dmiintdb /fsimb/groups/imb-luckgr/projects/interface_clustering/results/benchmarking/test_scaling/dmi_lddt90 $TMPDIR --exhaustive-search 1 -e 10000000 --min-assigned-chains-ratio 1.0 --lddt-threshold 0.90

/home/stromjoe/foldseek/build_createinterfacedb/src/foldseek easy-multimersearch /home/stromjoe/dmiintdb /home/stromjoe/dmiintdb /fsimb/groups/imb-luckgr/projects/interface_clustering/results/benchmarking/test_scaling/dmi_tmscore10 $TMPDIR --exhaustive-search 1 -e 10000000 --min-assigned-chains-ratio 1.0 --tmscore-threshold 0.10

/home/stromjoe/foldseek/build_createinterfacedb/src/foldseek easy-multimersearch /home/stromjoe/dmiintdb /home/stromjoe/dmiintdb /fsimb/groups/imb-luckgr/projects/interface_clustering/results/benchmarking/test_scaling/dmi_tmscore20 $TMPDIR --exhaustive-search 1 -e 10000000 --min-assigned-chains-ratio 1.0 --tmscore-threshold 0.20

/home/stromjoe/foldseek/build_createinterfacedb/src/foldseek easy-multimersearch /home/stromjoe/dmiintdb /home/stromjoe/dmiintdb /fsimb/groups/imb-luckgr/projects/interface_clustering/results/benchmarking/test_scaling/dmi_tmscore30 $TMPDIR --exhaustive-search 1 -e 10000000 --min-assigned-chains-ratio 1.0 --tmscore-threshold 0.30

/home/stromjoe/foldseek/build_createinterfacedb/src/foldseek easy-multimersearch /home/stromjoe/dmiintdb /home/stromjoe/dmiintdb /fsimb/groups/imb-luckgr/projects/interface_clustering/results/benchmarking/test_scaling/dmi_tmscore40 $TMPDIR --exhaustive-search 1 -e 10000000 --min-assigned-chains-ratio 1.0 --tmscore-threshold 0.40

/home/stromjoe/foldseek/build_createinterfacedb/src/foldseek easy-multimersearch /home/stromjoe/dmiintdb /home/stromjoe/dmiintdb /fsimb/groups/imb-luckgr/projects/interface_clustering/results/benchmarking/test_scaling/dmi_tmscore50 $TMPDIR --exhaustive-search 1 -e 10000000 --min-assigned-chains-ratio 1.0 --tmscore-threshold 0.50

/home/stromjoe/foldseek/build_createinterfacedb/src/foldseek easy-multimersearch /home/stromjoe/dmiintdb /home/stromjoe/dmiintdb /fsimb/groups/imb-luckgr/projects/interface_clustering/results/benchmarking/test_scaling/dmi_tmscore60 $TMPDIR --exhaustive-search 1 -e 10000000 --min-assigned-chains-ratio 1.0 --tmscore-threshold 0.60

/home/stromjoe/foldseek/build_createinterfacedb/src/foldseek easy-multimersearch /home/stromjoe/dmiintdb /home/stromjoe/dmiintdb /fsimb/groups/imb-luckgr/projects/interface_clustering/results/benchmarking/test_scaling/dmi_tmscore70 $TMPDIR --exhaustive-search 1 -e 10000000 --min-assigned-chains-ratio 1.0 --tmscore-threshold 0.70

/home/stromjoe/foldseek/build_createinterfacedb/src/foldseek easy-multimersearch /home/stromjoe/dmiintdb /home/stromjoe/dmiintdb /fsimb/groups/imb-luckgr/projects/interface_clustering/results/benchmarking/test_scaling/dmi_tmscore80 $TMPDIR --exhaustive-search 1 -e 10000000 --min-assigned-chains-ratio 1.0 --tmscore-threshold 0.80

/home/stromjoe/foldseek/build_createinterfacedb/src/foldseek easy-multimersearch /home/stromjoe/dmiintdb /home/stromjoe/dmiintdb /fsimb/groups/imb-luckgr/projects/interface_clustering/results/benchmarking/test_scaling/dmi_tmscore90 $TMPDIR --exhaustive-search 1 -e 10000000 --min-assigned-chains-ratio 1.0 --tmscore-threshold 0.90

rm /home/stromjoe/dmidb*
rm /home/stromjoe/dmidimerdb*
rm /home/stromjoe/dmiintdb*