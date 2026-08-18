## Script to combine the dimer cluster and interface cluster assignments to create a TSV file with the cluster assignments for all 3.12M interfaces

import numpy as np
import pandas as pd

def main():

    old_lookup = pd.read_csv('/fsimb/groups/imb-luckgr/imb-luckgr2/projects/interface_clustering/foldseek_dbs/pdb_20250313/dimerpdb.lookup', header=None, sep='\t')
    old_lookup.columns = ['chain_id','full_id','complex_id']
    old_index = pd.read_csv('/fsimb/groups/imb-luckgr/imb-luckgr2/projects/interface_clustering/foldseek_dbs/pdb_20250313/dimerpdb.index', header=None, sep='\t')
    old_index.columns = ['chain_id','start','len']
    old_lookup = old_lookup[old_lookup.chain_id.isin(old_index.chain_id)]

    old_lookup['pdb_id'] = [x.split('_')[1] if len(x.split('_')) > 2 else x.split('_')[0] for x in old_lookup.full_id]
    old_lookup['chain_id'] = [x.split('_')[-1] for x in old_lookup.full_id]
    old_lookup.drop(['full_id'], axis=1, inplace=True)
    old_lookup['idx'] = old_lookup.groupby('complex_id').cumcount()
    old_lookup = old_lookup.pivot(index='complex_id', columns='idx')[['pdb_id','chain_id']]
    old_lookup = old_lookup.sort_index(axis=1, level=1)
    old_lookup.columns = [f'{x}_{y}' for x,y in old_lookup.columns]
    old_lookup = old_lookup.reset_index()
    old_lookup.drop("pdb_id_1", inplace=True, axis=1)
    old_lookup.rename(columns={"pdb_id_0":"pdb_id", "complex_id":"old_complex_id"}, inplace=True)
    old_lookup['old'] = 1

    lookup = pd.read_csv('/fsimb/groups/imb-luckgr/imb-luckgr2/projects/interface_clustering/foldseek_dbs/pdb_20250911/dimerpdb.lookup', header=None, sep='\t')
    lookup.columns = ['chain_id','full_id','complex_id']
    print(type(lookup.complex_id))
    print(lookup.complex_id[0:10])

    index = pd.read_csv('/fsimb/groups/imb-luckgr/imb-luckgr2/projects/interface_clustering/foldseek_dbs/pdb_20250911/dimerpdb.index', header=None, sep='\t')
    index.columns = ['chain_id','start','len']
    
    lookup['pdb_id'] = [x.split('_')[1] if len(x.split('_')) > 2 else x.split('_')[0] for x in lookup.full_id]
    lookup['chain_id'] = [x.split('_')[-1] for x in lookup.full_id]
    lookup.drop(['full_id'], axis=1, inplace=True)
    lookup['idx'] = lookup.groupby('complex_id').cumcount()
    lookup = lookup.pivot(index='complex_id', columns='idx')[['pdb_id','chain_id']]
    lookup = lookup.sort_index(axis=1, level=1)
    lookup.columns = [f'{x}_{y}' for x,y in lookup.columns]
    lookup = lookup.reset_index()
    lookup.drop("pdb_id_1", inplace=True, axis=1)
    lookup.rename(columns={"pdb_id_0":"pdb_id", "complex_id":"new_complex_id"}, inplace=True)
    print(lookup.shape[0])
    print(lookup.head())

    merge = pd.merge(old_lookup, lookup, on=['pdb_id','chain_id_0','chain_id_1'], how='outer')
    merge.drop_duplicates(subset=["old_complex_id"], keep="first", inplace=True)
    print(merge.shape[0])
    
    dimerclu = pd.read_csv('/fsimb/groups/imb-luckgr/projects/interface_clustering/results/cluster_analysis/clu_mult90_chain50_clustermode0_cluster.tsv', header=None, sep='\t')
    dimerclu.columns = ['representative','member']
    dimerclu['dimercluster'] = pd.factorize(dimerclu.representative)[0]
    dimerclu['complex_id'] = [int(x.split('DI_')[0]) for x in dimerclu.member]
    print(dimerclu.complex_id[0:10])

    intclu = pd.read_csv('/fsimb/groups/imb-luckgr/projects/interface_clustering/results/cluster_analysis/interfaceclu40_0_cluster.tsv', header=None, sep='\t')
    intclu.columns = ['representative','member']
    intclu['intcluster'] = pd.factorize(intclu.representative)[0]
    intclu['member_complex_id'] = [int(x.split('DI')[0]) for x in intclu.member]
    intclu['rep_complex_id'] = [int(x.split('DI')[0]) for x in intclu.representative]
    dimerclu['intcluster'] = dimerclu.representative.map(dict(zip(intclu.member, intclu.intcluster)))
    print(intclu.member_complex_id[0:10])
    
    merge['dimercluster'] = merge.old_complex_id.map(dict(zip(dimerclu.complex_id, dimerclu.dimercluster)))   
    merge['intcluster'] = merge.old_complex_id.map(dict(zip(dimerclu.complex_id, dimerclu.intcluster)))

    dimerrep_complex_ids = set(intclu['member_complex_id'].values)
    intrep_complex_ids = set(intclu['rep_complex_id'].values)
    merge['dimerrep'] = [1 if x in dimerrep_complex_ids else 0 for x in merge['old_complex_id']]
    merge['intrep'] = [1 if x in intrep_complex_ids else 0 for x in merge['old_complex_id']]

    merge.to_csv('/fsimb/groups/imb-luckgr/projects/interface_clustering/results/cluster_analysis/pdb_clusters.tsv', sep='\t', index=None)

if __name__ == "__main__":
    main()

