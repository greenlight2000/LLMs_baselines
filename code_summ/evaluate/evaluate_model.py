import argparse
import multiprocessing
import json
from evaluate import load
from datasets import load_dataset
from nltk.translate.meteor_score import meteor_score
import nltk
nltk.download('wordnet')# for meteor calculation
nltk.download('punkt')# for word tokenizer
import logging
import datetime
import os
from pathlib import Path

import json
def cal_bleu(modelname, dataset_path, pred_field, ref_field, output_dir):
    print(output_dir)
    try:
        dataset = load_dataset("json", data_files=dataset_path, split="train")
        dataset = dataset.map(lambda examples: {ref_field: [examples[ref_field]], pred_field: examples[pred_field]})
        bleu = load('bleu')
        bleu_result = bleu.compute(predictions=dataset[pred_field], references=dataset[ref_field])
    except Exception as e:
        bleu_result = {"error": str(e)}
    finally:
        with open(output_dir / Path(f"{modelname}_bleu_result.json"), "w") as f:
            json.dump(bleu_result, f)
        return bleu_result
def cal_rouge(modelname, dataset_path, pred_field, ref_field, output_dir):
    try:
        dataset = load_dataset("json", data_files=dataset_path, split="train")
        rouge = load('rouge')
        rouge_result = rouge.compute(predictions=dataset[pred_field], references=dataset[ref_field])
    except Exception as e:
        rouge_result = {"error": str(e)}
    finally:
        with open(output_dir / Path(f"{modelname}_rouge_result.json"), "w") as f:
            json.dump(rouge_result, f)
        return rouge_result
def cal_bertscore(modelname, dataset_path, pred_field, ref_field, output_dir):
    try:
        dataset = load_dataset("json", data_files=dataset_path, split="train")
        bertscore = load("bertscore")
        bertscore_result = bertscore.compute(lang="en", predictions=dataset[pred_field], references=dataset[ref_field])
    except Exception as e:
        bertscore_result = {"error": str(e)}
    finally:
        with open(output_dir / Path(f"{modelname}_bertscore_result.json"), "w") as f:
            json.dump(bertscore_result, f)
        return bertscore_result
def cal_meteor(modelname, dataset_path, pred_field, ref_field, output_dir):
    try:
        dataset = load_dataset("json", data_files=dataset_path, split="train")
        dataset = dataset.map(lambda examples: {ref_field: nltk.word_tokenize(examples[ref_field]), pred_field: nltk.word_tokenize(examples[pred_field])})# pre tokenize words and symbols
        meteor_results = []
        for d in dataset:
            score = meteor_score(references=[d[ref_field]], hypothesis=d[pred_field])
            meteor_results.append(score)
        results = {"avg": sum(meteor_results)/len(meteor_results), "meteor_results": meteor_results}
    except Exception as e:
        results = {"error": str(e)}
    finally:
        with open(output_dir / Path(f"{modelname}_meteor_result.json"), "w") as f:
            json.dump(results, f)
        return results

def main():
    now = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    cur_dir = Path(__file__).parent
    output_dir = cur_dir / Path(f"eval_{args.modelname}_{now}")
    if not output_dir.exists():
        output_dir.mkdir()
    logging.basicConfig(filename=output_dir / Path("main.log"), level=logging.INFO)
    logger = logging.getLogger(__name__)#__name__是当前模块名
    logger.info(f"Start evaluation for {args.modelname} at {args.dataset_path}")

    with multiprocessing.Pool(4) as pool:
        # 开一个进程计算出bleu直接把结果写入文件
        bleu_proc = pool.apply_async(cal_bleu, args=(args.modelname, args.dataset_path, args.pred_field, args.ref_field, output_dir))
        # 开一个进程计算出rouge直接把结果写入文件
        rouge_proc = pool.apply_async(cal_rouge, args=(args.modelname, args.dataset_path, args.pred_field, args.ref_field, output_dir))
        # 开一个进程计算出bertscore直接把结果写入文件
        bertscore_proc = pool.apply_async(cal_bertscore, args=(args.modelname, args.dataset_path, args.pred_field, args.ref_field, output_dir))
        # 开一个进程计算出meteor直接把结果写入文件
        meteor_proc = pool.apply_async(cal_meteor, args=(args.modelname, args.dataset_path, args.pred_field, args.ref_field, output_dir))
        # 等待所有进程结束
        pool.close()
        pool.join()
        # 读取所有进程的结果
        bleu_result = bleu_proc.get()
        rouge_result = rouge_proc.get()
        bertscore_result = bertscore_proc.get()
        meteor_result = meteor_proc.get()
        # 计算总结果
        logger.info("Evaluation finished, checkout the results in the output directory")
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--modelname", type=str, default="", help="the name of the model to be evaluated(used as the prefix of the output file)")
    parser.add_argument("--dataset_path", type=str, default="", help="the absolute path to the dataset that is to be evaluated")
    parser.add_argument("--pred_field", type=str, default="code_sum_candidate")
    parser.add_argument("--ref_field", type=str, default="code_sum_groundtruth")
    args = parser.parse_args()
    main()