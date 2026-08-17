## Functions related to processing Foldseek-Interface and Foldseek-Interface-Cluster results files to determine benchmark accuracy
import numpy as np
import pandas as pd
import os, re
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import metrics

def format_foldseek_results(filepath, version='new'):
    """
    Recieve as input a filepath to a Foldseek alignment report and output a pandas DataFrame with proper formatting for following functions.

    Input:
        filepath|str: Path to alignment report file
        version|str: Possible values are 'new' and 'old'. An older version of Foldseek, used to create the CB-derived interfaces, had a different naming convention in the output report. The PDB filenames in that version are the first position in the query and target names. In the later version, the PDB filenames are in the last position of the query and target names. Changing the value of this parameter will change how the report file is processed to extract the original PDB filenames.
    """
    df = pd.read_csv(filepath, sep='\t', header=None)
    df.columns = ['query','target','qchain','tchain','qscore','tscore','u','t','complexid']
    if version=='new':
        df['query'] = [x.split('_')[-1] for x in df['query']]
        df['target'] = [x.split('_')[-1] for x in df['target']]
    elif version=='old':
        df['query'] = [x.split('_')[0] for x in df['query']]
        df['target'] = [x.split('_')[0] for x in df['target']]     
    return df

def format_ialign_results(filepath):
    query = []
    target = []
    score = []
    with open(filepath,'r') as f:
        contents = f.readlines()
        for i in range(len(contents)):
            if re.match(">>>", contents[i]):
                line = contents[i].split(" ")
                if len(line) > 2:
                    query.append(line[1][:-2])
                    target.append(line[3][:-3])
                    score.append(line[6])
    df = pd.DataFrame({'query':query, 'target':target, 'score':[float(x) for x in score]})
    return df

def results_to_pairwise(df, score, structures, cluster_assignments):
    """ 
    Receive output from alignment tool in all-by-all structure comparison and reformat into a long-form dataframe where every possible pairwise comparison is represented (order-independent) within the structure dataset. Add alignment scores to each of these pairs where available from alignment results, where not, replace missing values with 1 in the case of self-comparison and 0 in all other cases. Result can be coerced into a symmetric matrix.
    
    Expected input: df|pandas.DataFrame = Dataframe containing all available alignment results, where one column is labeled 'query' and another 'target'
                    score|list[str] = List of variable names containing alignment scores (this is usually either one variable or two depending on the tool and output format)
                    structures|list[str] = List of all desired structure names among which to make pairwise comparisons
    """
    
    names = list(set(df['query']) | set(df['target']))
    frac_aligned = round(len(names)/len(structures)*100, 2)

    df['avg'] = df[score].apply(lambda r: r.mean(), axis=1)
    df['comb_id'] = df[['query','target']].apply(lambda r: '-'.join(sorted(r)), axis=1)
    df.sort_values(by='avg', ascending=False, inplace=True) #Sort by average score and drop everything but the best average alignment for a pair
    df.drop_duplicates(subset=['comb_id'], keep='first', inplace=True, ignore_index=True)
    # Start new dataframe with all possible permutations of names
    if1 = []
    if2 = []
    for i in structures:
        for j in structures:
            if1.append(i)
            if2.append(j)
    template = pd.DataFrame({'if1':if1,'if2':if2})
    template['comb_id'] = template.apply(lambda r: '-'.join(sorted(r)), axis=1)
    # Merge alignment score into new dataframe
    results = pd.merge(template, df[['comb_id','avg']], on='comb_id', how='left').drop('comb_id', axis=1)
    results.loc[results['if1'] == results['if2'], 'avg'] = 1 #Alignment with itself is perfect score
    results['avg'] = results['avg'].fillna(0) #Anything with no alignment available has score 0

    # Label observations with provided cluster assignment mappings
    results['cluster1'] = results['if1'].map(cluster_assignments)
    results['cluster2'] = results['if2'].map(cluster_assignments)
    # Create agreement lable to distinguish 'similar' from 'dissimilar' interfaces based on cluster assignment
    results.loc[results['cluster1'] == results['cluster2'], 'agreement'] = 1
    results['agreement'] = results['agreement'].fillna(0)

    return results, frac_aligned

def roc1(x):
    n = x.index.get_loc(x.index[x['agreement'] == 0][0])
    if n == 0:
        return 0
    elif n > 0:
        return sum(x['agreement'][0:n])/sum(x['agreement'])

def roc1_auc_score(df, query_id, roc1_score):
    """
    Calculate the area under a ROC1 curve.
    
    Input:
        label|pandas.Series: A binary positive/negative label. Expecting values of 0 and 1
        score|pandas.Series: The score to be used to rank observations
    """
    sorted_df = df.sort_values(by=roc1_score, ascending=False)
    fracs = sorted_df.groupby(query_id).apply(roc1, include_groups=False)
    roc1_scores = []
    thresh = np.linspace(0.0, 1.0, 30)
    for n in thresh:
        roc1_scores.append(sum(fracs >= n)/len(fracs))
    return round(metrics.auc(thresh, roc1_scores), 3)

def calculate_auc(results, structures):
    """
    Calculate and output accuracy metrics for an input dataframe containing alignment scores from an all-vs-all alignment of a given dataset.
    
    Input:
        df|pandas.DataFrame: Dataframe where each observation contains the alignment score(s) and any other info found for a given query and target structure pair. Expecting the query structure identifier column to be labeled 'query' and the target structure identifier column to be labeled 'target'
        score|list[str]: List of strings, where each string is the name of a column in df containing the alignment score. The purpose of the list is to be able to compute an average score for cases where alignment scores are normalized on query and target structures separately
        structures|list[str]: List of strings, where each string is the identifier of one of the structures in the dataset
        cluster_assignments|dict: Dictionary containing mappings of structure identifiers to cluster assignments
    """

    # Calculate AUROC and AUROC1
    auc = round(metrics.roc_auc_score(results['agreement'], results['avg']), 3)
    auroc = roc1_auc_score(results, 'if1', 'avg')

    return auc, auroc

def create_heatmap(results, id_order, filepath=None, save=True):

    """ Receive dataframe with full pairwise alignment scores, coerce into symmetrical distance matrix and perform clustering with optional heatmap image output.
    
    Input: 
        results|DataFrame: Dataframe containing all available alignment results, where one column is labeled 'query' and another 'target'
        num_clust|int = List of variable names containing alignment scores (this is usually either one variable or two depending on the tool and output format)
        filepath|str = Filepath to save heatmap image (if desired), including desired filename but WITHOUT file extension
        save|Bool = Whether to save output dataframe """

    # Create symmetrical distance matrix, flatten, then generate linkage
    alignments = results.pivot_table(index='if1',columns='if2',values='avg')
    alignments = alignments.reindex(id_order)
    alignments = alignments.reindex(columns=id_order)

    # Final visualization with heatmap and dendrogram with output clusters labeled in color bars on left-hand side
    fig, ax = plt.subplots(figsize=(3,3))
    sns.heatmap(alignments, vmin=0.00, vmax=1.00, yticklabels=False, xticklabels=False, ax=ax, square=True, cmap="magma_r", cbar=False)
    ax.set_xlabel(None)
    ax.set_ylabel(None)

    fig = ax.figure
    if save:
        fig.savefig(f'{filepath}.pdf',
                    transparent=True,bbox_inches='tight')
        fig.savefig(f'{filepath}.jpeg',dpi=300,
                    transparent=True,bbox_inches='tight')
        
def process_cluster_tsv(filepath, dimer=True):
    clust_tsv = pd.read_csv(filepath, sep="\t", header=None)
    clust_tsv.columns = ["representative", "member"]
    if dimer:
        clust_tsv["representative"] = [x.split("_")[-1] for x in clust_tsv["representative"]]
        clust_tsv["member"] = [x.split("_")[-1] for x in clust_tsv["member"]]
    return clust_tsv

def process_cluster_report(filepath, dimer=True):
    f = open(filepath, "rb")
    data = []
    for line in f.readlines():
        linedata = line.decode('utf-8').replace('\x00', '').strip()
        linedata = linedata.split("\t")
        linedata_dict = {'query' : linedata[0],
                         'target' : linedata[1],
                         'qcov' : float(linedata[2]),
                         'tcov' : float(linedata[3]),
                         'qscore' : float(linedata[4]),
                         'tscore' : float(linedata[5]),
                         'iLDDT' : float(linedata[6]),
                         'u' : linedata[7],
                         't' : linedata[8]}
        data.append(linedata_dict)
    results = pd.DataFrame(data)
    if dimer:
        results['query'] = [x.split("_")[-1] for x in results["query"]]
        results['target'] = [x.split("_")[-1] for x in results["target"]]
    return results

def assign_nested_clusters(tsv1, tsv2, clust_var):
    tsv1["parent_clust"] = tsv1["representative"].map(dict(zip(tsv2.member, tsv2[clust_var])))
    return tsv1