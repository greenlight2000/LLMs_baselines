follow these steps to use GPT4 to inference on code summarization task
1. modify the openai API key in the gpt4.py file
2. cd to the ```code_summarization_inference``` directory
3. import related packages specified in generation.py and run ```python ./gpt4.py```

two files should be generated: (1)inference results: ```./code_summarization_inference_gpt4.jsonl``` and (2)running log: ```./code_summarization_inference_gpt4.log```

Notice: For gpt3.5 inference, just modify the MODEL variable to "gpt-3.5-turbo" in gpt4.py, and rename some output filenames, then you are all set. Run the same command as above