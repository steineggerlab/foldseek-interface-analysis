## Script to annotate PDB chains with Uniprot IDs where available from EMBL-EBI SIFTS database, and to convert PDB seq res IDs for interface residues to Uniprot residue IDs (necessary for further processing of annotations, i.e. IUPred2A scores which are provided for full-length canonical Uniprot sequences). Output is a TSV file with the PDB ID, chain ID, interface ID, list of interface residues as PDB seq res IDs, and list of interface residues as Uniprot residue indices.

import numpy as np
import pandas as pd
import struct, json

def get_int_list(r, byte_data):
    first = r['first']
    length = r['len']
    curr_window = byte_data[first:(first+length+1)]
    num_integers = len(curr_window) // 4
    integers = list(struct.unpack(f"<{num_integers}I", curr_window[:num_integers*4]))
    return ','.join([str(x) for x in integers])

def get_chain_ids(x):
    return '_'.join(list(x.chain_id))

def get_uniprot_res(r):
    uniprot_res_list = []
    if r['range'] is not np.nan:
        for ifres in [int(x) for x in r['if_res'].split(',')]:
            if ifres in range(r['range'][0],r['range'][1]):
                uniprot_res_list.append(ifres + r['shift'])
        return ','.join([str(int(x)) for x in uniprot_res_list])
    else:
        return None

def main():
    # Get interface residues from intdb
    lookup = pd.read_csv('/fsimb/groups/imb-luckgr/imb-luckgr2/projects/interface_clustering/foldseek_dbs/pdb_20250911/intpdb.lookup', header=None, sep='\t')
    lookup.columns = ['chain_index','full_id','complex_id']

    index = pd.read_csv('/fsimb/groups/imb-luckgr/imb-luckgr2/projects/interface_clustering/foldseek_dbs/pdb_20250911/intpdb_id.index', header=None, sep='\t')
    index.columns = ['chain_index','first','len']

    dimer_index = pd.read_csv('/fsimb/groups/imb-luckgr/imb-luckgr2/projects/interface_clustering/foldseek_dbs/pdb_20250911/dimerpdb.index', header=None, sep="\t")
    dimer_index.columns = ['chain_index','first','len']

    with open('/fsimb/groups/imb-luckgr/imb-luckgr2/projects/interface_clustering/foldseek_dbs/pdb_20250911/intpdb_id', 'rb') as f:
        byte_data = f.read()

    index['if_res'] = index.apply(lambda x: get_int_list(x, byte_data), axis=1)

    index['new_complex_id'] = index['chain_index'].map(dict(zip(lookup.chain_index, lookup.complex_id)))
    index['new_complex_id'] = [int(x) for x in index.new_complex_id]
    index['full_id'] = index['chain_index'].map(dict(zip(lookup.chain_index, lookup.full_id)))
    index['pdb_id'] = [str(x.split("_")[1].split("-")[0]) for x in index.full_id]
    index['chain_id'] = [str(x.split("_")[-1].split("-")[0]) for x in index.full_id]

    mapping = pd.read_csv('/fsimb/groups/imb-luckgr/projects/interface_clustering/datasets/cluster_analysis/mapping/pdb_chain_uniprot.tsv', sep='\t', skiprows=1)
    mapping['shift'] = mapping['SP_BEG'] - mapping['RES_BEG']
    mapping['range'] = mapping[['RES_BEG','RES_END']].apply(lambda x: [x['RES_BEG'],x['RES_END']], axis=1)
    
    res_maps = pd.merge(index, mapping[['PDB','CHAIN','SP_PRIMARY','shift','range']], left_on=['pdb_id','chain_id'], right_on=['PDB','CHAIN'], how='left')
    res_maps[res_maps['SP_PRIMARY'].isna()].drop_duplicates(subset=['pdb_id','chain_id']).to_csv('/fsimb/groups/imb-luckgr/projects/interface_clustering/results/cluster_analysis/pdb_chains_not_mapped.csv')

    res_maps['uniprot_res'] = res_maps.apply(lambda x: get_uniprot_res(x), axis=1)

    res_maps.drop(["first","len","PDB","CHAIN","shift","range"], inplace=True, axis=1)
    res_maps.rename(columns={"SP_PRIMARY":"uniprot_id"}, inplace=True)
    res_maps.drop_duplicates(subset=["full_id","uniprot_id","uniprot_res"], inplace=True, keep="first")
    print(res_maps.shape[0])
    
    combined_uni_res = res_maps[~res_maps["uniprot_res"].isna()].groupby(["full_id","uniprot_id"]).apply(lambda x: ",".join(x["uniprot_res"])).to_frame()
    combined_uni_res.columns = ["uniprot_res"]

    find_dups = res_maps[((res_maps["full_id"].duplicated(keep=False)) & (res_maps["uniprot_res"].isna()))]
    dups_do_not_drop = list(set(find_dups[find_dups["full_id"].duplicated(keep=False)].full_id))

    merge = pd.merge(res_maps, combined_uni_res, on=["full_id","uniprot_id"], how="left")
    merge.loc[merge["full_id"].isin(dups_do_not_drop), "uniprot_res_x"] = "not null :)"
    merge.loc[merge.duplicated(subset=["full_id","uniprot_id"], keep=False), "uniprot_res_x"] = merge.loc[merge.duplicated(subset=["full_id","uniprot_id"], keep=False), "uniprot_res_y"]
    merge.drop_duplicates(subset=["full_id","uniprot_id","uniprot_res_x"], keep="first", inplace=True)
    merge.loc[merge["full_id"].duplicated(keep=False), "chimeric"] = 1
    mask = ((merge["chimeric"] == 1) & (merge["uniprot_res_x"].isna()))
    print(len(list(set(merge.full_id))))
    merge = merge[~mask]
    print(len(list(set(merge.full_id))))
    merge.loc[merge["full_id"].duplicated(keep=False), "uniprot_id"] = "chimeric"
    merge.loc[merge["uniprot_id"] == "chimeric", "uniprot_res_x"] = np.nan
    merge.drop_duplicates(subset=["full_id"], keep="first", inplace=True)
    print(merge.shape[0])

    merge.rename(columns={"uniprot_res_x":"uniprot_res"}, inplace=True)
    merge.drop(["uniprot_res_y","chimeric"], axis=1, inplace=True)
    merge.loc[merge["uniprot_res"] == "not null :)", "uniprot_res"] = np.nan

    merge["FLlen"] = merge["chain_index"].map(dict(zip(dimer_index.chain_index, dimer_index.len)))

    merge.to_csv('/fsimb/groups/imb-luckgr/projects/interface_clustering/datasets/cluster_analysis/mapping/uniprot_residue_mapping.tsv', sep='\t', index=None)

if __name__ == "__main__":
    main()