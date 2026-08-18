## Script to fetch PDB metatdata from RCSB GraphQL server based on PDB ID.

import numpy as np
import pandas as pd
import requests

def main():

    # From collate_cluster_results.py
    pdb_clusters = pd.read_csv("/fsimb/groups/imb-luckgr/projects/interface_clustering/results/cluster_analysis/pdb_clusters.tsv", sep="\t")
    pdb_ids_to_fetch = list(set([x[0:4] for x  in pdb_clusters["pdb_id"]]))
    print("# PDB IDs to access: ", len(pdb_ids_to_fetch))

    url = "https://data.rcsb.org/graphql"

    body_pt1 = """
            query structure{
                entry(entry_id:""" + '"'
    body_pt2 = '"' + """){
                struct{
                    title
                }
                struct_keywords{
                    pdbx_keywords
                }
                exptl{
                    method
                }
                refine{
                    pdbx_refine_id
                    ls_d_res_high
                }
                em_3d_reconstruction{
                    resolution
                }
            }
        }
    """

    keywords = []
    titles = []
    expts = []
    reses = []

    for i in range(0, len(pdb_ids_to_fetch)):
        body = body_pt1 + pdb_ids_to_fetch[i] + body_pt2
        try:
            response = requests.post(url=url, json={"query":body})
            response_dict = response.json()
            curr_keyword = response_dict['data']['entry']['struct_keywords']['pdbx_keywords']
            curr_title = response_dict['data']['entry']['struct']['title']
            curr_expt = response_dict['data']['entry']['exptl'][0]['method']
            if curr_expt == "X-RAY DIFFRACTION":
                curr_res = response_dict['data']['entry']['refine'][0]['ls_d_res_high']
            elif curr_expt == "ELECTRON MICROSCOPY":
                curr_res = response_dict['data']['entry']['em_3d_reconstruction'][0]['resolution']
            else:
                curr_res = None
        except:
            curr_keyword = 'None'
            curr_title = 'None'
            curr_expt = 'None'
            curr_res = 'None'
        keywords.append(curr_keyword)
        titles.append(curr_title)
        expts.append(curr_expt)
        reses.append(curr_res)

    pdb_keywords = pd.DataFrame({"pdb_id":pdb_ids_to_fetch, "keyword":keywords, "expt_method":expts, "resolution":reses, "title":titles})
    pdb_keywords.to_csv("/fsimb/groups/imb-luckgr/projects/interface_clustering/datasets/cluster_analysis/mapping/pdb_characteristics.tsv", sep="\t", index=None)

if __name__ == "__main__":
    main()