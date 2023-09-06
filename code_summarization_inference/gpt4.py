import json
from multiprocessing import Pool
from tqdm import tqdm
import openai
import logging



openai.api_key = input("Enter your OpenAI API key: ")
# MAX_TOKENS = 8000
TEMPORATURE = 0
MODEL = "gpt-4"
prompt_template = "Please generate a short summarization for the following codes:\n<code>"

dataset_path = './code_summarization_dataset.jsonl'
output_path = './code_summarization_inference_gpt4.jsonl'
log_path = './code_summarization_inference_gpt4.log'
logging.basicConfig(filename=log_path, level=logging.INFO)
logging.info(f"Start inference with {MODEL} and temperature {TEMPORATURE}.")

def generate(prompt, max_tokens=256, temperature=0.0, model="gpt-3.5-turbo"):
    if model in ["gpt-3.5-turbo", "gpt-4"]:
        params = {
            "model": model,
            # "max_tokens": max_tokens,
            "temperature": temperature,
            "messages": [{"role": "user", "content": prompt}]
        }
        for retry in range(3):
            err_info = []
            try:
                return openai.ChatCompletion.create(**params)["choices"][0]["message"]["content"]
            except Exception as e:
                err_info.append(e)
        raise Exception(f"Failed to generate with {model} after 3 retries. Error info: {err_info}")
    else:
        raise Exception(f"Unsupported model: {model}")

with open(output_path, 'a') as f:
    f.write('')
with open(dataset_path) as f:
    for line in f:
        data = json.loads(line)
        code = data['code']
        prompt = prompt_template.replace('<code>', code.strip())
        try:
            code_sum_groundtruth = generate(prompt, temperature=TEMPORATURE, model=MODEL)
        except Exception as e:
            print(e)
            logging.error(f"Error happened at {data['lang']}:{data['task_name']}. {e}")
            code_sum_groundtruth = ""
        data['code_sum_candidate'] = code_sum_groundtruth
        with open(output_path, 'a') as f:
            json.dump(data, f)
            f.write('\n')
    logging.info(f"Finished inference with {MODEL} and temperature {TEMPORATURE}.")
