"""
Identify the top genes with the highest number of variants
from annotated genomic variant data.

Input:
    Excel file containing variant annotation results.

Output:
    - Excel file with top N genes per impact category
    - Bar plots showing gene variant counts

Author:
    Vaggelis Stilos
"""


import os
import argparse
import pandas as pd
import matplotlib.pyplot as plt

from collections import Counter


# ==========================
# Configuration
# ==========================

GENE_COLUMN = "SYMBOL"


# ==========================
# Functions
# ==========================

def load_sheet(file_path, sheet_name):
    """
    Load a specific Excel sheet.
    """

    df = pd.read_excel(
        file_path,
        sheet_name=sheet_name
    )

    df.columns = (
        df.columns
        .astype(str)
        .str.strip()
    )

    return df



def get_gene_counts(df, gene_column):
    """
    Count occurrences of each gene.
    """

    genes = (
        df[gene_column]
        .dropna()
        .astype(str)
    )

    counts = Counter(genes)

    result = pd.DataFrame(
        counts.items(),
        columns=[
            "Gene",
            "Variant_Count"
        ]
    )

    result = result.sort_values(
        by="Variant_Count",
        ascending=False
    )

    return result



def create_barplot(
        dataframe,
        sheet_name,
        output_folder
):
    """
    Create horizontal bar plot
    for top genes.
    """

    plt.figure(
        figsize=(10, 12)
    )

    plt.barh(
        dataframe["Gene"],
        dataframe["Variant_Count"]
    )

    plt.gca().invert_yaxis()

    plt.title(
        f"Top 30 Genes - {sheet_name}"
    )

    plt.xlabel(
        "Number of Variants"
    )

    plt.ylabel(
        "Gene"
    )

    plt.tight_layout()


    output_file = os.path.join(
        output_folder,
        f"top30_genes_{sheet_name}.png"
    )

    plt.savefig(
        output_file,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()



def analyze_variants(
        input_file,
        output_file,
        plot_folder,
        top_n=30
):
    """
    Main analysis workflow.
    """


    excel = pd.ExcelFile(
        input_file
    )


    sheets = excel.sheet_names[:5]


    all_results = []


    for sheet in sheets:


        print(
            f"Processing: {sheet}"
        )


        df = load_sheet(
            input_file,
            sheet
        )


        if GENE_COLUMN not in df.columns:

            print(
                f"Skipping {sheet}: "
                f"missing {GENE_COLUMN}"
            )

            continue


        gene_counts = get_gene_counts(
            df,
            GENE_COLUMN
        )


        top_genes = (
            gene_counts
            .head(top_n)
            .copy()
        )


        top_genes.insert(
            0,
            "Impact",
            sheet
        )


        all_results.append(
            top_genes
        )


        create_barplot(
            top_genes,
            sheet,
            plot_folder
        )


    final_results = pd.concat(
        all_results,
        ignore_index=True
    )


    final_results.to_excel(
        output_file,
        index=False
    )


    print(
        "\nAnalysis completed!"
    )

    print(
        final_results.head()
    )



# ==========================
# Command line execution
# ==========================

if __name__ == "__main__":


    parser = argparse.ArgumentParser(
        description=
        "Extract top variant-associated genes"
    )


    parser.add_argument(
        "-i",
        "--input",
        required=True,
        help="Input Excel file"
    )


    parser.add_argument(
        "-o",
        "--output",
        default="Top_variant_genes.xlsx",
        help="Output Excel file"
    )


    parser.add_argument(
        "-p",
        "--plots",
        default="results/figures",
        help="Folder for plots"
    )


    parser.add_argument(
        "-n",
        "--top",
        type=int,
        default=30,
        help="Number of top genes"
    )


    args = parser.parse_args()


    os.makedirs(
        args.plots,
        exist_ok=True
    )


    analyze_variants(
        input_file=args.input,
        output_file=args.output,
        plot_folder=args.plots,
        top_n=args.top
    )
