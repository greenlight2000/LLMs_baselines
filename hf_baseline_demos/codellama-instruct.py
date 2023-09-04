from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
device = "cuda" if torch.cuda.is_available() else "cpu"

checkpoint = "codellama/CodeLlama-7b-Instruct-hf"
tokenizer = AutoTokenizer.from_pretrained(checkpoint)
model = AutoModelForCausalLM.from_pretrained(checkpoint,
                                             torch_dtype=torch.float16,
                                             low_cpu_mem_usage=True,
                                             trust_remote_code=True).to(device)
user_prompt = 'Please generate a short summarization for the following codes:\n<code>'

code = """
def print_hello_world():
    print('hello world')
"""
user_prompt = user_prompt.replace('<code>', code)
prompt = f"<s>[INST] {user_prompt.strip()} [/INST]"
inputs = tokenizer(prompt, return_tensors="pt", add_special_tokens=False).to(device)
output = model.generate(
    inputs["input_ids"],
    max_new_tokens=3000,
    do_sample=True,
    top_p=0.9,
    temperature=0.1,
)
output = tokenizer.decode(output[0].to("cpu"))
summarization = output.split('[/INST]')[-1]# generated content will follows the last '[/INST]' token
print(summarization)