import os
import gc
import torch
import pandas as pd
from tqdm import tqdm
import numpy as np
import sys
path_project = os.path.dirname(os.path.abspath(__file__))
path_lib = path_project+os.sep+"src"+os.sep
sys.path.append(path_lib)

from utils import parse_args, getDataCoded, load_IK_model, freeze_mode_model, IK_extract_probability, aggregate_probs_vectorized
from config import tokens_len, path_output, path_model_ik_f1, path_model_ik_f2, path_model_ik_f3, path_model_ik_f4, path_model_ik_f5


#####################################################################
##### ImmunoKade Prediction - 22th Oct 2026 - Luigi Laezza, PhD #####
#####################################################################



def main(path_dataset,device,device_id,batch_size):
    # --- Config ---
    basename = os.path.basename(path_dataset).split(".")[0]
    file_probability = os.path.join(path_output,basename+"_ImmunoKade_score.csv")
    if device=="gpu":
        os.environ["CUDA_VISIBLE_DEVICES"] = str(device_id)
    else:
        os.environ["CUDA_VISIBLE_DEVICES"] = ""
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print("Using device:", os.environ.get("CUDA_VISIBLE_DEVICES"))
    print("Batch size:", batch_size)


    model_list = [path_model_ik_f1, path_model_ik_f2, path_model_ik_f3, path_model_ik_f4, path_model_ik_f5]
    
    # --- Data ---
    print("\nLoading and encoding data..")
    df = pd.read_csv(path_dataset,low_memory=False)
    df["combined"] = df["pept_code_left"]+df["hla_peptide_pocket"]+df["pept_code_right"]
    model, batch_converter = load_IK_model(model_list[0], device)
    encoding = getDataCoded(df, batch_converter, tokens_len)
    dataset = pd.DataFrame({"my_idx": df["combined"].index.to_list(),
                            "BA_label": [2]*len(df),"EL_label": [2]*len(df),"IM_label": [2]*len(df),
                            "BA_original": [False]*len(df),"EL_original": [False]*len(df),"IM_original": [False]*len(df)
                           }) # label is not useful for the output, but the dataloader need something
    print("Done!")
    
    print("\n\n############# Model prediction start! #############\n")
    for fold in range(0,5):
        path_model = model_list[fold]
        
        # --- Model Setup ---
        model, batch_converter = load_IK_model(path_model, device)
        model = freeze_mode_model(model)
        model.to(device)
        print("\n\nFold",fold+1,"- Using model in:")
        print(path_model)
        # --- Embedding & Probability extraction ---
        embeddings, probability_BA, probability_EL, probability_IM = IK_extract_probability(
            model, encoding, dataset, batch_size, device)
        if fold ==0:
            data = df.copy()
        data["ImmunoKade_BA_f"+str(fold+1)] = probability_BA
        data["ImmunoKade_EL_f"+str(fold+1)] = probability_EL
        data["ImmunoKade_IM_f"+str(fold+1)] = probability_IM

    
    ImmunoKade_flods_BA = ["ImmunoKade_BA_f"+str(fold+1) for fold in range(5)]
    ImmunoKade_flods_EL = ["ImmunoKade_EL_f"+str(fold+1) for fold in range(5)]
    ImmunoKade_flods_IM = ["ImmunoKade_IM_f"+str(fold+1) for fold in range(5)]
    
    a=1
    data["ImmunoKade_BA"] = aggregate_probs_vectorized(data[ImmunoKade_flods_BA].values, a)
    data["ImmunoKade_EL"] = aggregate_probs_vectorized(data[ImmunoKade_flods_EL].values, a)
    data["ImmunoKade_IM"] = aggregate_probs_vectorized(data[ImmunoKade_flods_IM].values, a)
    
    data = data.drop(columns = ImmunoKade_flods_BA+ImmunoKade_flods_EL+ImmunoKade_flods_IM)
    data = data.drop(columns=["combined"])
    data.to_csv(file_probability,index=False)
    print(f"\n\nSaved probability to {file_probability}\n")
    
    # --- Cleanup ---
    gc.collect()
    torch.cuda.empty_cache()

if __name__ == "__main__":
    args = parse_args()
    main(args.input_data, args.device, args.gpu_id, args.batch_size)















