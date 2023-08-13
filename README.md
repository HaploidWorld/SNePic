# SNePic
A pipeline to detect epistatic SNPs that affect some trait.

### Installation

We will need python3.10+, [plink1.9](https://www.cog-genomics.org/plink/1.9/), [MIDESP 1.2](https://github.com/FelixHeinrich/MIDESP) and Java 8+.

0. Install plink1.9 and MIDESP jar. 
1. Clone the repository and install everything from `./requirements.txt`.
2. Edit the `snepic/config.py`.

### Run

- `python3 snepic [params]` from the repository directory.

#### Params

- Phenotype parameter to study, e.g. `python3 snepic Ala`. This parameter overrides the value from `config.py`.

### Configuration

`snepic/config.py` has several parameters:

- `THREADS int` - threads to use for MIDESP
- `LOG_PATH str` - path for the program log. It doesn't create directories.
- `PLINK_COMMAND str` - path for the PLINK binary
- `INPUT_GENO str` - path for the VCF file with genotypes
- `INPUT_PHENO str` - path for the TSV file with phenotypes
- `OUTPUT_GWAS str` - path for the GWAS results
- `OUTPUT_MIDESP str` - path for the MIDESP results
- `MAF float` - [Minor Allele Frequency](https://www.cog-genomics.org/plink/1.9/filter#maf) for PLINK
- `GENO float` - [geno filter flag](https://www.cog-genomics.org/plink/1.9/filter#missing) for PLINK
- `LD_PARAMS List[float]` - list of [indep-pairwise params](https://www.cog-genomics.org/plink/1.9/ld#indep) for PLINK
- `CHR_COUNT int` - amount of chromosomes.
- `PHENO_PARAM str` - phenotype parameter to study. It should have the same name as in the INPUT_PHENO file.

### What does this program do?

1. Filter input data: create SNP IDs (chr name + pos), rename IDs, LD pruning, ...
2. GWAS via plink (--linear)
3. MIDESP analysis
4. Graph construction
5. Selection of SNPs


### Credits

Team members:
Lavrentii Danilov,
Mikhail Rayko,
Vera Panova,
Kseniia Maksimova,
Kseniia Struikhina,
Alexey Kosolapov,
Anna Bubnova





