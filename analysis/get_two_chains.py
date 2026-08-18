## Script to extract the two interacting chains of every dimer cluster representative from the PDB biological assemblies for visualization in ChimeraX

import numpy as np
import pandas as pd
from Bio import PDB
import gzip, os

def get_two_chains(structure, chains, save_name):
    io = PDB.mmcifio.MMCIFIO()
    chains = chains.split("_")
    io.set_structure(structure)
    class ChainSelect(PDB.Select):
        # Obtain only the target chains (those participating in the interface)
        def accept_chain(self, chain):
            if chain.get_id()==chains[0] or chain.get_id()==chains[1]:
                return True
            else:
                return False
    io.save(f"/fsimb/groups/imb-luckgr/imb-luckgr2/projects/interface_clustering/two-chain_dimerreps/{str(save_name)}.cif", ChainSelect())

def main():
    
    pdb_clusters = pd.read_csv("/fsimb/groups/imb-luckgr/projects/interface_clustering/results/cluster_analysis/pdb_clusters_annotated.tsv", sep="\t")
    pdb_clusters["chain_id_0"] = pdb_clusters["chain_id_0"].fillna('NA')
    pdb_clusters["chain_id_1"] = pdb_clusters["chain_id_1"].fillna('NA')

    pdb_clusters = pdb_clusters[pdb_clusters["dimerrep"] == 1]
    print(pdb_clusters.shape[0])

    pdb_clusters['chains'] = pdb_clusters[['chain_id_0','chain_id_1']].apply(lambda x: '_'.join(sorted([str(y) for y in x])), axis=1)
    pdb_clusters['report_lookup_id'] = pdb_clusters[['old_complex_id', 'pdb_id']].apply(lambda x: "DI"+str(x.iloc[0])+"_"+str(x.iloc[1]), axis=1)

    assemblies = list(set(pdb_clusters.pdb_id))
    assemblies_processed = [x.split("_")[-1].strip(".cif") for x in os.listdir("/fsimb/groups/imb-luckgr/imb-luckgr2/projects/interface_clustering/two-chain_dimerreps")]

    parser = PDB.MMCIFParser(QUIET=True)
    for assembly in assemblies:
        if assembly not in assemblies_processed:
            two_letters = assembly[1:3]
            with gzip.open(f"/fsimb/groups/imb-luckgr/imb-luckgr2/projects/interface_clustering/pdb-assemblies_download_20250313/divided/{two_letters}/{assembly}.cif.gz", 'rt') as file:
                try:
                    structure = parser.get_structure(assembly, file)
                except:
                    print(assembly)
                    continue
            assembly_df = pdb_clusters[pdb_clusters['pdb_id'] == assembly]
            for i,r in assembly_df.iterrows():
                get_two_chains(structure, r['chains'], r['report_lookup_id'])

if __name__ == "__main__":
    main()