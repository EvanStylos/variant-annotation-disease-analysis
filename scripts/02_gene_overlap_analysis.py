"""
02_gene_overlap_analysis.py

Identify overlaps between the top genes from different
variant impact categories and visualize them using a
three-set Venn diagram.

Author:
    Vaggelis Stilos
"""

import argparse
from collections import Counter
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib_venn import venn3


GENE_COLUMN = "SYMBOL"


def get_top_genes(
    input_file,
    sheet_name,
    top_n=30
):
    """Return the top N genes from an Excel sheet."""

    df = pd.read_excel(
        input_file,
        sheet_name=sheet_name
    )

    df.columns = (
        df.columns
        .astype(str)
        .str.strip()
    )

    if GENE_COLUMN not in df.columns:
        raise ValueError(
            f"Column '{GENE_COLUMN}' not found "
            f"in sheet '{sheet_name}'."
        )

    genes = (
        df[GENE_COLUMN]
        .dropna()
        .astype(str)
        .str.strip()
    )

    counts = Counter(genes)

    return set(
        gene
        for gene, _ in counts.most_common(top_n)
    )


def create_venn_diagram(
    gene_sets,
    labels,
    output_file
):
    """Create and save a three-set Venn diagram."""

    plt.figure(figsize=(12, 10))

    venn = venn3(
        gene_sets,
        set_labels=labels
    )

    regions = {
        "100": gene_sets[0] - gene_sets[1] - gene_sets[2],
        "010": gene_sets[1] - gene_sets[0] - gene_sets[2],
        "001": gene_sets[2] - gene_sets[0] - gene_sets[1],
        "110": (gene_sets[0] & gene_sets[1]) - gene_sets[2],
        "101": (gene_sets[0] & gene_sets[2]) - gene_sets[1],
        "011": (gene_sets[1] & gene_sets[2]) - gene_sets[0],
        "111": (
            gene_sets[0]
            & gene_sets[1]
            & gene_sets[2]
        )
    }

    for region_id, genes in regions.items():

        label = venn.get_label_by_id(region_id)

        if label is not None:

            label.set_text(
                "\n".join(sorted(genes))
            )

            label.set_fontsize(7)

    plt.title(
        "Overlap of Top Variant-Associated Genes"
    )

    plt.tight_layout()

    plt.savefig(
        output_file,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()


def main():

    parser = argparse.ArgumentParser(
        description=(
            "Analyze overlap between top genes "
            "from three variant impact categories."
        )
    )

    parser.add_argument(
        "-i",
        "--input",
        required=True,
        help="Input Excel file."
    )

    parser.add_argument(
        "--sheets",
        nargs=3,
        default=["High", "Moderate", "Low"],
        help=(
            "Three Excel sheets to compare. "
            "Default: High Moderate Low"
        )
    )

    parser.add_argument(
        "-n",
        "--top",
        type=int,
        default=30,
        help="Number of top genes per category."
    )

    parser.add_argument(
        "-o",
        "--output",
        default="results/figures/top_gene_overlap.png",
        help="Output Venn diagram."
    )

    args = parser.parse_args()

    gene_sets = [
        get_top_genes(
            args.input,
            sheet,
            args.top
        )
        for sheet in args.sheets
    ]

    output_file = Path(args.output)

    output_file.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    create_venn_diagram(
        gene_sets,
        args.sheets,
        output_file
    )

    print(
        f"Venn diagram saved to: {output_file}"
    )


if __name__ == "__main__":
    main()
