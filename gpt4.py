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


openai.api_key = input("Enter your OpenAI API key: ")


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
