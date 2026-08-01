"""
04_disease_phrase_analysis.py

Identify frequently occurring two-word and three-word
disease-related phrases across variant impact and
disease categories.

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
    """Clean disease descriptions and remove stopwords."""

    text = str(text).lower()

    text = re.sub(
        r"\(.*?\)",
        "",
        text
    )

    text = re.sub(
        r"[^a-z\s]",
        " ",
        text
    )

    words = text.split()

    return [
        word
        for word in words
        if word not in STOPWORDS
        and len(word) > 2
    ]


def generate_phrases(words):
    """Generate bigrams and trigrams."""

    bigrams = [
        " ".join(words[i:i + 2])
        for i in range(
            len(words) - 1
        )
    ]

    trigrams = [
        " ".join(words[i:i + 3])
        for i in range(
            len(words) - 2
        )
    ]

    return bigrams + trigrams


def analyze_group(group, impact, category):

    term_count = defaultdict(int)
    term_genes = defaultdict(set)

    for _, row in group.iterrows():

        gene = str(row["Gene"])

        words = clean_text(
            row["Malacards"]
        )

        phrases = generate_phrases(
            words
        )

        for phrase in phrases:

            term_count[phrase] += 1

            term_genes[phrase].add(
                gene
            )

    return [
        {
            "Impact": impact,
            "Category": category,
            "Disease_Term": term,
            "Frequency": count,
            "Unique_Genes": len(
                term_genes[term]
            )
        }
        for term, count in term_count.items()
    ]


def main():

    parser = argparse.ArgumentParser(
        description=(
            "Identify frequent disease-related "
            "bigrams and trigrams."
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
            "top_disease_phrases.xlsx"
        ),
        help="Output Excel file."
    )

    parser.add_argument(
        "-n",
        "--top",
        type=int,
        default=10,
        help="Number of top phrases per category."
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

        df = df.dropna(
            subset=[
                "Gene",
                "Malacards",
                "Category"
            ]
        )

        for category, group in df.groupby(
            "Category"
        ):

            results.extend(
                analyze_group(
                    group,
                    sheet,
                    category
                )
            )

    if not results:
        raise ValueError(
            "No valid disease annotation data found."
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
