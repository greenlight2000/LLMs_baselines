import os
import json
import glob
import re
from multiprocessing import Pool
from tqdm import tqdm
import torch
import openai
import itertools
import random
import pandas as pd


openai.api_key = input("Enter your OpenAI API key: ")
MAX_TOKENS = 8000
TEMPORATURE = 0.3
MODEL = "gpt-4"
task_file = './task_selected_final.csv'
solution_path = './solutions/bytask/'

def generate(prompt, max_tokens=256, temperature=0.0, model="gpt-3.5-turbo"):
    if model in ["gpt-3.5-turbo", "gpt-4"]:
        params = {
            "model": model,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "messages": [{"role": "user", "content": prompt}]
        }
        for retry in range(3):
            try:
                return openai.ChatCompletion.create(**params)["choices"][0]["message"]["content"]
            except:
                pass
        raise Exception("Failed to generate")
    
    # For older models, use the completion API with max_tokens=1024
    params = {
        "model": model,
        "max_tokens": min(max_tokens, 1024),
        "temperature": temperature,
        "prompt": prompt
    }
    for retry in range(3):
        try:
            return openai.Completion.create(**params)["choices"][0]["text"]
        except:
            pass

#step1: 生成可复用的code summarization
task_selected = pd.read_csv(task_file)
code_summ_col = []
for index,row in task_selected.iterrows():
    task_name = row['task_name']
    description = row['task_description']
    prompt = f"""
        rearrange the programming task description text in ```{task_name}:{description}``` to generate corresponding code summarization. You should pretend that a piece of codes is written according to the task description and you are summarizing the functionality of the codes.
        The output should strictly capture the semantics details given in the text and be short. Code summarization: the following codes <output>
        """
    try:
        code_summ = generate(prompt, max_tokens=MAX_TOKENS, temperature=TEMPORATURE, model=MODEL)
    except Exception as e:
        print(e)
        code_summ = f"Exception:{e}"
    code_summ_col.append(code_summ)
task_selected.insert(5, 'code_summarization', code_summ_col)
task_selected.to_csv(task_file, index=False)

#step2: 对于solution中进一步给出了explanation的数据，为他们专门定制一个code summarization
task_selected = pd.read_csv(task_file)
task_json_files = os.listdir(solution_path)
for task_json_file in task_json_files:
    with open(f'{solution_path}{task_json_file}') as f:
        solutions = json.load(f)
        # 因为是bytask遍历的，所以这些信息在文件中是相同的
        task_name = solutions[0]['task_name']# 'Knapsack problem/0-1'
        task_append_info = task_selected[task_selected['task_name']==task_name].iloc[0]
        for s in solutions:
            task_explain = s['explain']
            if task_explain == "":
                code_sum_groundtruth = task_append_info['code_summarization']
            else:
                task_description = task_append_info['task_description']
                description = task_description+task_explain
                prompt = f"""
                rearrange the programming task description text in ```{task_name}:{description}``` to generate corresponding code summarization. You should pretend that a piece of codes is written according to the task description and you are summarizing the functionality of the codes.
                The output should strictly capture the semantics details given in the text and be short. Code summarization: the following codes <output>
                """
                try:
                    code_sum_groundtruth = generate(prompt, max_tokens=MAX_TOKENS, temperature=TEMPORATURE, model=MODEL)
                except Exception as e:
                    print(e)
                    code_sum_groundtruth = f"Exception:{e}"
            s['code_sum_groundtruth'] = code_sum_groundtruth
            # break
        with open(f'{solution_path}{task_json_file}', 'w') as f:
            json.dump(solutions, f)
