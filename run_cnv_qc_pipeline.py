import argparse
import pandas as pd

from CNV.cnv import cnv_qc

parser = argparse.ArgumentParser(description='Perform quality control on genotype data')
parser.add_argument('--geno_path', help='Path to genotype data file')
parser.add_argument('--out_path', help='Output path for QC files')
parser.add_argument('--covar_path', help='Path to covariate file with matching ids to the genotype')
parser.add_argument('--maf', type=float, default=0.01, help='Minor allele frequency threshold')
parser.add_argument('--geno', type=float, default=0.02, help='Genotyping rate threshold')
parser.add_argument('--hwe', type=float, default=5e-6, help='Hardy-Weinberg equilibrium p-value threshold')
parser.add_argument('--indep_pairwise', nargs=3, type=float, default=[1000, 10, 0.01], help='SNP pruning parameters [window size, step size, r^2 threshold]')
parser.add_argument('--samples_path', default=None, help='Path to sample metadata file')

args = parser.parse_args()

geno_path = args.geno_path
out_path = args.out_path
covar_path = args.covar_path
maf = args.maf
geno = args.geno
hwe = args.hwe
indep_pairwise = args.indep_pairwise
samples_path = args.samples_path

cnv_qc(geno_path, out_path, maf=maf, geno=geno, hwe=hwe, indep_pairwise=indep_pairwise, samples_path=samples_path)

covar = pd.read_csv(covar_path, dtype={'FID':str, 'GP2sampleID':str})
pcs = pd.read_csv(f'{out_path}.eigenvec', sep='\s+')
pc_num = pcs.iloc[:, 2:].shape[1]
pc_names = ['FID','GP2sampleID'] + [f'PC{i}' for i in range(1, pc_num+1)]
pcs.columns = pc_names
pcs.loc[:,'FID'] = pcs.loc[:,'FID'].astype(str)
pcs.loc[:,'GP2sampleID'] = pcs.loc[:,'GP2sampleID'].astype(str)

cov = pcs.merge(covar, on=['FID','GP2sampleID'], how='left')
cov.age.fillna(cov.age.mean(), inplace=True)
cov.age_of_onset.fillna(cov.age_of_onset.mean(), inplace=True)
cov.sex_for_qc.fillna(cov.sex_for_qc.median(), inplace=True)
cov.rename(columns={'GP2sampleID':'sampleid','sex_for_qc':'sex'}, inplace=True)
cov.to_csv(f'{out_path}.cov', sep='\t', header=True, index=False)

# samples = cov.merge(key[['GP2sampleID','IID']], left_on='sampleid', right_on='GP2sampleID', how='left')
# samples['IID'].to_csv(f'{out_path}_barcode.samples', header=False, index=False)

bim = pd.read_csv(f'{out_path}.bim', sep='\s+', header=None, names=['chr','id','pos','bp','a1','a2'], usecols=['id'])
bim.to_csv(f'{out_path}.snps', sep='\t', header=False, index=False)