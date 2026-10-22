import pandas as pd
import numpy as np
import torch
from torch import nn
import esm
import argparse
from tqdm import tqdm
from torch.utils.data import DataLoader
from classes import simple_classifier, IK_Dataset, immunoKade

##########################################################################
##### Utils Functions ImmunoKade - 22th Oct 2026 - Luigi Laezza, PhD #####
##########################################################################


# --- Input Config ---

def parse_args():
    parser = argparse.ArgumentParser(description="Script description")
    parser.add_argument("input_data", help="input dataset path")
    parser.add_argument(
        "-d", "--device",
        choices=["gpu", "cpu"],
        default="gpu",
        help="device on which to execute (default: gpu)",
        )
    parser.add_argument(
        "-g", "--gpu_id",
        type=int,
        default=0,
        help="index of the GPU to use; ignored if --device cpu (default: 0)",
        )
    parser.add_argument(
        "-bs", "--batch_size",
        type=int,
        default=2048,
        help="batch size to load in the model (default: 2048)",
        )
    return parser.parse_args()



# --- Model Setup ---

def load_esm_model(device):
    model, alphabet = esm.pretrained.esm2_t6_8M_UR50D()
    model = model.to(device)
    batch_converter = alphabet.get_batch_converter()
    return model, batch_converter


def load_IK_model(model_path, device):
    esm2, batch_converter = load_esm_model(device)

    BA_classifier = simple_classifier(320,1).to(device)
    EL_classifier = simple_classifier(320,1).to(device)
    IM_classifier = simple_classifier(320,1).to(device)

    model = immunoKade(esm2, BA_classifier,EL_classifier,IM_classifier)

    model.load_state_dict(torch.load(model_path,map_location=device))
    return model, batch_converter


def freeze_mode_model(model):
    for param in model.parameters():
        param.requires_grad = False
    model.eval()
    return model



# --- Data ---

def getDataCoded(hla_peptide_code,batch_converter, tokens_len):
    ### dict_code
    batch_labels, batch_strs, batch_tokens = batch_converter([('1','ACDEFGHIKLMNPQRSTUVWXYOBZ')])
    batch_tokens = batch_tokens.view(-1)
    dict_code = {}
    for x,y in zip(list(batch_strs[0]),batch_tokens[1:tokens_len]):
        dict_code[x]=int(y)
    ###
    df_aa_to_idx = pd.DataFrame([dict_code])
    aa_to_idx_ndim = df_aa_to_idx[np.concatenate(hla_peptide_code["combined"].apply(lambda x : list(x)))].to_numpy().reshape(-1, tokens_len)
    torch_aa_to_idx = torch.tensor(aa_to_idx_ndim, dtype=torch.long)
    return torch_aa_to_idx


def getDataLoader(df, shuf, batch_size):
    if shuf:
        df = df.sample(frac=1,random_state=42).reset_index(drop=True)
    dataset = IK_Dataset(df) #batch of (feature, labels) ; in our case features are indexes pointing fetures matrix rows
    dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=False)
    return dataloader



# --- Prediction ---

def IK_extract_probability(model, encoding, dataset, batch_size, device):
    final_layer = model.pretrained.num_layers
    dataloader = getDataLoader(df=dataset, shuf=False, batch_size=batch_size)
    sequence_representations = []
    prob_seq_BA = []
    prob_seq_EL = []
    prob_seq_IM = []
    for batch in tqdm(dataloader):
        inputs = encoding[batch[0], :].to(device)
        with torch.no_grad():
            embedding = model.pretrained(inputs, repr_layers=[final_layer], return_contacts=False)
            output_BA, output_EL, output_IM = model(inputs)
        token_representations = embedding["representations"][final_layer]
        seq_repr = token_representations[:,0,:]
        sequence_representations.append(seq_repr.cpu())
        prob_BA = nn.Sigmoid()(output_BA)
        prob_EL = nn.Sigmoid()(output_EL)
        prob_IM = nn.Sigmoid()(output_IM)
        
        prob_seq_BA.append(prob_BA.cpu())
        prob_seq_EL.append(prob_EL.cpu())
        prob_seq_IM.append(prob_IM.cpu())
    embeddings = torch.cat(sequence_representations, dim=0)
    probability_BA = torch.cat(prob_seq_BA, dim=0)
    probability_EL = torch.cat(prob_seq_EL, dim=0)
    probability_IM = torch.cat(prob_seq_IM, dim=0)
    return embeddings, probability_BA, probability_EL, probability_IM


def aggregate_probs_vectorized(probs_matrix, a):
    probs_matrix = np.clip(probs_matrix, 1e-10, 1-1e-10)
    logits_matrix = np.log(probs_matrix / (1 - probs_matrix))
    Y_bar = np.mean(logits_matrix, axis=1)
    corrected_logits = a * Y_bar
    p_hat = np.exp(corrected_logits) / (1 + np.exp(corrected_logits))
    return p_hat


