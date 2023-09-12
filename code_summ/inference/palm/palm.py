# https://github.com/google/generative-ai-python/blob/v0.1.0/google/generativeai/__init__.py
# pip install google-generativeai
import json
from tqdm import tqdm
import logging
import google.generativeai as palm

palm.configure(api_key='AIzaSyCKgHPsJ6kyJa0BBsY2QTBWZVBJcZRi5fY', transport='rest')
prompt_template = "Please generate a short summarization for the following codes:\n<code>"

dataset_path = './code_summarization_dataset.jsonl'
output_path = './code_summarization_inference_palm.jsonl'
log_path = './code_summarization_inference_palm.log'
logging.basicConfig(filename=log_path, level=logging.INFO)
logging.info(f"Start inference with palm.")

with open(output_path, 'a') as f:
    f.write('')
with open(dataset_path) as f:
    for line in tqdm(f):
        data = json.loads(line)
        code = data['code']
        my_prompt = prompt_template.replace('<code>', code.strip())
        try:
            code_sum_groundtruth = palm.generate_text(prompt=my_prompt).result
        except Exception as e:
            print(e)
            logging.error(f"Error happened at {data['lang']}:{data['task_name']}. {e}")
            code_sum_groundtruth = ""
        data['code_sum_candidate'] = code_sum_groundtruth
        with open(output_path, 'a') as f:
            json.dump(data, f)
            f.write('\n')
    logging.info(f"Finished inference with palm.")
