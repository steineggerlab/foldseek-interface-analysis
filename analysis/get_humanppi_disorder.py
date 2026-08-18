## Script to fetch residue-level disorder for HumanPPI interfaces from IUPred2A API based on Uniprot ID. IUPred2A predictions are in short mode for the full-length canonical Uniprot sequence. Residues are considered disordered if the IUPred2A score is above 0.4. Interface residues are extracted from the full-length IUPred2A predictions based on the Uniprot residue indices for the interface residues. Output is a TSV file with the fraction of disordred residues for each chain for each interface, where data is available.

import numpy as np
import pandas as pd
import requests
import os
pd.options.mode.copy_on_write = True

def get_disorder_frac(r, iupred):
    try:
        ifres = [int(x) for x in str(r["if_res"]).split(",") if ((x != 'nan') & (x != ''))]
        if len(list(set(ifres).difference(iupred.index))) == 0:
            # Restrict disorder predictions to only the residues which are in interface
            iupredres = iupred[ifres]
            numdis = len(iupredres[iupredres > 0.4])
            numres = len(ifres)
        else:
            numdis = np.nan
            numres = len(ifres)
        if numres > 0:
            dis_frac = numdis/numres
        else:
            dis_frac = np.nan
        return dis_frac
    except:
        print(r["complex_id"], " ", r["uniprot"])

def main():

    # From humanppi_vs_pdb.ipynb
    humanppi_ifres = pd.read_csv('/fsimb/groups/imb-luckgr/projects/interface_clustering/results/bfmdvspdb/humanppi_only/humanppi_ifres.tsv', sep="\t")
    humanppi_ifres["chain_id"] = [x.split("_")[-1] for x in humanppi_ifres.chain_name]
    uniprot_acs = list(set(humanppi_ifres["uniprot"]))

    if not os.path.isfile('/fsimb/groups/imb-luckgr/projects/interface_clustering/datasets/cluster_analysis/bfmdvspdb/humanppi_disorder_fractions.tsv'):
        with open("/fsimb/groups/imb-luckgr/projects/interface_clustering/datasets/cluster_analysis/bfmdvspdb/humanppi_disorder_fractions.tsv", 'a+') as f:
            f.write("chain_id\tcomplex_id\tuniprot_id\tdisfrac\n")
        acs_already_processed = []
    else:
        disorder_fractions = pd.read_csv('/fsimb/groups/imb-luckgr/projects/interface_clustering/datasets/cluster_analysis/bfmdvspdb/humanppi_disorder_fractions.tsv', sep="\t")
        acs_already_processed = list(set([str(x) for x in disorder_fractions["uniprot_id"]]))

    for ac in uniprot_acs:
        if (str(ac) not in acs_already_processed) & (str(ac) != "id not found") & (str(ac) != "chimeric"):
            curr_df = humanppi_ifres[humanppi_ifres["uniprot"] == ac]
            url = 'http://iupred2a.elte.hu/iupred2a/short/'+str(ac).lower()+'.json'
            response = requests.get(url)
            if 'iupred2' in response.text:
                try:
                    resjson = response.json()
                except:
                    print(response.text)
                iupred = pd.Series(resjson['iupred2'])
                if len(iupred.index) > 0:
                    iupred.index = iupred.index + 1
                    curr_df["disfrac"] = curr_df.apply(lambda x: get_disorder_frac(x, iupred), axis=1)
                    
                with open("/fsimb/groups/imb-luckgr/projects/interface_clustering/datasets/cluster_analysis/bfmdvspdb/humanppi_disorder_fractions.tsv", 'a') as f:
                    for i,r in curr_df.iterrows():
                        line_to_write = "\t".join([str(r["chain_id"]),str(r["complex_id"]),str(r["uniprot"]),str(r["disfrac"])])
                        f.write(line_to_write)
                        f.write("\n")

if __name__ == "__main__":
    main()