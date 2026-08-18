#!/usr/bin/env python3

"""
Summarize DSSP secondary structure composition for CATH domains.

This script maps CATH domain boundaries onto DSSP secondary structure
assignments and calculates the number and percentage of residues in each
secondary structure class for every CATH domain.

Input
-----
1. cath_domain_boundary_label_asym_seq_ids.tsv
   Tab-separated file containing at least the following columns:
       Domain          CATH domain identifier (e.g. 1abcA00)
       Label_asym_id   Chain identifier matching DSSP label_asym_id
       Boundary        Domain boundaries in label_seq_id numbering
                       (e.g. 15-78 or 15-78,120-156)

2. DSSP mmCIF files
   One gzipped mmCIF file per PDB entry located under DSSP_DIR using
   the directory structure:
       <DSSP_DIR>/<pdb[1:3]>/<pdb>.cif.gz

Output
------
domain_ss_summary_3.csv
    One row per CATH domain containing:
        - residue counts for each DSSP secondary structure code
        - percentages of each secondary structure code
        - number of unassigned (NA) residues

missing_cif_files_3.txt
    List of DSSP files that could not be found.

Dependencies
------------
Python >=3.10
pandas
gemmi
tqdm
"""

from pathlib import Path
from collections import defaultdict, Counter
import pandas as pd
import gemmi
from tqdm import tqdm



#----------- Configuration ---------------#

CATH_FILE = Path("cath_domain_boundary_label_asym_seq_ids.tsv")
DSSP_DIR = Path("/fsimb/groups/imb-luckgr/imb-luckgr2/projects/interface_clustering/dssp_download_20251030/cif")
OUTPUT = Path("domain_dssp_ss_summary.csv")

MISSING_OUTPUT = Path("missing_cif_files_3.txt")
missing_cifs = []

# DSSP secondary structure codes
SS_CODES = ["H", "B", "E", "G", "I", "P", "T", "S"]
ALL_CODES = SS_CODES + ["NA"]


def load_domains(cath_file):

    """
    Read the CATH domain table and group domains by PDB entry.

    Returns
    -------
    dict
        {pdb_id: [(domain_id, chain, residue_set, domain_length), ...]}
    """

    domains = defaultdict(list)

    df = pd.read_csv(cath_file, sep="\t")

    # extract domain id, boundary, pdb id, chain
    for _, row in df.iterrows():
        domain_id = row["Domain"]
        chain = row["Label_asym_id"]
        boundary = row["Boundary"]
        pdb = domain_id[:4]
        residue_set = set()

        # Map domain boundary to start-end integers (compatible with discontinuous domains)
        for segment in boundary.split(","):
            start, end = map(int, segment.split("-"))
            residue_set.update(range(start, end + 1))

        domains[pdb].append((domain_id, chain, residue_set, len(residue_set),))

    return domains



def read_dssp(cif_file, required_chains):

    """
    Extract DSSP secondary structure assignments for selected chains.

    Only residues from the requested chains are parsed to reduce memory use.
    Unknown or missing DSSP codes are assigned as 'NA'.
    """

    # Read the DSSP summary table from the mmCIF file.
    block = gemmi.cif.read_file(str(cif_file)).sole_block()
    table = block.find(
        "_dssp_struct_summary.",
        [
            "label_asym_id",
            "label_seq_id",
            "secondary_structure",
        ],
    )

    residues = defaultdict(list)

    for row in table:
        chain = row[0]

        if chain not in required_chains:
            continue

        try:
            resnum = int(row[1])

        except ValueError:
            continue

        ss = row[2]
        if ss not in SS_CODES:
            ss = "NA"

        residues[chain].append((resnum, ss))

    return residues



def process_pdb(pdb, domains):

    """
    Calculate residue counts and percentages of DSSP secondary structure
    classes for every domain in a single PDB entry.
    """

    cif = (DSSP_DIR/ pdb[1:3] / f"{pdb}.cif.gz")

    if not cif.exists():
        missing_cifs.append(str(cif))
        return []

    required_chains = {chain for _, chain, _, _ in domains}
    residues = read_dssp(cif, required_chains)

    rows = []
    for domain_id, chain, residue_set, total in domains:

        counter = Counter()

        # Match DSSP label_seq_id residues to the CATH domain boundaries
        for resnum, ss in residues.get(chain, ()):
            if resnum in residue_set:
                counter[ss] += 1

        # Residues within the CATH domain that are absent from DSSP are
        # counted as unassigned (NA).
        counter["NA"] += (total - sum(counter.values()))

        row = {"Domain": domain_id, "Total": total, }

        for ss in ALL_CODES:
            row[ss] = counter[ss]

        for ss in ALL_CODES:
            row[f"{ss}%"] = (round(counter[ss] * 100 / total, 2) if total > 0 else 0.0)

        rows.append(row)

    return rows



def main():

    domains = load_domains(CATH_FILE)

    results = []

    for pdb, domain_list in tqdm(domains.items(), total=len(domains)):
        results.extend(process_pdb(pdb, domain_list))

    df = pd.DataFrame(results)
    df.to_csv(OUTPUT, index=False)
    print(df.head())

    if missing_cifs:
        with open(MISSING_OUTPUT, "w") as f:
            for item in sorted(set(missing_cifs)):
                f.write(item + "\n")

        print(f"Missing CIFs: {len(set(missing_cifs))}")

    print(f"\nSaved {len(df):,} domains to {OUTPUT}")


if __name__ == "__main__":
    main()