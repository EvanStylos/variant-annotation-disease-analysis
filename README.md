# variant-annotation-disease-analysis
Bioinformatics workflow for prioritizing variant-associated genes, integrating disease annotations, and performing disease enrichment and text-based analysis.
## Overview

This project presents a bioinformatics workflow for analyzing annotated genomic variants and exploring their potential disease associations.

The workflow integrates variant-level information, gene prioritization, disease annotation, and enrichment analysis to identify biological patterns associated with genes containing genomic variants.

## Workflow Overview

The analysis consists of the following steps:

### 1. Variant-based Gene Prioritization

Annotated variant data were analyzed to:

- Extract gene identifiers from variant annotation files
- Count the number of variants per gene
- Identify the top 30 genes with the highest number of detected variants
- Compare gene overlap between different variant impact categories

Variant impact categories analyzed:

- High
- Moderate
- Low
- Modifier


### 2. Gene Overlap Analysis

The overlap between prioritized genes from different impact categories was visualized using Venn diagrams to identify:

- Shared genes between impact groups
- Category-specific genes
- Common high-priority genes


### 3. Disease Annotation Integration

Genes were linked with disease information using:

- ClinVar annotations
- MalaCards disease associations

Disease information was manually curated and categorized into broader disease groups to facilitate downstream analysis.


### 4. Disease Term Frequency Analysis

Text-based analysis was performed on disease descriptions to identify:

- Frequently occurring disease-related terms
- Multi-word disease patterns
- Number of unique genes associated with each term

The analysis included:

- Word frequency analysis
- Bigram and trigram extraction
- Removal of common non-informative terms (stopwords)


### 5. Disease Gene Set Analysis

Overrepresentation analysis results were visualized using bubble plots to highlight:

- Disease categories associated with prioritized genes
- Enrichment scores
- Number of matched genes
- Gene–disease associations

## Tools & Technologies

Programming:
- Python

Libraries:
- Pandas
- NumPy
- Matplotlib
- Seaborn
- matplotlib-venn

Bioinformatics resources:
- ClinVar
- MalaCards

Analysis approaches:
- Variant prioritization
- Disease enrichment analysis
- Text mining
- Data visualization

## Repository Structure
variant-annotation-disease-analysis/

│
├── README.md
│
├── scripts/
│   ├── 01_top_variant_genes.py
│   ├── 02_gene_overlap_analysis.py
│   ├── 03_disease_term_frequency.py
│   ├── 04_disease_phrase_analysis.py
│   └── 05_disease_gene_set_bubbleplot.py
│
├── notebooks/
│   └── exploratory_analysis.ipynb
│
├── results/
│   ├── figures/
│   │   ├── top30_genes_high.png
│   │   ├── top30_genes_moderate.png
│   │   ├── top30_genes_low.png
│   │   ├── venn_top_genes.png
│   │   └── disease_gene_bubbleplot.png
│   │
│   └── tables/
│       ├── Top30_variant_genes.xlsx
│       ├── Top10_Word_Terms_by_Category.xlsx
│       └── Top_Disease_Terms_by_Category.xlsx
│
├── requirements.txt
│
└── LICENSE

scripts/
Variant processing and visualization scripts

results/
Generated figures and analysis outputs

notebooks/
Exploratory analysis notebooks

## Results

The workflow generates:

- Ranked lists of genes according to variant frequency
- Gene overlap visualizations
- Disease term frequency tables
- Disease enrichment visualizations

## Data Availability

Raw genomic datasets are not included due to privacy and data protection considerations.

The repository contains analysis scripts and example outputs demonstrating the workflow.

---

## Author
Evangelos Stylos
