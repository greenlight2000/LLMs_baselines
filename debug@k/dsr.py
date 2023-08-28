import json 
def main():
    contents = []
    acc = 0
    with open("final/final.json", 'r',encoding = 'utf-8') as f:
                for i in f.readlines():
                    content = json.loads(i)
                    contents.append(content)
                    if(content['label'] == 1):
                            acc = acc + 1
    f.close()
    print("acc :",acc/len(contents))
if __name__ == '__main__':
    main()