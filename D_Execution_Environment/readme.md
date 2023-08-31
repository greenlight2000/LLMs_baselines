## Install the D language execution environment.

```conda create -n d_env python=3.8```
```conda activate d_env```
```curl -fsS https://dlang.org/install.sh | bash -s dmd```


## Activate the D language execution environment.
```source ~/dlang/dmd-2.105.0/activate```  # Please follow the previous step to install successfully and then prompted to check whether the version number is updated.

```run_perl_scripts.py --input_txt /root/autodl-tmp/perl.txt --output_folder /root/autodl-tmp/perl --output_txt /root/autodl-tmp/output_results.txt```

```deactivate```

