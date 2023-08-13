import logging
import subprocess
from typing import List
from pathlib import Path
from sys import argv as sysargs

import config
from prep import manipulate, plink
from proc import run_midesp


logging.basicConfig(
    format='%(levelname)s:%(asctime)s %(message)s',
    datefmt='%Y/%m/%d %I:%M:%S %p',
    filename=config.LOG_PATH,
    level=logging.INFO
)


def print_config() -> None:
    """
    Prints config variables
    """
    print("PARAMETERS:")
    for param, val in config.__dict__.items():
        print(f"{param}: {val}")



def create_dir(dir: str) -> None:
    """
    Creates dir if not exists
    """
    Path(dir).mkdir(parents=True, exist_ok=True)
    logging.info("now /temp exists.")


# TODO check if java is 8+
# FIXME paths from config
def main():
    print_config()

    PHENO_PARAM = config.PHENO_PARAM
    if len(sysargs) > 1 and sysargs[1] != config.PHENO_PARAM:
        print(f"New pheno param is {sysargs[1]}")
        PHENO_PARAM = sysargs[1]


    print("Proceed? y or n")
    b = input()
    if b == "n":
        print("bye")
        return 1
    logging.info("START")

    create_dir("./temp")
    create_dir(Path(config.OUTPUT_GWAS).parent)
    # prepare pheno (rename IDs)
    prepared_pheno_path = manipulate.prepare_pheno(config.INPUT_PHENO)
    # select param from config
    selected_pheno_path = manipulate.select_columns(prepared_pheno_path, ["FID", "IID", PHENO_PARAM])
    prepared_geno_path = manipulate.prepare_geno()

    # run plink pipeline (filter data and GWAS)
    plink.run_pipeline(selected_pheno_path, prepared_geno_path, PHENO_PARAM)
    
    # run MIDESP
    run_midesp()


if __name__ == "__main__":
    main()
