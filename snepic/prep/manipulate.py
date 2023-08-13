from typing import List
import io
import pandas as pd
from pathlib import Path
import logging

from config import INPUT_GENO


def add_to_filename(filepath: str, to_add: str) -> str:
    """
    Adds to_add to the end of filename
    """
    pth = Path(filepath)
    filename = pth.stem
    suffix = pth.suffix
    pth = pth.parent
    return f"{pth}/{filename}_{to_add}{suffix}"


def select_columns(filepath: str, columns: List[str], output: str = "") -> str:
    """
    Saves modified tsv that contains only selected columns and returns the new file path
    """
    if not output:
        output = add_to_filename(filepath, "but_" + ", ".join(columns))
    pheno = pd.read_csv(filepath, sep="\t")
    pheno.to_csv(output, columns=columns, sep="\t", index=False)
    logging.info(f"selected columns and saved to {output}")
    return output


def rename_IDs(filepath: str) -> str:
    """
    Renames IDs so they are ok for plink and returns the new file path
    """
    save_to = add_to_filename(filepath, "renamed")
    pheno = pd.read_csv(filepath, sep="\t")
    pheno.drop(columns=["IID"], inplace=True)
    pheno["FID"] = pheno["FID"].str.replace("-", "_").replace(" ", "_")
    pheno.insert(1, "IID", pheno["FID"])
    pheno.to_csv(save_to, sep="\t", index=False)
    logging.info(f"renamed IDs and added SNP's id to {save_to}")
    return save_to


def prepare_pheno(pheno_path: str) -> str:
    """
    Prepares pheno data and returns the new file path
    """
    renamed_pheno = rename_IDs(pheno_path)
    return renamed_pheno


def prepare_geno() -> str:
    """
    Prepares geno data and returns the new file path
    """
    save_to = add_to_filename(INPUT_GENO, "IDs")
    with open(INPUT_GENO, 'r') as f:
        lines = [l for l in f if not l.startswith('##')]
    geno = pd.read_csv(io.StringIO(''.join(lines)), sep="\t")

    # FIXME 5 only for soybean
    geno.loc[:, "#CHROM"] = geno.loc[:, "#CHROM"].str[5:]
    geno["ID"] = geno[["#CHROM", "POS"]].astype(str).agg(':'.join, axis=1)

    geno.to_csv(save_to, sep="\t", index=False)
    logging.info(f"geno prepared and saved to {save_to}")

    return save_to
