# Data
```code_summarization_dataset_with_gt.jsonl``` 是 code summarizaiton的数据集。里面每一行是一个某道编程题的题解。

模型推理和评估只需要关注里面几个字段：
- 题解的代码"```code```" （用于推理）, 
- 代码总结的参考“```code_sum_groundtruth```” （用于评估计算相似度）, 
- 使用的编程语言"```lang```", 代码行数"```LOC```" (用于统计分析，如分类计算相似度)

# Inference
推理代码参考codellama-instruct.py, palm.py, gpt4.py。只需要修改开头的配置信息在文件里写死（如checkpoint,tokenizer,model,outputpath等），然后根据每个模型的api修改“```generate()```”函数即可，剩下的代码都可以重用。

代码会在```dataset_path```（数据集路径）进行推理在原文件的基础上添加一个新字段```"code_sum_candidate"```，并将其结果写入```output_path```文件。该文件可以直接用于```../evaluate/evaluate_model.py```进行评估计算指标。