import subprocess
import logging
from typing import List

import config


def run_proc(args: List[str], stdout = False):
    """
    Runs subprocess and writes stderr to log, stdout to log if stdout is True
    """
    popen = subprocess.Popen(
        args,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
    )
    popen.wait()
    popen.stdout.close()

    if stdout:
        for stdout_line in iter(popen.stdout.readline, ""):
            logging.info(stdout_line.strip())

    if popen.returncode != 0:
        logging.error(f"Something happened during executing {args[0]}... {popen.returncode}")
        for stderr_line in iter(popen.stderr.readline, ""):
            logging.error(stderr_line.strip())
        print(f"Something happened during executing {args[0]}..")
        raise RuntimeError("Check logs")


def run_midesp(tped: str, tfam: str):
    args = [
        "java", 
        "-jar",  config.MIDESP_JAR,
        "-threads", str(config.THREADS), 
        " -out", config.OUTPUT_MIDESP, 
        "-keep", "0.25", "-fdr", "0.005",
        "-cont", "-k", "30",
        "-noapc",       #FIXME че делать
        "./temp/data_ready_to_midesp.tped",
        "./temp/data_ready_to_midesp.tfam",
    ]
    run_proc(args)
