## Script to fetch gene names for each PDB chain from PDBe API based on PDB ID and author chain ID.

import numpy as np
import pandas as pd
import requests, json

def main():

    # Read in file from previous runs to avoid duplicating work
    gene_name_mapped = pd.read_csv("/fsimb/groups/imb-luckgr/projects/interface_clustering/datasets/cluster_analysis/mapping/pdb_gene-name_mapping.tsv", sep="\t")
    mapped_pdbs = list(set(gene_name_mapped["pdb_id"]))

    # File with all removed PDB IDs and the superseding ID where available, downloaded from RCSB
    with open('/fsimb/groups/imb-luckgr/projects/interface_clustering/datasets/cluster_analysis/mapping/all_removed_entries.json', encoding='utf8') as json_file:
        removed_entries_dict = json.load(json_file)

    # From residue_mapping.py
    uniprot_mapping = pd.read_csv('/fsimb/groups/imb-luckgr/projects/interface_clustering/datasets/cluster_analysis/mapping/uniprot_residue_mapping.tsv', sep="\t")
    pdb_ids_to_fetch = list(set([x[0:4] for x in uniprot_mapping["pdb_id"] if x not in mapped_pdbs]))
    print("# PDB IDs to access: ", len(pdb_ids_to_fetch))

    url = "https://www.ebi.ac.uk/pdbe/api/pdb/entry/molecules/"

    pdb_ids = []
    chain_ids = []
    gene_names = []

    for i in pdb_ids_to_fetch:
        if i.upper() in removed_entries_dict.keys():
            try:
                id_to_fetch = removed_entries_dict[i.upper()]["superseded_by"][0].lower()
            except:
                id_to_fetch = i
        else:
            id_to_fetch = i
        try:
            response = requests.get(url+id_to_fetch).json()
            for item in response[id_to_fetch]:
                if "polypeptide" in item["molecule_type"]:
                    if item["gene_name"] is not None:
                        gene_name = ",".join(item["gene_name"])
                    else:
                        gene_name = "NA"
                    for chain_id in item["in_chains"]:
                        pdb_ids.append(i)
                        chain_ids.append(chain_id)
                        gene_names.append(gene_name)
        except:
            print(id_to_fetch + " (original id " + i + ") : unable to fetch gene names")
    
    gene_name_map = pd.DataFrame({"pdb_id":pdb_ids, "chain_id":chain_ids, "gene_names":gene_names})
    gene_name_tosave = pd.concat([gene_name_mapped, gene_name_map], axis=0)
    gene_name_tosave.to_csv("/fsimb/groups/imb-luckgr/projects/interface_clustering/datasets/cluster_analysis/mapping/pdb_gene-name_mapping.tsv", sep="\t", index=None)

if __name__ == "__main__":
    main()