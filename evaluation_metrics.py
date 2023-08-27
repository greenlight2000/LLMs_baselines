import evaluate

# please install corresponding packages according to debugging msg

bleu = evaluate.load('bleu')
rouge = evaluate.load('rouge')
bert_score = evaluate.load('bertscore')

# predictions: output of LLMs,
# reverences: ground truth

print(bleu.compute(predictions=base_ans, references=eval_set['chosen'].values))
print(rouge.compute(predictions=base_ans, references=eval_set['chosen'].values))
bertscore_result = bert_score.compute(predictions=decoded_preds, references=decoded_labels, lang="en")

