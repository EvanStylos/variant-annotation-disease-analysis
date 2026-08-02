"""
05_disease_gene_set_bubbleplot.py

Visualize disease gene-set analysis results using a bubble plot.

Bubble size represents the number of matched genes.
Color represents the gene-disease evidence score.

Author:
    Vaggelis Stilos
"""

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def load_results(input_file, sheet_name):
    """Load and prepare disease gene-set analysis results."""

    df = pd.read_excel(
        input_file,
        sheet_name=sheet_name
    )

    df.columns = (
        df.columns
        .astype(str)
        .str.strip()
    )

    required_columns = {
        "Disease",
        "Score",
        "Matched Gene(s)",
        "Matched Gene–Disease"
    }

    missing = (
        required_columns
        - set(df.columns)
    )

    if missing:
        raise ValueError(
            f"Missing columns: {missing}"
        )

    df["MatchedGenes"] = (
        df["Matched Gene(s)"]
        .astype(str)
        .str.extract(
            r"(\d+)",
            expand=False
        )
        .astype(float)
    )

    return df.sort_values(
        "Score",
        ascending=True
    )


def create_bubble_plot(
    df,
    output_file
):
    """Create and save the disease prioritization plot."""

    plt.figure(
        figsize=(
            18,
            max(8, len(df) * 0.35)
        )
    )

    sns.scatterplot(
        data=df,
        x="Score",
        y="Disease",
        size="MatchedGenes",
        hue="Matched Gene–Disease",
        sizes=(50, 900),
        alpha=0.85
    )

    plt.title(
        "Disease Gene Set Analysis",
        fontsize=18,
        weight="bold",
        pad=20
    )

    plt.xlabel(
        "Score",
        fontsize=14
    )

    plt.ylabel(
        "",
        fontsize=14
    )

    plt.xticks(
        fontsize=11
    )

    plt.yticks(
        fontsize=10
    )

    plt.legend(
        bbox_to_anchor=(
            1.1,
            0.9
        ),
        loc="upper left",
        borderaxespad=0,
        fontsize=9,
        title="Evidence"
    )

    plt.subplots_adjust(
        left=0.4,
        right=0.65,
        top=0.9,
        bottom=0.1
    )

    plt.savefig(
        output_file,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()


def main():

    parser = argparse.ArgumentParser(
        description=(
            "Create a bubble plot from "
            "disease gene-set analysis results."
        )
    )

    parser.add_argument(
        "-i",
        "--input",
        required=True,
        help="Input Excel file."
    )

    parser.add_argument(
        "-s",
        "--sheet",
        default="Disease Gene Set Analysis",
        help="Excel sheet containing analysis results."
    )

    parser.add_argument(
        "-o",
        "--output",
        default=(
            "results/figures/"
            "disease_gene_set_bubbleplot.png"
        ),
        help="Output image file."
    )

    args = parser.parse_args()

    output_file = Path(
        args.output
    )

    output_file.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    df = load_results(
        args.input,
        args.sheet
    )

    create_bubble_plot(
        df,
        output_file
    )

    print(
        f"Bubble plot saved to: {output_file}"
    )


if __name__ == "__main__":
    main()
