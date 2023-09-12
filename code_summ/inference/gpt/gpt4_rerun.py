# References: https://github.com/openai/openai-cookbook/blob/main/examples/How_to_handle_rate_limits.ipynb
import json
from multiprocessing import Pool
from tqdm import tqdm
import openai
import logging
import datetime

""" 
gpt3.5的推理结果发现有很多地方没有生成成功, 报错事backoff“”, 这个文件是gpt4的修改版, 用于重跑推理。
- 设置了只会在dataset_path的基础上找到没有生成成功的数据进行重跑, 并输出到output_path
- 所以每次重跑的时候, 请修改dataset_path和output_path的文件名, 以免覆盖之前的结果
"""
openai.api_key = input("Enter your OpenAI API key: ") # 请修改该字段
# MAX_TOKENS = 8000
TEMPORATURE = 0.0
MODEL = "gpt-4"
prompt_template = "Please generate a short summarization for the following codes:\n<code>"

dataset_path = './code_summarization_dataset.jsonl' # 请修改该字段：在这个文件的基础上进行（新生成/补充生成）code summarization prediction
output_path = './code_summarization_inference_gpt4.jsonl' # 请修改该字段：生成的code summarization prediction会输出到这个文件
log_path = './code_summarization_inference_gpt4.log'


now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
logging.basicConfig(filename=log_path, level=logging.INFO)
logging.info(f"Start inference with {MODEL} and temperature {TEMPORATURE} at {now_time}.")

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

total_gen_cnt = 0
failed_gen_cnt = 0
with open(output_path, 'w') as f:
    f.write('')
with open(dataset_path) as f:
    for line in f:
        data = json.loads(line)
        # 如果之前已经生成成功了，就跳过
        if data['code_sum_candidate'] != "" and data['code_sum_candidate'] is not None:
            with open(output_path, 'a') as f:
                json.dump(data, f)
                f.write('\n')
            continue
        # 如果之前还没有（成功）生成，就在这里生成
        total_gen_cnt += 1
        code = data['code']
        prompt = prompt_template.replace('<code>', code.strip())
        try:
            code_sum_candidate = generate(prompt, temperature=TEMPORATURE, model=MODEL)
        except Exception as e:
            print(e)
            logging.error(f"Error happened at {data['lang']}:{data['task_name']}. {e}")
            code_sum_groundtruth = ""
            failed_gen_cnt += 1
        finally:
            data['code_sum_candidate'] = code_sum_candidate
            with open(output_path, 'a') as f:
                json.dump(data, f)
                f.write('\n')
now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
logging.info(f"Finished inference with {MODEL} and temperature {TEMPORATURE}.")
if failed_gen_cnt > 0:
    logging.info(f"Failed to generate {failed_gen_cnt} out of {total_gen_cnt} cases. Please configure the `dataset_path`,`output_path` files name, and rerun the script.")
else:
    logging.info(f"successfully generate all {total_gen_cnt} data")