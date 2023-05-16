# from CNV.cnv import create_cnv_dosage_matrices
import argparse
import pandas as pd

parser = argparse.ArgumentParser(description='Arguments for Running CNV Pipeline.')    
parser.add_argument('--files', type=str, default='Nope.', help='df with one column with sample ids and no header')
parser.add_argument('--label', type=str, default='Nope.', help='ancestry label')
parser.add_argument('--cnv_type', type=str, default='Nope.', help='type of cnv.')
parser.add_argument('--out_path', type=str, default='Nope.', help='Path to prefix for output files.')
args = parser.parse_args()

files = args.files 
files_df = pd.read_csv(files, header=None)
files_list = list(files_df.loc[:,0])
label = args.label
cnv_type = args.cnv_type
out_path = args.out_path

dosage_ = pd.DataFrame()

for sample_file in files_list:

    sample = sample_file.split('/')[-1].replace(f'CNV_{label}_','').replace(f'.parquet','')
    cnvs = pd.read_parquet(sample_file)
    cnvs.loc[:,'sampleid'] = sample
    cnvs_final = cnvs.loc[~cnvs[cnv_type].isna()]
    dosage = cnvs_final.loc[:,[cnv_type,'INTERVAL','sampleid']]
    dosage_pivot = dosage.pivot(index='sampleid', columns='INTERVAL', values=cnv_type)

    dosage_ = pd.concat([dosage_, dosage_pivot])
dosage_.to_csv(out_path)
