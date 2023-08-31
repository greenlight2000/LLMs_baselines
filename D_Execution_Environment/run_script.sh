#!/bin/bash

CONDA_BASE=$(conda info --base)

#*******************Use them only the first time.************************

conda create -n d_env python=3.8 -y

. $CONDA_BASE/etc/profile.d/conda.sh && conda activate d_env && curl -fsS https://dlang.org/install.sh | bash -s dmd

#*******************Use them only the first time.************************


source ~/dlang/dmd-2.105.0/activate

$CONDA_BASE/envs/perl_env/bin/python run_perl_scripts.py --input_txt /root/autodl-tmp/perl.txt --output_folder /root/autodl-tmp/perl --output_txt /root/autodl-tmp/output_results.txt

deactivate

