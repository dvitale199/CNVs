import pandas as pd
import argparse

parser = argparse.ArgumentParser(description='outputting snp metrics for gene')
parser.add_argument('--metrics_file', type=str, default='nope', help='per-sample snp metrics parquet file path')
parser.add_argument('--chrom', type=str, default='nope', help='chromosome')
parser.add_argument('--gene_start', type=int, default='nope', help='start position')
parser.add_argument('--gene_end', type=int, default='nope', help='end position')
parser.add_argument('--out_path', type=str, default='nope', help='output file for gene')

args = parser.parse_args()

metrics_file = args.metrics_file
chrom = args.chrom
gene_start = args.gene_start
gene_end = args.gene_end
out_path = args.out_path

snp_metrics = pd.read_parquet(metrics_file)
snp_metrics.loc[:,'chromosome'] = snp_metrics.loc[:,'chromosome'].astype(str)
gene = snp_metrics.loc[(snp_metrics['chromosome']==chrom) & (snp_metrics['position']>=gene_start) & (snp_metrics['position']<=gene_end)]
gene.to_csv(out_path, header=True, index=False)