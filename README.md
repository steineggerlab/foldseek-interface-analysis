# Foldseek-Interface — analysis code

Analysis code for **"Foldseek-Interface reveals a protein interface universe far from complete"**


Foldseek-Interface converts 3D interface structures into searchable 3Di sequences,
enabling fast alignment and clustering of protein interaction interfaces. It matches
the accuracy of iAlign while running up to **230× faster**. Applied to all biological
assemblies in the PDB, it clusters **3,121,961 dimers into 77,167 interface clusters**
(via 189,830 non-redundant dimer representatives) — the first comprehensive resource of
experimentally determined protein interfaces clustered by interface structure. The full
workflow took roughly six days: 21 h on two L40S GPUs plus 120 h on a single 128-core node.

This repository holds **only the scripts and notebooks that produced the results and
figures of the paper**. The method itself is implemented in Foldseek.

## Resources

| | |
|---|---|
| Preprint | TODO |
| Interface search server | https://search.foldseek.com/interface |
| Interface cluster explorer | https://interface.foldseek.com |
| Cluster resource download | Zenodo [10.5281/zenodo.22040892](https://doi.org/10.5281/zenodo.22040892) |
| Foldseek (method source) | https://github.com/steineggerlab/foldseek |

## Repository layout

| Directory | Contents |
|---|---|
| `scripts/` | Shell/SLURM drivers for all Foldseek, iAlign and MMseqs2 runs — database construction, benchmarks, PDB and HumanPPI clustering, NMR control, taxonomy assignment |
| `benchmarking/` | Benchmark dataset construction, accuracy evaluation, Figure 1 / S1, Tables S1–S6 |
| `annotations/` | Retrieval of external annotations for the PDB interfaces and assembly of the annotated cluster tables |
| `analysis/` | Downstream analyses, Figures 2–4 / S2–S4, Tables S7–S13 |

## Pipeline

### 1. Benchmarking (`benchmarking/`, `scripts/`)

Because no geometry-based reference clustering of interfaces exists, two
sequence-derived ground-truth sets were built:

- **Order–order (DDI)** — ProtCID clusters for a manually curated set of 43 Pfam
  binding pairs with high-confidence domain–domain interface structures; 30 pairs had
  ProtCID clusters, giving **41 clusters / 654 interfaces**. ProtCID data dump of
  2024-02-01. Built in `benchmarking/create_ord-ord_benchmark_dataset.ipynb`.
- **Disorder–order (DMI)** — SLiM classes from a MoMaP data dump (2024-06-05)
  restricted to classes mapped to ELM, sampled evenly across the 2nd/3rd/4th quartiles
  of cluster size; **58 clusters / 778 interfaces**, with ELM class as ground truth.
  Built in `benchmarking/create_dis-ord_benchmark_dataset.ipynb`.

| Script | Purpose |
|---|---|
| `scripts/slurm_foldseek_ord-ord.sh`, `slurm_foldseek_dis-ord.sh` | All-by-all Foldseek-Interface alignment on DDI / DMI |
| `scripts/slurm_ialign-is_*.sh`, `slurm_ialign-tm_*.sh` | iAlign baselines, IS-score and TM-score normalisation |
| `scripts/slurm_foldseek_*_single-chain-thresh.sh` | Sweeps of `--lddt-threshold` and `--tmscore-threshold` (0.1–0.9) |
| `scripts/slurm_foldseek_*_pdb-aln_filter-modes.sh` | Prefilter modes (default k-mer, ungapped, exhaustive + LDDT) at PDB scale |
| `scripts/slurm_foldseek_createdb_pdb-plus-bm.sh` | Combined PDB + benchmark interface database for the scaling tests |
| `scripts/slurm_foldseek_*_cluster_dimer-int.sh` | Clustering benchmark: dimer clustering, then interface clustering of representatives at interface TM 0.3 / 0.4 / 0.5 |

Evaluation code: `benchmarking/results_processing.py` (report parsing, ROC/AUC,
heatmaps), `benchmarking/pdb_file_processing.py` (structure handling, two-chain
extraction), `benchmarking/process_cluster_benchmark.ipynb` (Adjusted Rand Score
against the ground-truth clusterings).

Headline result: 0.966 vs. 0.949 (order–order) and 0.789 vs. 0.809 (disorder–order)
for Foldseek-Interface vs. iAlign. An interface TM-score cut-off of **0.3** is optimal
on the benchmarks; **0.4** was chosen for the full PDB (Fig. S2a).

### 2. Clustering the PDB (`scripts/cluster_pdb.sh`)

PDBe biological assembly files downloaded 2025-03-13. Two-stage procedure:

1. `foldseek createdimerdb` (default parameters) → 3,121,961 dimers, then
   `foldseek multimercluster` with
   `--multimer-tm-threshold 0.9 --chain-tm-threshold 0.5 --interface-lddt-threshold 0 -c 0 --cov-mode 0 --cluster-mode 0`
   → 189,830 non-redundant dimer clusters. Strict thresholds avoid merging distinct interfaces.
2. `foldseek createinterfacedb` on the dimer representatives, then `multimercluster` with
   `--multimer-tm-threshold 0.4 --chain-tm-threshold 0 --interface-lddt-threshold 0 -c 0 --cov-mode 0 --cluster-mode 0 --exhaustive-search 1 -e 10000000 --lddt-threshold 0.2 --max-iteration 1`
   → **77,167 interface clusters**. All members of each dimer cluster inherit the
   interface cluster of their representative.

The final step was re-run at thresholds 0.3 / 0.4 / 0.5 and scored by Adjusted Rand
Score against the benchmark ground truth to confirm the choice of 0.4.

Supporting scripts:

- `annotations/collate_cluster_results.py` — joins dimer-level and interface-level
  assignments into one table covering all 3.12 M interfaces.
- `scripts/lca.sh` — taxonomic last common ancestor per cluster via `mmseqs lca` followed by Metabuli-App.
- `scripts/nmr_clustering.sh` — NMR control. 1,805 NMR entries in the dimer database
  yielded 5,135 dimers, 3,950 of them with multiple models; each entry's models are
  re-clustered with the PDB parameters. 83.79 % of NMR entries yield a single interface
  cluster (most fragmented: 25 clusters).

### 3. Annotation (`annotations/`)

| Script | Annotation | Source |
|---|---|---|
| `residue_mapping.py` | UniProt IDs and PDB→UniProt residue index conversion for interface residues | SIFTS |
| `get_disorder.py` | Fraction of disordered interface residues (IUPred2A short, score > 0.4) | IUPred2A |
| `get_dssp.py` | Secondary structure fractions of interface residues | PDB-REDO / DSSP 4 |
| `get_pfam.py` | Pfam domains and boundaries | PDBe API |
| `get_coiledcoils.py` | Coiled-coil regions | UniProt |
| `get_gene_name_mapping.py` | Gene names per PDB chain | PDBe API |
| `get_pdbcharacteristics.py` | Entry metadata, incl. deposition/release dates | RCSB GraphQL |

`add_annot_to_clusters.ipynb` merges all of the above (plus CATH, antibody and GO
annotations) into the annotated interface table; `create_cluster_summary.ipynb`
aggregates it into per-cluster summary statistics.

### 4. Downstream analysis (`analysis/`)

- **Secondary structure** — `cath_interface_secondary_structure_analysis.ipynb` with
  `get_domain_dssp_secondary_structure.py`: maps CATH domain boundaries onto DSSP
  assignments, aggregates by CATH homologous superfamily, and compares ordered
  interfaces, disorder-mediated interfaces and whole folds. Mixed ANOVA, secondary
  structure × group interaction F = 263.96, P < 0.001; Holm-corrected post hoc tests.
- **Structural / functional diversity** — `figure3_S3.ipynb`: of 13,725 clusters with
  more than one CATH-annotated interface, 721 (5 %) contain more than one unique CATH
  domain pair; ~60 % of those span different CATH classes.
- **Pathogen mimicry** — `notebook_pathogen_mimicry.ipynb`: clusters containing both
  human–human (HH) and human–pathogen interfaces, after removing antibody/immune
  interactions and *E. coli*. Yields 56 candidate mimicry clusters (9 HH/HB, 46 HH/HV,
  1 with all three). Fisher exact tests with BH correction.
- **HumanPPI** — `scripts/cluster_and_search_humanppi.sh` with `humanppi_vs_pdb.ipynb`:
  21,048 predicted binary human complexes from the HumanPPI database
  (http://prodata.swmed.edu/humanPPI/, accessed 2024-09-29; RoseTTAFold2 + AlphaFold2),
  filtered to 20,299 interfaces with at least one chain contributing > 12 interface
  residues, clustered with the PDB parameters and searched against the PDB interface
  cluster representatives (`multimersearch`, default parameters; hit if qTM or tTM ≥ 0.4).
  Of 10,040 clusters, 1,780 have no PDB hit for any member and are called putatively
  novel (97 % singletons).
- **GO enrichment** — `enrichGO_humanppi_nohit.R`: clusterProfiler on the UniProt IDs
  of the novel HumanPPI clusters.
- **AlphaFold-Multimer** — `af_new_if-types.ipynb`: clusters labelled pre-/post-training
  against the AF-MM v2.3 cut-off (2021-09-30), stratified by orderedness, excluding
  peptide–peptide and very small interfaces (max interface chain length < 13 residues);
  479 sampled cluster representatives predicted with ColabFold v1.5.5 (20 recycles,
  MSAs from MMseqs2 commit 6f45232 against uniref30_2302 and colabfold_envdb_202108 at
  sensitivity 7) and scored by DockQ.
- **Visualisation** — `get_two_chains.py` extracts the two interacting chains of a
  cluster representative; `color_if_res.py` renders a standardised interface view in
  ChimeraX (`open color_if_res.py`, then `color_if_res model #1 chain1 A chain2 B color_mode dark`).

## Figures and supplemental tables

| Output | Location |
|---|---|
| Figure 1 | `benchmarking/figure1.ipynb` |
| Figure S1 · Tables S1–S6 | `benchmarking/figureS1.ipynb` |
| Figure 2 · Table S7 | `analysis/figure2.ipynb`; panel 2d from `analysis/cath_interface_secondary_structure_analysis.ipynb`, panel 2c from `scripts/nmr_clustering.sh` |
| Figure S2 · Table S8 | `analysis/figureS2.ipynb`,  NMR clustering input from `scripts/nmr_clustering.sh` |
| Table S9 | `analysis/cath_interface_secondary_structure_analysis.ipynb` |
| Figure 3 · S3 · Table S10 | `analysis/figure3_S3.ipynb` |
| Figure 3h–l · Table S11 | `analysis/notebook_pathogen_mimicry.ipynb` |
| Figure 4 · S4 · Tables S12, S13 | `analysis/figure4_S4.ipynb`; panel 4d via `analysis/enrichGO_humanppi_nohit.R`, AF-MM benchmark in `analysis/af_new_if-types.ipynb`, HumanPPI processing in `analysis/humanppi_vs_pdb.ipynb` |


## Requirements

- **Foldseek** with interface support — `createdimerdb`, `createinterfacedb`,
  `multimercluster`, `multimersearch`, `easy-multimersearch`, `easy-multimercluster`
- **MMseqs2** — `scripts/lca.sh`
- **iAlign** (Perl) — benchmark baseline
- **ColabFold v1.5.5** — AlphaFold-Multimer predictions
- **Python 3** — numpy, pandas, scipy, scikit-learn, statsmodels, matplotlib, seaborn,
  biopython (v1.86), gemmi, requests, tqdm
- **R** — clusterProfiler, ggplot2, org.Hs.eg.db, org.Bt.eg.db
