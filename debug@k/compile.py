def run_python_script(script_path):
    if not script_path:
        return "Please provide a valid Python script path."
    command = f"python {script_path}"
    k = 0
    try:
        
        start_time = time.time()
        process = subprocess.Popen(command, shell=True)
        while True:
            if  process.poll() is not None:
                output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, text=True)
                break

            elif time.time() - start_time > 20:  
                k=1
                process.terminate()
                output="timeout"
                break
            time.sleep(0.1)  
        
    except subprocess.CalledProcessError as e:
            k=1
            output = str(e.output)
    return output,k

def deal_code(code):
    code = re.sub(r'\n', ' ', code)
    code = re.sub(r'\s+', ' ', code)
    code = re.sub(r'^[\s\n]+|[\s\n]+$', '', code)
    return code
def save_result_to_json(data, file_path):
    with open(file_path, "a") as file:
        json.dump(data, file, ensure_ascii=False)
        file.write('\n')
        file.close()

import json
import time
import re
import subprocess

def main():
    u=0
    contents = []
    targets = []
    with open("new_all.json", 'r',encoding = 'utf-8') as f:
                for i in f.readlines():
                    content = json.loads(i)
                    contents.append(content)
                    targets.append(content["output"])
    f.close()
    for j in range(len(contents)):
        print(j)
        content = contents[j]
        key_source = list(content.keys())[3]
        source = content[key_source]
        target = deal_code(content["output"])
        output,k = run_python_script(f"output/output{j}.py")
        output = deal_code(output)

        with open(f"output/output{j}.py", "r", encoding="utf-8") as f:
            python_code = f.read()
        f.close()
        if(output==target):
          u=u+1
          dic = {'id':j, "label":1, "output":output,"Python":python_code,key_source:source}
        elif(k==0 and output!=target):
          dic = {'id':j, "label":0, "output":"The code compiles but the output is incorrect.","Python":python_code,key_source:source}
        else:
          if(len(output)>2000):
            output = output[:2000]
          dic = {'id':j, "label":0, "output":output,"Python":python_code,key_source:source}
        save_result_to_json(dic, "final/final.json")
if __name__ == '__main__':
    main()