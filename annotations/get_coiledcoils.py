## Script to fetch annotations of coiled-coil domains from Uniprot. Results in TSV file with Uniprot IDs and Uniprot residue ranges for coiled-coil domains for all Uniprot IDs in the PDB interfaces

import numpy as np
import pandas as pd
import requests

def main():

    # From residue_mapping.py
    uniprot_mapping = pd.read_csv('/fsimb/groups/imb-luckgr/projects/interface_clustering/datasets/cluster_analysis/mapping/uniprot_residue_mapping.tsv', sep="\t")
    uniprot_acs = list(set(uniprot_mapping["uniprot_id"]))
    print("# Uniprot ACs to access: ", len(uniprot_acs))

    with open("/fsimb/groups/imb-luckgr/projects/interface_clustering/datasets/cluster_analysis/mapping/uniprot_coiledcoils.tsv", 'a') as f:
        f.write("uniprot_id\tft_coiled\n")

    batches = range(0, len(uniprot_acs), 20)

    for i in range(0, len(batches)):
        if batches[i] < batches[-1]:
            curr_acs = uniprot_acs[batches[i]:batches[i+1]]
            print("Batch #", i, ", Length of current list of Uniprot ACs: ", len(curr_acs))
        else:
            curr_acs = uniprot_acs[batches[i]:]
            print("Batch #", i, ", Length of current list of Uniprot ACs: ", len(curr_acs), " this is the last batch")
        curr_acs_str = "%20OR%20".join([str(x) for x in curr_acs])
        url = f"https://rest.uniprot.org/uniprotkb/search?query=accession:({curr_acs_str})&format=tsv&fields=accession,ft_coiled"
        coils = requests.get(url).text
        coils_without_header = "\n".join(coils.split("\n")[1:])
        print("Number of results: ", len(coils_without_header.split("\n")))
        
        with open("/fsimb/groups/imb-luckgr/projects/interface_clustering/datasets/cluster_analysis/mapping/uniprot_coiledcoils.tsv", 'a') as f:
            f.write(coils_without_header)

if __name__ == "__main__":
    main()