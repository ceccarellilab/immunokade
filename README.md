# ImmunoKade
ImmunoKade is a protein language model that predicts HLA–peptide binding affinity, presentation and immunogenicity


______________________________________________________________________________________________________________________________

## 📂 File Structure
```bash
├── data_input/            # Processed input files
├── data_output/           # Prediction outputs
├── model_EL/              # ESM2FT_EL model files
├── model_IM/              # ESM2FT_IM model files
├── src/
│   ├── config.py          # 
│   ├── classes.py         # 
│   ├── trainer.py         # 
│   ├── utils.py           # 
│   └── hla_pocket.csv     # HLA format reference
├── ESM2FT_input_file.py   # Input preprocessing
├── ESM2FT_EL_pred.py      # EL prediction script
└── ESM2FT_IM_pred.py      # IM prediction script
```
______________________________________________________________________________________________________________________________

## 🔧 Dependencies


Install with:

```bash
# 1. Build Conda/Mamba Env
mamba create -n "immunokade" python=3.8.15
mamba activate immunokade

# 2. Insall PyTorch via Conda/Mamba & pip for set the paths
# (our version for gpu is 1.12.1 because of nvidia drivers, but you can use your torch version. Also gpu is not mandatory for run)
pip install torch==1.12.1+cu113 -f https://download.pytorch.org/whl/cu113/torch_stable.html
python -c "import torch; print(torch.cuda.is_available())"

# 3. Insall packages via pip
pip install pandas==1.5.2 fair-esm==2.0.0 numpy==1.22.3 scikit-learn==1.1.3 matplotlib==3.6.2 tqdm


```

______________________________________________________________________________________________________________________________

## 🚀 Quick Start

### 1. Input Preparation
Generate the input file in the format required by ESM2FT models. The output is saved in the `data_input` folder. Usage:

```bash
python ./ESM2FT_input_file.py /path/to/data.csv
```

Requirements:

- Input CSV must contain columns: `hla`, `peptide`

- HLA format: See `src/hla_pocket.csv`

- Peptide length: 8-15mer


### 2. Run Predictions

- `ESM2FT_EL_pred.py` - Given the input file coded as required, it generate the ESM2FT_EL score.<br>
The output is saved in the `data_output` folder. Usage:

```bash
python ./ESM2FT_EL_pred.py ./data_input/data_coded.csv
```

- `ESM2FT_IM_pred.py` - Given the input file coded as required, it generate the ESM2FT_IM score.<br>
The output is saved in the `data_output` folder. Usage:

```bash
python ./ESM2FT_IM_pred.py ./data_input/data_coded.csv
```

______________________________________________________________________________________________________________________________

## Data Availability
[https://doi.org/10.5281/zenodo.21496931]https://doi.org/10.5281/zenodo.21496931
