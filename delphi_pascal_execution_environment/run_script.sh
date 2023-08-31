#!/bin/bash

CONDA_BASE=$(conda info --base)

conda create -n delphi_pascal_env python=3.8 -y

. $CONDA_BASE/etc/profile.d/conda.sh && conda activate delphi_pascal_env

sudo apt update -y
sudo apt install fpc -y
fpc -v
sudo apt install lazarus -y
