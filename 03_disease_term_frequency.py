"""
03_disease_term_frequency.py

Analyze disease-associated terms across gene-disease
annotations.

For each variant impact category and disease category,
the script identifies frequently occurring disease terms
and counts the number of unique genes associated with
each term.

Author:
    Vaggelis Stilos
"""

import argparse
import re
from collections import defaultdict
from pathlib import Path

import pandas as pd


STOPWORDS = {
    "disease",
    "diseases",
    "syndrome",
    "syndromes",
    "disorder",
    "disorders",
    "type",
    "types",
    "associated",
    "association",
    "familial",
    "hereditary",
    "susceptibility",
    "protein",
    "autosomal",
    "dominant",
    "recessive",
    "linked",
    "congenital",
    "deficiency",
    "adult",
    "juvenile",
    "early",
    "late",
    "primary",
    "secondary"
}


def clean_text(text):
    """Convert disease text into informative terms."""

    text = str(text).lower()

    text = re.sub(
        r"[^a-z0-9\s]",
        " ",
        text
    )

    words = text.split()

    return [
        word
        for word in words
        if len(word) >= 3
        and word not in STOPWORDS
    ]


def analyze_sheet(
    dataframe,
    impact
):
    """Analyze disease terms within one impact category."""

    dataframe = dataframe.dropna(
        subset=[
            "Gene",
            "Malacards",
            "Category"
        ]
    )

    results = []

    for category, group in dataframe.groupby(
        "Category"
    ):

        term_frequency = defaultdict(int)
        term_genes = defaultdict(set)

        for _, row in group.iterrows():

            gene = str(row["Gene"])

            terms = clean_text(
                row["Malacards"]
            )

            for term in terms:

                term_frequency[term] += 1

                term_genes[term].add(
                    gene
                )

        for term, frequency in term_frequency.items():

            results.append({
                "Impact": impact,
                "Category": category,
                "Term": term,
                "Frequency": frequency,
                "Unique_Genes": len(
                    term_genes[term]
                )
            })

    return results


def main():

    parser = argparse.ArgumentParser(
        description=(
            "Identify frequent disease-associated "
            "terms across impact categories."
        )
    )

    parser.add_argument(
        "-i",
        "--input",
        required=True,
        help="Input Excel file."
    )

    parser.add_argument(
        "-o",
        "--output",
        default=(
            "results/tables/"
            "top_disease_terms.xlsx"
        ),
        help="Output Excel file."
    )

    parser.add_argument(
        "-n",
        "--top",
        type=int,
        default=10,
        help="Number of top terms per category."
    )

    args = parser.parse_args()

    excel = pd.ExcelFile(
        args.input
    )

    results = []

    for sheet in excel.sheet_names:

        print(
            f"Processing: {sheet}"
        )

        df = pd.read_excel(
            args.input,
            sheet_name=sheet
        )

        df.columns = (
            df.columns
            .astype(str)
            .str.strip()
        )

        required_columns = {
            "Gene",
            "Malacards",
            "Category"
        }

        if not required_columns.issubset(
            df.columns
        ):
            print(
                f"Skipping {sheet}: "
                "required columns are missing."
            )
            continue

        results.extend(
            analyze_sheet(
                df,
                sheet
            )
        )

    if not results:
        raise ValueError(
            "No valid data were found."
        )

    results_df = pd.DataFrame(
        results
    )

    results_df = results_df.sort_values(
        [
            "Impact",
            "Category",
            "Frequency"
        ],
        ascending=[
            True,
            True,
            False
        ]
    )

    top_results = (
        results_df
        .groupby(
            ["Impact", "Category"],
            group_keys=False
        )
        .head(args.top)
    )

    output_file = Path(
        args.output
    )

    output_file.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    top_results.to_excel(
        output_file,
        index=False
    )

    print(
        f"Results saved to: {output_file}"
    )


if __name__ == "__main__":
    main()
