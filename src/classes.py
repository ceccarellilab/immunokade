import torch
import torch.nn as nn
from torch.utils.data import DataLoader


##################################################################################
##### Classes NN & DataLoader ImmunoKade - 22th Oct 2026 - Luigi Laezza, PhD #####
##################################################################################



class simple_classifier(nn.Module):
    def __init__(self, clf_input_size, clf_output_size):
        super().__init__()
        self.fc1 = nn.Linear(clf_input_size, clf_output_size)

    def forward(self, x):
        x = self.fc1(x)
        return x


class immunoKade(nn.Module):
    def __init__(self,pretrained,BA_top_nn,EL_top_nn,IM_top_nn):
        super().__init__()
        self.pretrained = pretrained
        self.final_layer = pretrained.num_layers
        self.BA_top_nn = BA_top_nn
        self.EL_top_nn = EL_top_nn
        self.IM_top_nn = IM_top_nn

    def forward(self, x):
        # Get the output from the frozen pretrained model
        x = self.pretrained(x,repr_layers=[self.final_layer], return_contacts=False)
        x = x["representations"][self.final_layer]
        x = x[:,0,:]
        #x = torch.mean(x, dim=1)
        BA_x = self.BA_top_nn(x)
        EL_x = self.EL_top_nn(x)
        IM_x = self.IM_top_nn(x)
        return BA_x, EL_x, IM_x


class IK_Dataset(torch.utils.data.Dataset):
    def __init__(self, df):
        self.features = df["my_idx"].values
        self.label = df[["BA_label","EL_label","IM_label"]].values
        self.original = df[["BA_original","EL_original","IM_original"]].values

    def __len__(self):
        return len(self.features)

    def __getitem__(self, idx):
        return self.features[idx], self.label[idx], self.original[idx]



        

