# fs_snakemake_demo

This is a simple example of using snakemake with finestructure.

You need [finestructure](https://github.com/danjlawson/finestructure4) and [snakemake](https://snakemake.readthedocs.io/en/stable/getting_started/installation.html).

It is not ready for general usage and significant investment is required to make it work for you in reality.

This is how you run it, once you have installed snakemake as recommended:
```{bash}
conda activate snakemake
snakemake -c1 -s fs_snakemake.py
```
It runs the example1 from the  [finestructure](https://github.com/danjlawson/finestructure4) repository.
