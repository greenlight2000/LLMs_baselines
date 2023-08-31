#!/bin/bash

conda create -n myperl python=3.8 -y
source $(conda info --base)/etc/profile.d/conda.sh
conda activate myperl
conda install -c conda-forge perl -y

# Print the perl version information and check if the installation is successful.
perl -v

python run_perl_script.py --input_txt /path/to/source_code.txt --output_folder /path/to/output/folder --output_txt /path/to/output_results.txt
