#!/usr/bin/env bash

set -euo pipefail

CLUSTER=interfacecluster_expandedtodimers.tsv
SEQDB=/fast2/yewon1/AFCDB_analysis_data/foldseek_search_PDBe/foldseek_pdb_db/pdb_seq

awk -F'\t' '
  FNR==NR {                                   
    base=$2; sub(/_[^_]*$/,"",base);         
    keys[base]=(base in keys ? keys[base] SUBSEP $1 : $1);
    next
  }
  {                                           
    rb=$1; sub(/^[^_]*_/,"",rb);             
    mb=$2; sub(/^[^_]*_/,"",mb);
    if (!(rb in keys) || !(mb in keys)) next;
    split(keys[rb], rk, SUBSEP); repkey=rk[1];  
    n=split(keys[mb], mk, SUBSEP);
    for (i=1;i<=n;i++) print repkey"\t"mk[i];    
  }
' "${SEQDB}.lookup" "$CLUSTER" | sort -k1,1n > cluster.key.tsv

mmseqs tsv2db cluster.key.tsv clusterDB --output-dbtype 6

mmseqs lca            "$SEQDB" clusterDB lcaDB --tax-lineage 1
mmseqs createtsv      "$SEQDB" lcaDB lca_result.tsv
mmseqs taxonomyreport "$SEQDB" lcaDB report.kraken.txt
