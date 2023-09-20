# Llama 2-70b
1. `cd inference-pipeline`
2. `pip install -r requirements.txt`
3. `python scripts/eval_llama2.py --checkpoint {absolute_path_to_your_Llama2_dir} --data_load_name code_summarization_dataset_with_gt.jsonl --result_save_name code_summ_inference_llama2.jsonl --log_file_name code_summ_inference_llama2.log`
4. logs will be generated under logs folder, and inference results will be genreared under results folder