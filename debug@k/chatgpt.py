def process_content_keys(key_source):
    if key_source == 'VB':
        key_source = 'Visual Basic'
    return key_source
def prepare_prompt_cot1(file_path):
    texts = []
    targets = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for i in f.readlines():
            content = json.loads(i)
            target = content["output"]
            key_source = list(content.keys())[3]
            source = content[key_source]
            key_source = process_content_keys(list(content.keys())[3])
            key_intro = list(content.keys())[4]
            intro = content[key_intro]
            text = f"Function description:{intro}\nPlease translate into Python code according to the following {key_source} code and its functional description:{source}\nDo not return anything including notes and the like except for one translated Python code."
            print(text)
            texts.append(text)
            targets.append(target)
    return texts,targets
def prepare_prompt(file_path,type):
    examples=[]
    with open("example.json", 'r', encoding='utf-8') as f_new:
                for z in f_new.readlines():
                  example = json.loads(z)
                  examples.append(example)
                  
    f_new.close()
    texts = []
    targets = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for i in f.readlines():
            content = json.loads(i)
            target = content["output"]
            key_source = list(content.keys())[3]
            source = content[key_source]
            key_source = process_content_keys(list(content.keys())[3])
            if(type == "0shot_1"):
                text = f"Translate {key_source} to Python:{source}\nDo not return anything including notes and the like except for one translated Python code."
            elif(type == "0shot_2" or type == "0shot_3" or type == "0shot_4" or type == "0shot_5"):
                text = f"Please provide the Python translation for the following {key_source} code:\n{source}\nDo not return anything including notes and the like except for one translated Python code."
            elif(type == "0shot_6"):               
                text = f"Please translate the following {key_source} code into Python code:{source}\nDo not return anything including notes and the like except for one translated Python code."
            elif(type == "0shot_7"):
                text = f"Translating {key_source} to Python ensures that Python code can be compiled:{source}\nDo not return anything including notes and the like except for one translated Python code."
            elif(type == "0shot_8"):
                text = f"Can you rewrite this {key_source} code in Python? {source}"
            elif(type == "1shot_1"):
                text = '''
                        Here is an example of a translation from Java to Python.
                        "Java": "import java.util.ArrayList;\nimport java.util.Arrays;\nimport java.util.LinkedList;\nimport java.util.List;\nimport java.util.Queue;\n\npublic class WordBreak {\n\n public static void main(String[] args) {\n List<String> dict = Arrays.asList(\"a\", \"aa\", \"b\", \"ab\", \"aab\");\n for ( String testString : Arrays.asList(\"aab\", \"aa b\") ) {\n List<List<String>> matches = wordBreak(testString, dict);\n System.out.printf(\"String = %s, Dictionary = %s. Solutions = %d:%n\", testString, dict, matches.size());\n for ( List<String> match : matches ) {\n System.out.printf(\" Word Break = %s%n\", match);\n }\n System.out.printf(\"%n\");\n }\n dict = Arrays.asList(\"abc\", \"a\", \"ac\", \"b\", \"c\", \"cb\", \"d\");\n for ( String testString : Arrays.asList(\"abcd\", \"abbc\", \"abcbcd\", \"acdbc\", \"abcdd\") ) {\n List<List<String>> matches = wordBreak(testString, dict);\n System.out.printf(\"String = %s, Dictionary = %s. Solutions = %d:%n\", testString, dict, matches.size());\n for ( List<String> match : matches ) {\n System.out.printf(\" Word Break = %s%n\", match);\n }\n System.out.printf(\"%n\");\n }\n }\n \n private static List<List<String>> wordBreak(String s, List<String> dictionary) {\n List<List<String>> matches = new ArrayList<>();\n Queue<Node> queue = new LinkedList<>();\n queue.add(new Node(s));\n while ( ! queue.isEmpty() ) {\n Node node = queue.remove();\n \n if ( node.val.length() == 0 ) {\n matches.add(node.parsed);\n }\n else {\n for ( String word : dictionary ) {\n \n if ( node.val.startsWith(word) ) {\n String valNew = node.val.substring(word.length(), node.val.length());\n List<String> parsedNew = new ArrayList<>();\n parsedNew.addAll(node.parsed);\n parsedNew.add(word);\n queue.add(new Node(valNew, parsedNew));\n }\n }\n }\n }\n return matches;\n }\n \n private static class Node {\n private String val; \n private List<String> parsed; \n public Node(String initial) {\n val = initial;\n parsed = new ArrayList<>();\n }\n public Node(String s, List<String> p) {\n val = s;\n parsed = p;\n }\n }\n\n}\n", "Python": "from itertools import (chain)\n\n\n\ndef stringParse(lexicon):\n \n return lambda s: Node(s)(\n tokenTrees(lexicon)(s)\n )\n\n\n\ndef tokenTrees(wds):\n \n def go(s):\n return [Node(s)([])] if s in wds else (\n concatMap(nxt(s))(wds)\n )\n\n def nxt(s):\n return lambda w: parse(\n w, go(s[len(w):])\n ) if s.startswith(w) else []\n\n def parse(w, xs):\n return [Node(w)(xs)] if xs else xs\n\n return lambda s: go(s)\n\n\n\ndef showParse(tree):\n \n def showTokens(x):\n xs = x['nest']\n return ' ' + x['root'] + (showTokens(xs[0]) if xs else '')\n parses = tree['nest']\n return tree['root'] + ':\\n' + (\n '\\n'.join(\n map(showTokens, parses)\n ) if parses else ' ( Not parseable in terms of these words )'\n )\n\n\n\n\ndef main():\n \n\n lexicon = 'a bc abc cd b'.split()\n testSamples = 'abcd abbc abcbcd acdbc abcdd'.split()\n\n print(unlines(\n map(\n showParse,\n map(\n stringParse(lexicon),\n testSamples\n )\n )\n ))\n\n\n\n\n\ndef Node(v):\n \n return lambda xs: {'type': 'Node', 'root': v, 'nest': xs}\n\n\n\ndef concatMap(f):\n \n return lambda xs: list(\n chain.from_iterable(map(f, xs))\n )\n\n\n\ndef unlines(xs):\n \n return '\\n'.join(xs)\n\n\n\nif __name__ == '__main__':\n main()\n"
                       '''+ f"Please imitate this example to translate following code from {key_source} to Python:{source}\nDo not return anything including notes and the like except for one translated Python code."
            elif(type == "1shot_2"):
                for j in range(len(examples)):
                    example = examples[j]
                    example_source = list(example.keys())[1]
                    example_source = process_content_keys(example_source)
                    example_target = list(example.keys())[2]
                    if(example_source==key_source and example_target=="Python"):
                            t = str(example)
                            break
                text = f'''
                            Here is an example of a translation from {key_source} to Python.
                        '''+ t+f"\nPlease imitate this example to translate following code from {key_source} to Python:{source}Do not return anything including notes and the like except for one translated Python code."
            elif(type == "1shot_3"):        
                text = '''
                        Here is an example of a translation from Go to C++. "Go": "package main\n\nimport (\n \"errors\"\n \"fmt\"\n \"log\"\n)\n\nvar (\n v1 = []int{1, 3, -5}\n v2 = []int{4, -2, -1}\n)\n\nfunc dot(x, y []int) (r int, err error) {\n if len(x) != len(y) {\n return 0, errors.New(\"incompatible lengths\")\n }\n for i, xi := range x {\n r += xi * y[i]\n }\n return\n}\n\nfunc main() {\n d, err := dot([]int{1, 3, -5}, []int{4, -2, -1})\n if err != nil {\n log.Fatal(err)\n }\n fmt.Println(d)\n}\n", "C++": "#include <iostream>\n#include <numeric>\n\nint main()\n{\n int a[] = { 1, 3, -5 };\n int b[] = { 4, -2, -1 };\n\n std::cout << std::inner_product(a, a + sizeof(a) / sizeof(a[0]), b, 0) << std::endl;\n\n return 0;\n}" 
                       '''+ f"Please imitate this example to translate following code from {key_source} to Python:{source}\nDo not return anything including notes and the like except for one translated Python code."
            elif(type == "cot_2"):
                text = f"First, understand the function of the following {key_source} code. Then, translate the {key_source} code into Python code while keeping the function unchanged.\n{source}\nDo not return anything including notes and the like except for one translated Python code."
            elif(type == "cot_3"):
                text = f"First, understand the functionality of the following {key_source} code and predict the compilation output. Then, translate the {key_source} code into Python while maintaining the same functionality, ensuring that the translated code can be successfully compiled.\n{source}\nDo not return anything including notes and the like except for one translated Python code."
            elif(type == "cot_4"):
                for j in range(len(examples)):
                    example = examples[j]
                    example_source = list(example.keys())[1]
                    example_source = process_content_keys(example_source)
                    example_target = list(example.keys())[2]
                    if(example_source==key_source and example_target=="Python"):
                            t = str(example)
                            break
                text = f'''
                        First, learn how to translate {key_source} code to Python based on the example, '''+t +f'''. Then, understand the functionality of the following {key_source} code and predict the compilation output, 
                        {key_source}: {source}. Finally, translate the {key_source} code into Python while maintaining the same functionality, ensuring that the translated code can be successfully compiled.
                        '''+ f"Do not return anything including notes and the like except for one translated Python code."

            print(text)    
            texts.append(text)
            targets.append(target)
    return texts,targets

def chatgpt(text='',type='',i=0,):
    if(type == "0shot_3" or type == "0shot_4" or type == "0shot_5"):
        while True: 
            try:
                key_sources=[]
                with open("new_all.json", 'r', encoding='utf-8') as f:
                    for j in f.readlines():
                        content = json.loads(j)
                        key_source = list(content.keys())[3]
                        key_sources.append(key_source)
                f.close()
                key_source = key_sources[i]
                if(type == "0shot_3"):
                    text_system = f"You are a code translation system that specializes in {key_source} and Python programming languages."
                elif(type == "0shot_4"):
                    text_system = "You are a programmer proficient in multiple programming languages."
                elif(type == "0shot_5"):
                    text_system = f"You are a programmer proficient in {key_source} and Python programming languages."                
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    temperature = 0,
                    top_p=0,
                    messages=[
                        {"role": "system", "content": text_system},
                        {"role": "user", "content": text},
                    ]
                )
                resText = response['choices'][0]['message']['content']
                print(resText)
                return resText
            except Exception as e:
                print("An error occurred: ", str(e))
                print("Sleeping for 10 seconds before retrying...")
                time.sleep(20)  

    else:    
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
                print(resText)
                return resText
            except Exception as e:
                print("An error occurred: ", str(e))
                print("Sleeping for 10 seconds before retrying...")
                time.sleep(20)  

import openai
import json
import time

def main():
    
    import argparse
    parser = argparse.ArgumentParser(description='Get py file.')
    parser.add_argument('--key', '-key',help="Key of chatgpt.")
    parser.add_argument('--type', '-type',help="Experiment type.")

    args = parser.parse_args()

    openai.api_key = args.key
    if(args.type == "cot_1"):
        texts,targets = prepare_prompt_cot1("data_intro.json")
    else:
        texts,targets = prepare_prompt("new_all.json",args.type)
        
    restexts = [chatgpt(text,args.type, i) for i, text in enumerate(texts)]


    for j, (restext) in enumerate(restexts):
        with open(f"output/output{j}.py", "w", encoding="utf-8") as f:
            f.write(restext)
if __name__ == '__main__':
    main()