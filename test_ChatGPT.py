import openai
from tqdm import tqdm,trange
import json
import os
import argparse
import random

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Options')
    parser.add_argument("--start", type=int, default=0, help="idx")
    parser.add_argument("--idx", type=int, default=0, help="idx")
    parser.add_argument("--runid", type=int, default=0, help="idx")
    parser.add_argument("--seed", type=int, default=0, help="seed")
    parser.add_argument("--prompt_num", type=int, default=0, help="p_num")
    parser.add_argument("--nn", type=int, default=1, help="nn")
    parser.add_argument("--cate", type=int, default=0, help="cate")
    parser.add_argument("--temp", type=float, default=0, help="temp")
    parser.add_argument("--model", type=str, default="gpt3.5", help="model")
    parser.add_argument("--subset", type=str, default="test", help="subset")
    parser.add_argument("--store_dir", type=str, default="V_zero", help="store")
    parser.add_argument("--lidu", type=int, default=20, help="lidu")
    args = parser.parse_args()
    print(args.cate)
    print(args.model)
    openai.api_type = "azure"
    if args.model == "gpt3.5":
        openai.api_key = "please input your key here"
        openai.api_base = "https://PUSH-AIGC02-FC.openai.azure.com/"
        openai.api_version = "2023-03-15-preview"
        deployment_id="PUSH-AIGC02-FC"
    elif args.model == "gpt4":
        openai.api_key = "please input your key here"
        openai.api_base = "https://PUSH-AIGC02-FC.openai.azure.com/"
        openai.api_version = "2023-03-15-preview"
        deployment_id="gpt4"
    number = 50000
    nn = args.nn
    prompt_num = args.prompt_num
    seed = args.seed
    random.seed(seed)
    store_dir = args.store_dir
    os.makedirs("Completion/"+store_dir, exist_ok=True)
    os.makedirs("tag/"+store_dir, exist_ok=True)
    temp = args.temp
    file_name= "{}/".format(store_dir)+'{}_'.format(args.model)+"_"+str(nn)+"tem{}".format(temp)
    os.makedirs("Completion/"+file_name, exist_ok=True)
    os.makedirs("log", exist_ok=True)
    os.makedirs("tag/{}".format(file_name), exist_ok=True)

    lidu = args.lidu
    start_num = args.idx*lidu+args.start
    end_num = (1+args.idx)*lidu+args.start

    def read_json_files_in_directory(directory_path):
        json_data = {}

        # 遍历目录中的文件
        for filename in os.listdir(directory_path):
            if filename.endswith('.json'):  # 只处理 JSON 文件
                file_path = os.path.join(directory_path, filename)
                with open(file_path, 'r') as file:
                    try:
                        data = json.load(file)
                        # 在这里您可以对解析后的数据进行处理
                        json_data[filename.split(".json")[0]] = data
                    except json.JSONDecodeError as e:
                        print("Error decoding JSON:", e)

        return json_data


    if not os.path.exists("tag/{}/{}".format(file_name,args.idx)):
        if os.path.exists('{}/{}.jsonl'.format(file_name,args.idx)):
            os.remove('{}/{}.jsonl'.format(file_name,args.idx))
        dataset_directory = "./cognitive_v2"
        stages = os.listdir(dataset_directory)
        stage_data = []
        for i in stages:
            data = read_json_files_in_directory(dataset_directory + "/{}".format(i))
            for tem in data.keys():
                # if "2" not in tem:
                #     continue
                type = i+"-"+tem
                for t in data[tem]:
                    t["type"] = type
                    stage_data.append(t)
        data = stage_data
        task_prompts = [
            {
                "Q": 'Where is the capital of France?\nPlease choose one of the following options to answer the above question.\nOptions: A. Paris B. London C. Marid D. Berlin',
                "A": 'The answer is: \\boxed{A}'
                # "A": 'Paris is the capital of France because it has held this status for centuries and is the political, economic, cultural, and historical center of the country. The answer is: \\boxed{A}'
            },
            {
                "Q": 'which color is not a primary color?\nPlease choose one of the following options to answer the above question.\nOptions: A. Blue B. Red C. Yellow D. Green',
                "A": 'The answer is \\boxed{D}'
                # "A": 'The primary colors are red, blue, and yellow. The answer is \\boxed{D}'
            },
            {
                "Q": "Which sport is not included in the Summer Olympics?\nPlease choose one of the following options to answer the above question.\nOptions: A. Soccer B. Basketball C. Skiing D. Swimming",
                "A": 'The answer is \\boxed{C}'
                # "A": "The Summer Olympics primarily feature warm-weather and indoor sports, while skiing is a cold-weather sport that is part of the Winter Olympics. The answer is \\boxed{C}"
            },
            {
                "Q": 'What year did the Titanic sink?\nPlease choose one of the following options to answer the above question.\nOptions: A. 1909 B. 1912 C. 1915 D. 1920',
                "A": 'The answer is \\boxed{B}'
                # "A": 'The sinking of the Titanic occurred on April 15, 1912. It was a tragic event in which the ship struck an iceberg and sank during its maiden voyage from Southampton to New York City. The answer is \\boxed{B}'
            },
        ]
        cur = []
        for tem in task_prompts:
            cur.append({"role": "user", "content": "Question: "+tem["Q"]})
            cur.append({"role": "assistant", "content": "Answer: "+tem["A"]})

        # 单个种类
        if start_num<min(number,len(data)):
            with open('Completion/{}/{}.jsonl'.format(file_name,args.idx), 'w') as f:
                for i in trange(start_num,min(end_num,min(number,len(data)))):
                    flag = 0
                    example = data[i]
                    cans = ["A","B","C","D","E","F"]
                    options = ""
                    for ii in range(len(example["candidates"])):
                        options+=" "+cans[ii]+". "+example["candidates"][ii]
                    Q = "Question: " + example['question']+"\nOptions:"+options
                    # mes = [{"role": "system", "content": "You are a helpful assistant. Think the question step by step and select only one choice from the Options. End up your answer with the template 'The answer is \\boxed{your option}'."}]+ cur + [{"role": "user", "content": Q}]
                    mes = [{"role": "system",
                            "content": "You are a helpful assistant. Give your answer to the question strictly with the template 'The answer is \\boxed{your option}'."}] + cur + [
                              {"role": "user", "content": Q}]

                    while True:
                        try:
                                response1 = openai.ChatCompletion.create(
                                    engine=deployment_id,
                                    # model="gpt-4",
                                    messages=mes,
                                    temperature=temp,
                                    n=nn,
                                )
                                flag = 1
                        except openai.error.InvalidRequestError as e:
                            flag = 2
                        except Exception as e:
                                flag = 0
                        if flag == 1:
                                generated_answers = response1['choices']

                                if nn > 1:
                                    answer= []
                                    for tem in generated_answers:
                                        if 'content' in tem['message'].keys():
                                            answer.append(tem['message']['content'])
                                        else:
                                            answer.append("")
                                    sample_dict = {"question": Q, "answer": example['answer'], "generated_answer": answer,"type":example['type'],"candidates":example['candidates']}
                                    f.write(json.dumps(sample_dict) + '\n')
                                    f.flush()
                                else:
                                    for x in generated_answers:
                                        try:
                                            answer = x['message']['content']
                                        except:
                                            answer = "No response"
                                        sample_dict = {"question": Q, "answer": example['answer'], "generated_answer": answer,"type":example['type'],"candidates":example['candidates']}
                                        f.write(json.dumps(sample_dict) + '\n')
                                        f.flush()
                                break
                        if flag==2:
                            break
                f.close()

            os.makedirs("tag/{}/{}".format(file_name,args.idx), exist_ok=True)
