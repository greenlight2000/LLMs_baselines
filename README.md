# LLMs_baselines

The LLM baselines we need to use will be provided here.

For open source CLM, we leverage the instruction-tuned checkpoints provided by [Hugging Face](https://huggingface.co/) to implement our experiments across various tasks.

## CodeLlama(instruction-tuned) 7b

[Prerequisite](https://huggingface.co/codellama/CodeLlama-7b-hf):
cuda, torch, transformers, accelerate

Specially, by the time we conduct the experiments(2023.08-2023.09), instruction-tuned CodeLlama requires installing transformers from main repository:
```
pip install git+https://github.com/huggingface/transformers.git@main accelerate
```
a demo is given in [here](./hf_baseline_demos/codellama-instruct.py)

## InstructionCodeT5+ 16b

[Prerequisite](https://huggingface.co/Salesforce/instructcodet5p-16b):
cuda, torch, transformers, accelerate

a demo is given in [here](./hf_baseline_demos/instructCodeT5+.py)