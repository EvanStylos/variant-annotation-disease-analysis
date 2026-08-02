# Variant Annotation & Disease Analysis

Bioinformatics workflow for prioritizing variant-associated genes, integrating gene–disease annotations, and exploring disease-related patterns through text analysis and disease gene-set analysis.

## Overview

This project presents a bioinformatics workflow for analyzing annotated genomic variants and investigating potential disease associations.

The workflow combines gene-level variant prioritization, comparison of variant impact categories, disease annotation and categorization, text-based disease analysis, and disease gene-set visualization.

## Workflow

### 1. Variant-Based Gene Prioritization

Annotated variant data were analyzed to identify genes with the highest number of detected variants.

For each variant impact category, the workflow:

* Extracts gene identifiers from annotated variant data
* Counts the number of variants associated with each gene
* Identifies the top 30 genes
* Generates visualizations of the prioritized genes

The following impact categories were analyzed:

* High
* Moderate
* Low
* Modifier

### 2. Gene Overlap Analysis

The top 30 genes from the High, Moderate, and Low impact categories were compared to investigate their overlap.

A three-set Venn diagram was used to identify:

* Genes unique to each impact category
* Genes shared between two categories
* Genes common to all three categories

### 3. Disease Annotation and Categorization

Disease associations were investigated using gene–disease information from ClinVar and MalaCards.

Disease information retrieved from MalaCards was manually curated and organized into broader disease categories for downstream analysis.

Manual curation was used because the available MalaCards API access was insufficient for the number of required queries.

### 4. Disease Term and Phrase Analysis

Disease descriptions were analyzed using text-processing approaches to identify recurring disease-related patterns.

Two complementary analyses were performed:

**Term frequency analysis**

* Identification of frequently occurring disease-related terms
* Calculation of term frequency
* Number of unique genes associated with each term
* Removal of common non-informative terms

**Phrase analysis**

* Extraction of two-word phrases (bigrams)
* Extraction of three-word phrases (trigrams)
* Identification of recurring multi-word disease patterns
* Association of terms with variant impact and disease categories

### 5. Disease Gene-Set Analysis

Overrepresentation analysis was performed using prioritized genes from the High-impact category.

The resulting disease associations were visualized using a bubble plot based on:

* Disease
* Analysis score
* Number of matched genes
* Gene–disease evidence

## Tools & Technologies

### Programming

* Python

### Libraries

* Pandas
* NumPy
* Matplotlib
* Seaborn
* matplotlib-venn

### Bioinformatics Resources

* ClinVar
* MalaCards

### Analysis Approaches

* Variant prioritization
* Gene-level variant counting
* Gene overlap analysis
* Disease annotation
* Manual disease categorization
* Text mining
* Bigram and trigram analysis
* Overrepresentation analysis
* Data visualization

## Repository Structure

```text
variant-annotation-disease-analysis/
│
├── README.md
├── LICENSE
├── requirements.txt
│
├── data/
│   └── README.md
│
├── scripts/
│   ├── 01_top_variant_genes.py
│   ├── 02_gene_overlap_analysis.py
│   ├── 03_disease_term_frequency.py
│   ├── 04_disease_phrase_analysis.py
│   └── 05_disease_gene_set_bubbleplot.py
│
└── results/
    └── figures/
        ├── top30_genes_high.png
        ├── top30_genes_moderate.png
        ├── top30_genes_low.png
        ├── venn_top_genes.png
        └── disease_gene_bubbleplot.png
```

### `scripts/`

Contains the Python scripts implementing the main analysis steps, from variant-based gene prioritization to disease gene-set visualization.

### `data/`

Contains documentation describing the input data. Raw genomic and annotation datasets are not included in the repository.

### `results/figures/`

Contains selected visual outputs generated during the analysis.

## Results

The workflow produces:

* Ranked lists of genes according to variant frequency
* Variant impact-specific gene visualizations
* Gene overlap Venn diagrams
* Disease term frequency results
* Disease phrase analysis results
* Disease gene-set bubble plots

These outputs provide an integrated view of variant-associated genes and their potential disease relationships.

## Data Availability

Raw genomic variant files and original annotation datasets are not included in this repository due to privacy, data protection, and data-sharing considerations.

The repository focuses on the computational workflow, analysis scripts, and selected visualization outputs.

## Author

**Evangelos Stylos**
