def chatgpt(text=''):
    while True:
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                temperature = 0,
                top_p=0,
                messages=[
                    {"role": "user", "content": text},
                ]
            )
            resText = response['choices'][0]['message']['content']
            return resText
        except Exception as e:
            print("An error occurred: ", str(e))
            print("Sleeping for 10 seconds before retrying...")
            time.sleep(20)  # Wait for 10 seconds

import openai
import json

def main():
    import argparse
    parser = argparse.ArgumentParser(description='Get py file.')
    parser.add_argument('--key', '-key',help="Key of chatgpt.")

    args = parser.parse_args()

    openai.api_key = args.key


    contents = []
    with open("final/final.json", 'r',encoding = 'utf-8') as f:
                for i in f.readlines():
                    content = json.loads(i)
                    contents.append(content)
    f.close()

    for j in range(len(contents)):
        content = contents[j]
        python_code = content["Python"]
        label = content["label"]
        if(label==1):
            with open(f"output/output{j}.py", "w", encoding="utf-8") as f:
                f.write(python_code)
        else:
            key_source = list(content.keys())[4]
            source = content[key_source]
            error = content['output']
            text = f"Translate {key_source} to Python :{source}.\n\nChatGPT:{python_code}.\n\nUser: The above python code compiles with the following errors, please correct them.{error}"
            code = chatgpt(text)
            print(text)
            with open(f"debug/output{j}.py", "w", encoding="utf-8") as f:
                f.write(code)
if __name__ == '__main__':
    main()