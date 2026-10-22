# ImmunoKade
ImmunoKade is a protein language model that predicts HLA–peptide binding affinity, presentation and immunogenicity


______________________________________________________________________________________________________________________________

## 📂 File Structure
```bash
├── data_input/            # Folder for input files
├── data_output/           # Folder for output files (predictions)
├── models/                # ImmunoKade trained models (5 folds)
├── src/                   # Script and files for IK_input.py and IK_pred.py
│   ├── config.py          # Global variables config
│   ├── classes.py         # Objects definitions
│   ├── utils.py           # Functions for load and use IK model (IK_pred.py)
│   └── hla_pocket.csv     # Dict HLA : 34 amino acids binding poket
├── IK_input.py            # Input preprocessing script
└── IK_pred.py             # BA, EL, IM predictions script
```
______________________________________________________________________________________________________________________________

## 🔧 Dependencies


Install with:

```bash
# 1. Build Conda/Mamba Env
mamba create -n "immunokade" python=3.8.15
mamba activate immunokade

# 2. Insall PyTorch via Conda/Mamba & pip for set the paths
# (our version for gpu is 1.12.1 because of nvidia drivers, but you can use your torch version. Also gpu is not mandatory for run ;)
pip install torch==1.12.1+cu113 -f https://download.pytorch.org/whl/cu113/torch_stable.html
python -c "import torch; print(torch.cuda.is_available())"

# 3. Insall packages via pip
pip install pandas==1.5.2 fair-esm==2.0.0 numpy==1.22.3 scikit-learn==1.1.3 matplotlib==3.6.2 tqdm


```

______________________________________________________________________________________________________________________________

## 🚀 Quick Start

### 1. Input Preparation
`IK_input.py` - Converts your input file into the format required by the ImmunoKade model.<br>
The output is saved in the `data_input` folder.

Usage:

```bash
python ./IK_input.py ./data_input/example_viral.csv
```

Requirements:

- The input CSV must contain the following two columns: `hla`, `peptide`.

- `hla` column: HLA allele name, e.g. `HLA-A*02:01`. See `./src/hla_pocket.csv` for all the available HLAs. If your HLA is not in the dictionary, please add the amino acids of its binding pocket to the dictionary.

- `peptide` column: peptide sequence, e.g. `FLPSPLFFFL`. The peptide length must be between 8 and 15 amino acids.

- Allowed amino acids to code: `ACDEFGHIKLMNPQRSTUVWXYOBZ`


### 2. Run Predictions

`IK_pred.py` - Given the input file coded as required, it generate the BA, EL and IM score.<br>
The output is saved in the `data_output` folder.

Usage:

```bash
python ./IK_pred.py ./data_input/example_viral_coded.csv
```

By default, the script runs on the GPU (device 0). The following options are available:

| Option | Description | Default |
|--------|-------------|---------|
| `-d`, `--device` | Device to run on: `gpu` or `cpu` | `gpu` |
| `-g`, `--gpu-id` | Index of the GPU to use (ignored if `--device cpu`) | `0` |

Examples:

```bash
# Run on the CPU (use this if no GPU is available)
python ./IK_pred.py ./data_input/example_viral_coded.csv -d cpu

# Run on a specific GPU (e.g. the second one)
python ./IK_pred.py ./data_input/example_viral_coded.csv -g 2
```


______________________________________________________________________________________________________________________________

## Data Availability
https://doi.org/10.5281/zenodo.21496931
