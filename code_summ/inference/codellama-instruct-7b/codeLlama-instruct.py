# Load model directly
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import os
import json
import time
import logging

MODEL = "CodeLlama-7b-Instruct-hf"
TEMPORATURE = 0.0
device = "cuda"# if torch.cuda.is_available() else "cpu"

checkpoint = "codellama/CodeLlama-7b-Instruct-hf"
tokenizer = AutoTokenizer.from_pretrained(checkpoint)
model = AutoModelForCausalLM.from_pretrained(checkpoint,
                                             torch_dtype=torch.float16,
                                             low_cpu_mem_usage=True,
                                             trust_remote_code=True).to(device)
prompt_template = 'Please generate a short summarization for the following codes:\n<code>'
dataset_path = './code_summarization_dataset.jsonl'
output_path = './code_summarization_inference_codellamainstruct.jsonl'
log_path = './code_summarization_inference_codellamainstruct.log'
logging.basicConfig(filename=log_path, level=logging.INFO)
logging.info(f"Start inference with {MODEL} and temperature {TEMPORATURE}..")

def generate(model, prompt, TEMPORATURE):
    try:
        inputs = tokenizer(prompt, return_tensors="pt", add_special_tokens=False).to(device)
        output = model.generate(
            inputs["input_ids"],
            max_new_tokens=4096,
            do_sample=False,
            # top_p=0.9,
            temperature=TEMPORATURE,
            pad_token_id=tokenizer.eos_token_id
        )
        output = tokenizer.decode(output[0].to("cpu"))
        summarization = output.split('[/INST]')[-1].replace('</s>','')
    except Exception as e:
        summarization = ''
        raise Exception(e)
    finally:
        # print(summarization)
        return summarization

with open(output_path, 'w') as f:
    f.write('')
with open(dataset_path) as f:
    for line in f:
        data = json.loads(line)
        code = data['code']
        prompt = prompt_template.replace('<code>', code.strip())
        prompt = f"<s>[INST] {prompt.strip()} [/INST]"
        try:
            code_sum_candidate = generate(model, prompt, TEMPORATURE)
        except Exception as e:
            print(e)
            logging.error(f"Error happened at {data['lang']}:{data['task_name']}. {e}")
            code_sum_groundtruth = ""
        data['code_sum_candidate'] = code_sum_candidate
        with open(output_path, 'a') as f:
            json.dump(data, f)
            f.write('\n')
    logging.info(f"Finished inference with {MODEL} and temperature {TEMPORATURE}.")
