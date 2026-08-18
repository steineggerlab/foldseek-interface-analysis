## Script to fetch Pfam domain annotations and start and end PDB seq res ID boundaries from PDBe API based on PDB ID and author chain ID.

import numpy as np
import pandas as pd
import requests

def main():

    # From residue_mapping.py
    uniprot_mapping = pd.read_csv('/fsimb/groups/imb-luckgr/projects/interface_clustering/datasets/cluster_analysis/mapping/uniprot_residue_mapping.tsv', sep="\t")
    pdb_ids_to_fetch = list(set([x[0:4] for x  in uniprot_mapping["pdb_id"]]))
    print("# PDB IDs to access: ", len(pdb_ids_to_fetch))

    url = "https://www.ebi.ac.uk/pdbe/api/v2/mappings/pfam/"

    pdb_ids = []
    chain_ids = []
    starts = []
    ends = []
    pfam_names = []
    pfam_ids = []

    for pdb_id in pdb_ids_to_fetch:
        response = requests.get(url+pdb_id).json()
        try:
            for k,v in response[pdb_id]["Pfam"].items():
                for entry in v["mappings"]:
                    pdb_ids.append(pdb_id)
                    chain_ids.append(entry["chain_id"])
                    starts.append(str(entry["start"]["residue_number"]))
                    ends.append(str(entry["end"]["residue_number"]))
                    pfam_names.append(v["description"])
                    pfam_ids.append(k)
        except:
            print(pdb_id, ": key not found in API response")

    pdb_pfam = pd.DataFrame({"pdb_id":pdb_ids, "chain_id":chain_ids, "start":starts, "end":ends, "pfam_name":pfam_names, "pfam_id":pfam_ids})
    pdb_pfam.to_csv("/fsimb/groups/imb-luckgr/projects/interface_clustering/datasets/cluster_analysis/mapping/pdb_pfam.tsv", sep="\t", index=None)

if __name__ == "__main__":
    main()