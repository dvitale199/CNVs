import pandas as pd
import argparse

parser = argparse.ArgumentParser(description='outputting snp metrics for gene')
parser.add_argument('--metrics_file', type=str, default='nope', help='per-sample snp metrics parquet file path')
parser.add_argument('--snp_list', type=str, default='nope', help='snp list file')
parser.add_argument('--sample_id', type=str, default='nope', help='sample id to add as column')
parser.add_argument('--out_path', type=str, default='nope', help='output file for gene')

args = parser.parse_args()

metrics_file = args.metrics_file
snp_list = args.snp_list
sample_id = args.sample_id
out_path = args.out_path


snp_list_df = pd.read_csv(snp_list)
snp_list_df[['chromosome','position']] = snp_list_df.loc[:,'hg19'].str.split(':', expand=True)
snp_list_df.loc[:,'chromosome'] = snp_list_df.loc[:,'chromosome'].astype(str)
snp_list_df.loc[:,'position'] = snp_list_df.loc[:,'position'].astype(str)

metrics = pd.read_parquet(metrics_file)
metrics.loc[:,'chromosome'] = metrics.loc[:,'chromosome'].astype(str)
metrics.loc[:,'position'] = metrics.loc[:,'position'].astype(str)
metrics.loc[:,'sample_id'] = sample_id
snp_list_df_metrics = snp_list_df.merge(metrics, how='left', on=['chromosome','position']).drop(columns=snp_list_df.columns)
snp_list_df_metrics = snp_list_df_metrics.drop_duplicates()
snp_list_df_metrics.to_csv(out_path, index=False)