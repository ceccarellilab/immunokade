# ImmunoKade
ImmunoKade is a protein language model that predicts HLA–peptide binding affinity, presentation and immunogenicity


______________________________________________________________________________________________________________________________

## 📂 File Structure
```bash
├── data_input/            # Folder for input files
├── data_output/           # Folder for output files (predictions)
├── models/                # ImmunoKade trained models (5 folds)
├── src/                   # Script and files for IK_input.py and IK_pred.py
│   ├── config.py             # Global variables config
│   ├── classes.py            # Objects definitions
│   ├── utils.py              # Functions for load and use IK model (IK_pred.py)
│   └── hla_pocket.csv        # Dict HLA : 34 amino acids binding poket
├── IK_input.py            # Input preprocessing script
└── IK_pred.py             # BA, EL, IM predictions script
```
______________________________________________________________________________________________________________________________

## 🔧 Dependencies


Install with:

```bash
# 1. Clone the repository
git clone https://github.com/ceccarellilab/immunokade.git
cd immunokade

# 2. Build the Conda/Mamba environment
mamba create -n immunokade python=3.8.15
mamba activate immunokade

# 3. Install PyTorch
# (We use version 1.12.1 for GPU because of our NVIDIA drivers, but you can use your own torch version.
# A GPU is not mandatory to run the model.)
pip install torch==1.12.1+cu113 -f https://download.pytorch.org/whl/cu113/torch_stable.html
python -c "import torch; print(torch.cuda.is_available())"

# 4. Install the other packages via pip
pip install numpy==1.22.3 pandas==1.5.2 fair-esm==2.0.0 tqdm

# (Optional) To run the notebook in "./data_output/":
# pip install scikit-learn==1.1.3 matplotlib==3.6.2 notebook
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

- `hla` column: HLA allele name, e.g. `HLA-A*02:01`. See `./src/hla_pocket.csv` for all the available HLAs. If your HLA is not in the dictionary, please add the 34 amino acids of its binding pocket to the dictionary.

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
| `-bs`, `--batch_size` | Number of samples loaded into the model per batch. Lower it if you run out of memory. | `2048` |

Examples:

```bash
# Run on the CPU (use this if no GPU is available)
python ./IK_pred.py ./data_input/example_viral_coded.csv -d cpu

# Run on a specific GPU (e.g. the number 2) with a lower batch size
python ./IK_pred.py ./data_input/example_viral_coded.csv -g 2 -bs 512
```


______________________________________________________________________________________________________________________________

## Data Availability
https://doi.org/10.5281/zenodo.21496931
