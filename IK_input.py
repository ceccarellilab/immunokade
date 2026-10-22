import os
import pandas as pd
import numpy as np
import math
import sys
path_project = os.path.dirname(os.path.abspath(__file__))
path_lib = path_project+os.sep+"src"+os.sep
sys.path.append(path_lib)
from config import path_hla_pocket, path_input


def code_func(pept,side):
    length = len(pept)
    code = "X"*(15-length)
    if side=="left":
        code = pept+code
    else:
        code = code+pept
    return code

def main(path_input_file):
    basename = os.path.basename(path_input_file).split(".")[0]
    file_output = os.path.join(path_input,basename+"_coded.csv")
    print("\nGenerating ImmunoKade input format of the following file:\n",path_input_file)
    data = pd.read_csv(path_input_file)
    
    ## input columns file: "peptide", "hla"
    ## input hla type must be without "HLA-", "*" and ":", see hla_pocket.csv dict
    data["hla"] = data["hla"].apply(lambda x: x.split("-")[1].replace("*", "").replace(":", ""))
    
    print("Input file dim",data.shape)
    data["pept_len"] = data["peptide"].apply(lambda x: len(x))
    print("Peptide length distribution:\n",data["pept_len"].value_counts())
    data = data[data["pept_len"]<=15].reset_index(drop=True)
    
    # 1) Code peptide column: length 15 padding with "X"
    print("\n1. Padding peptide...")
    data["pept_code_left"] = data["peptide"].apply(lambda x: code_func(x,"left"))
    data["pept_code_right"] = data["peptide"].apply(lambda x: code_func(x,"right"))
    print("Done!")
    
    # 2) Merging hla peptide pocket
    hla_pocket = pd.read_csv(path_hla_pocket)
    print("\n2. Coding HLA...")
    df_merge = data.merge(hla_pocket,on="hla",how="left")
    print("Done!")
    print("\nHLA coded file dim",df_merge.shape)
    # if not found, check the key names
    nan_pockets = df_merge[df_merge["hla_peptide_pocket"].isna()].shape[0]
    if nan_pockets>0:
        print("\nWarning!!",nan_pockets,"HLA not found")
        df_merge = df_merge[~(df_merge["hla_peptide_pocket"].isna())].reset_index(drop=True)
        print("Final file dim",df_merge.shape,"\n")
    duplicated = len(df_merge[["peptide","hla"]].drop_duplicates()) - len(df_merge[["peptide","hla_peptide_pocket"]].drop_duplicates())
    if duplicated > 0:
        print("\nWarning, the HLA substitution with the binding pocket generate",duplicated,"duplicated couples\n")
    
    df_merge.to_csv(file_output,index=False)
    print("Final length distribution:\n",df_merge["pept_len"].value_counts())
    print("\nOutput file saved in:\n",file_output,"\n")
    
    return

if __name__ =='__main__':
    
    main(sys.argv[1])
