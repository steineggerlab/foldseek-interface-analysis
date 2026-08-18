## Script to extract fractions of secondary structure assignments to interface residues. Source data is downloaded from PDB-REDO. Data for each interface chain is extracted based on PDB ID, author chain ID, and PDB seq res ID. Output is a TSV file with the fractions of interface residues annotated with each secondary structure element. All helix/coil DSSP categories are combined, and both strand-like DSSP categories are combined.

import numpy as np
import pandas as pd
from Bio import PDB
import gzip

def main():

    # From residue_mapping.py
    res_map = pd.read_csv("/fsimb/groups/imb-luckgr/projects/interface_clustering/datasets/cluster_analysis/mapping/uniprot_residue_mapping.tsv", sep="\t")
    res_map["simple_pdb_id"] = [x[0:4] for x in res_map["pdb_id"]]
    res_map["simple_chain_id"] = [str(x).split("-")[0] for x in res_map["chain_id"]]

    pdb_ids_to_process = list(set(res_map["simple_pdb_id"]))

    complex_ids = []
    chain_ids = []
    helix_fracs = []
    beta_fracs = []
    turn_fracs = []
    bend_fracs = []
    other_fracs = []

    for pdb_id in pdb_ids_to_process:
        tmp_df = res_map[res_map["simple_pdb_id"] == pdb_id]

        # Downloaded mmCIF files from PDB-REDO
        with gzip.open(f"/fsimb/groups/imb-luckgr/imb-luckgr2/projects/interface_clustering/dssp_download_20251030/cif/{pdb_id[1:3]}/{pdb_id}.cif.gz", "r") as f:
            with open("/home/stromjoe/tmp_cif.cif", "wb") as g:
                for line in f.readlines():
                    g.write(line)

        cif_dict = PDB.MMCIF2Dict.MMCIF2Dict("/home/stromjoe/tmp_cif.cif")
        try:
            structdf = pd.DataFrame({"struct_type":cif_dict["_struct_conf.conf_type_id"],
                                    "auth_chain_id":cif_dict["_struct_conf.beg_auth_asym_id"],
                                    "beg_label_seq_id":cif_dict["_struct_conf.beg_label_seq_id"],
                                    "end_label_seq_id":cif_dict["_struct_conf.end_label_seq_id"]})
        except:
            print(pdb_id, ": DSSP CIF does not contain the required loop")
            continue
        else:
            label_seq_id = []
            struct_type = []
            chain_id = []
            for i,r in structdf.iterrows():
                begin = int(r["beg_label_seq_id"])
                end = int(r["end_label_seq_id"])+1
                label_seq_id.extend(list(range(begin, end)))
                chain_list = [r["auth_chain_id"]] * len(list(range(begin, end)))
                chain_id.extend(chain_list)
                struct_list = [r["struct_type"]] * len(list(range(begin, end)))
                struct_type.extend(struct_list)

            chain_id = pd.Series(chain_id)
            label_seq_id = pd.Series(label_seq_id)
            struct_type = pd.Series(struct_type)
            
            for i,r in tmp_df.iterrows():
                if_res = [int(x) for x in r['if_res'].split(',')]
                curr_chain_id = r["simple_chain_id"]
                mask = (chain_id == curr_chain_id) & (label_seq_id.isin(if_res))
                struct_type_if = pd.Series([x.split("_")[0] for x in struct_type[mask]])
                if len(struct_type_if) > 0:
                    helix_frac = len(struct_type_if[struct_type_if == "HELX"])/len(struct_type_if)
                    beta_frac =  len(struct_type_if[struct_type_if == "STRN"])/len(struct_type_if)
                    turn_frac = len(struct_type_if[struct_type_if == "TURN"])/len(struct_type_if)
                    bend_frac = len(struct_type_if[struct_type_if == "BEND"])/len(struct_type_if)
                    other_frac = len(struct_type_if[struct_type_if == "OTHER"])/len(struct_type_if)
                else:
                    helix_frac = np.nan
                    beta_frac = np.nan
                    turn_frac = np.nan
                    bend_frac = np.nan
                    other_frac = np.nan

                complex_ids.append(r["new_complex_id"])
                chain_ids.append(r["chain_id"])
                helix_fracs.append(helix_frac)
                beta_fracs.append(beta_frac)
                turn_fracs.append(turn_frac)
                bend_fracs.append(bend_frac)
                other_fracs.append(other_frac)
            
    struct_types_df = pd.DataFrame({"new_complex_id":complex_ids, "chain_id":chain_ids, "helix_frac":helix_fracs, "beta_frac":beta_fracs, "turn_frac":turn_fracs, "bend_frac":bend_fracs, "other_frac":other_fracs})
    struct_types_df.to_csv("/fsimb/groups/imb-luckgr/projects/interface_clustering/datasets/cluster_analysis/mapping/if_struct_types.tsv", sep="\t", index=None)

if __name__ == "__main__":
    main()