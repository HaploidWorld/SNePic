from typing import List
import logging

from proc import run_proc
import config


CHR_SET_FLAG = ["--chr-set", str(config.CHR_COUNT)]
NOSEX_AND_EXTRA_CHR = ["--allow-no-sex", "--allow-extra-chr"]


def run(params: List[str]):
    """
    Runs plink with additional params
    """
    args = [
        config.PLINK_COMMAND,
    ] + params
    run_proc(args)


def run_pipeline(filtered_pheno_path, prepared_geno_path, pheno_param):
    """
    Runs plink pipeline: QC, LD pruning, GWAS
    """
    run_filtering(filtered_pheno_path, prepared_geno_path)
    run_GWAS(filtered_pheno_path, pheno_param)


def run_filtering(filtered_pheno_path, prepared_geno_path):
    """
    Runs filtering: QC and LD pruning 
    """
    print_and_log("Plink filtering starts...")

    run_qc(filtered_pheno_path, prepared_geno_path)
    print_and_log("QC done")
    
    run_LD_pruning()
    print_and_log("LD Pruning done")
    
    print_and_log("Filtering done...")


def run_qc(filtered_pheno_path, prepared_geno_path):
    """
    Runs QC
    """
    params = [
        "--vcf", prepared_geno_path,
        "--pheno", filtered_pheno_path,
        "--prune",
        "--double-id",
        "--maf", str(config.MAF),
        "--geno", str(config.GENO),
        "--make-bed",
        "--out", "./temp/data_after_qc"
    ] + CHR_SET_FLAG + NOSEX_AND_EXTRA_CHR
    run(params)


def run_LD_pruning():
    """
    Runs LD pruning
    """
    params1 = [
        "--indep-pairwise"] + [str(x) for x in config.LD_PARAMS] + [ 
        "--make-founders",
        "--double-id",
        "--out", "./temp/data_after_ld1",
        "--bfile", "./temp/data_after_qc"
    ] + CHR_SET_FLAG + NOSEX_AND_EXTRA_CHR
    params2 = [
        "--double-id", 
        "--extract", "./temp/data_after_ld1.prune.in",
        "--make-founders",
        "--out", "./temp/data_after_ld2",
        "--bfile", "./temp/data_after_qc", "--make-bed"
    ] + CHR_SET_FLAG + NOSEX_AND_EXTRA_CHR
    params3 = [
        "--bfile", "./temp/data_after_ld2",
        "--recode", "transpose",
        "--out", "./temp/data_ready_to_midesp"
    ] + CHR_SET_FLAG + NOSEX_AND_EXTRA_CHR
    run(params1)
    run(params2)
    run(params3)


def run_GWAS(filtered_pheno_path, pheno_param):
    """
    Runs GWAS
    """
    params = [
    "--bfile", "./temp/data_after_ld2",
    "--pheno", filtered_pheno_path,
    "--pheno-name", pheno_param,
    "--linear", "--adjust",
    "--out", config.OUTPUT_GWAS
    ] + NOSEX_AND_EXTRA_CHR

    print_and_log("GWAS starts...")
    run(params)


def print_and_log(msg: str):
    """
    Prints msg to stdout and writes msg to log
    """
    logging.info(msg)
    print(msg)
