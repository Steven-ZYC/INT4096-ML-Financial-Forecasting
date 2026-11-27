# Run the notebook with Miniconda (NVIDIA GPU)

Run these from the repository root. You need
[Miniconda](https://docs.conda.io/projects/miniconda/) and, for the GPU, a recent
NVIDIA driver.

```bash
conda create -n int4096 python=3.12 -y
conda activate int4096
pip install -r requirements.txt
pip install torch==2.9.1 --index-url https://download.pytorch.org/whl/cu130
python -c "import torch; print(torch.cuda.is_available(), torch.cuda.get_device_name(0))"
python scripts/execute_notebook.py
```

- The check on the fifth line should print `True` and the GPU name. `cu130` needs a
  driver for which `nvidia-smi` shows CUDA 13.0 or higher; with an older driver,
  replace `cu130` with `cu126`.
- The last line runs every cell and writes `INT4096_Final_Colab_executed.ipynb`
  (a few minutes). Submit it together with `INT4096_Final_Colab.ipynb`.
- Only the neural experiment (section 9) uses the GPU. The other models run on the CPU.

## Check the output

| Section | Look for |
|---|---|
| 1 | Your GPU name and `torch 2.9.1` with a CUDA build |
| 7 | `MATCH: all 20 experiments agree ...` (or the list of differences) |
| 9 | Neural accuracy now against the submitted values; they should agree with the report's wording |

## Working in Jupyter or VS Code instead

Select the `int4096` environment as the kernel. Save any run under a new file name:
the tests require `INT4096_Final_Colab.ipynb` to have no saved outputs. Each session
creates an `int4096_workspace_*` folder, which Git ignores.
