## Install the Delphi and Pascal languages execution environment.

```conda create -n delphi_pascal_env python=3.8```

```conda activate delphi_pascal_env```

```sudo apt update```

```sudo apt install fpc```

```fpc -v```

```sudo apt install lazarus```


## Execute Delphi and Pascal scripts.

```run_delphi_pascal_scripts.py --input_txt /root/autodl-tmp/delphi.txt --output_folder /root/autodl-tmp/delphi --output_txt /root/autodl-tmp/output_results.txt```
