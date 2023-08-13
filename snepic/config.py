THREADS = 6
LOG_PATH = "./snepic.log"

# replace with the path of PLINK binary (e.g. /usr/bin/plink1.9)
PLINK_COMMAND = "../plink/plink"
# replace with the path of MIDESP jar
MIDESP_JAR = "../MIDESP_1.2.jar"

INPUT_GENO = "../data/soybean_aa_genotypes.vcf"
INPUT_PHENO = "../data/soybean_aa_phenotypes_renamed.tsv"

OUTPUT_GWAS = "./output/gwas_out.assoc.linear"
OUTPUT_MIDESP = "./output/midesp.epi"

# Quality Control params
MAF = 0.05
GENO = 0.05

# indep-pairwise
LD_PARAMS = [10000, 5, 0.99]

# TODO detect automatically
CHR_COUNT = 20

# Phenotype parameter to check
PHENO_PARAM = "Ala"
