#!/bin/bash

#*******************Use them only the first time.************************

CONDA_BASE=$(conda info --base)

conda create -n perl_envss python=3.8 -y

. $CONDA_BASE/etc/profile.d/conda.sh && conda activate perl_envss && conda install -c conda-forge perl -y

$CONDA_BASE/envs/perl_envss/bin/perl -v   # Print the perl version information and check if the installation is successful.

#*******************Use them only the first time.************************


$CONDA_BASE/envs/perl_envss/bin/python run_perl_scripts.py --input_txt /root/autodl-tmp/perl.txt --output_folder /root/autodl-tmp/perl --output_txt /root/autodl-tmp/output_results.txt


