# Prequisite: 
评估前需要准备好一个模型的inference结果，需要是jsonl格式，且包含reference和prediction的内容，这两个内容在jsonl中的字段索引可以在指令的```--pred_field```和```--ref_field```中修改，模型是使用"code_sum_groundtruth"和"code_sum_candidate"。
# how to use

直接运行一下命令即可对模型进行评估。
```
nohup python ./evaluate.py \
--modelname {model name} \
--dataset_path {inference result in jsonl} \
--pred_field {prediction field name in jsonl} \
--ref_field {reference field name in jsonl} \
> eval.log 2>&1 &
```

建议后台运行，因为bertscore运行时间较久. 这个程序会为推理结果计算```BLEU-4```，```ROUGE```(四种都算，包括ROUGE-L), ```METEOR```(默认超参数), ```BERTSOCORE```，并将这些指标计算结果以json文件的形式存到```./eval_{modelname}/eval_{metric}_{timestamp}.json```的文件中。
