import json
import os
from copy import deepcopy
from tqdm import tqdm
from transformers import pipeline, set_seed
import torch
import warnings
import fire
from llama import Llama
from typing import List
# warnings.filterwarnings('ignore')

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

def candidates_to_choices(choices):
    answer_map = {0: "A", 1: "B", 2: "C", 3: "D", 4: "E", 5: "F"}
    out_str = ""
    for i in range(len(choices)):
        out_str += answer_map[i] + "." + choices[i].split(".")[0] + ". "
    return  out_str.strip()+" "

def data_vadality_check(stage_data):
    for i in range(len(sub_data)):
                question = sub_data[i]["question"]
                candidates = sub_data[i]["candidates"]
                choices = candidates_to_choices(candidates)
                answer = answer_map[sub_data[i]["answer"]]
                hint = "The answer is: "
                input = question + choices + hint

    print("data validation check pass !!!")

def main(
    ckpt_dir: str,
    tokenizer_path:str,
    temperature: float = 0,
    top_p: float = 0.9,
    max_seq_len: int = 128,
    max_gen_len: int = 64,
    max_batch_size: int = 4,
):
    
    generator = Llama.build(
        ckpt_dir=ckpt_dir,
        tokenizer_path=tokenizer_path,
        max_seq_len=max_seq_len,
        max_batch_size=max_batch_size,
    )
    dataset_directory = "./dataset"
    stages = os.listdir(dataset_directory)
    stage_data = {}
    for i in stages:
        data = read_json_files_in_directory(dataset_directory + "/{}".format(i))
        stage_data[i] = data

    answer_map = {0:"A", 1:"B", 2:"C", 3:"D", 4:"E", 5:"F"}
    result = deepcopy(stage_data)
    # data_vadality_check(stage_data)
   
    prompts: List[str] = ["I believe the meaning of life is", "Simply put, the theory of relativity states that "]
    icts: List[str] = ["Where is the capital of France?\nPlease choose one of the following options to answer the above question:A. Paris B. London C. Marid D. Berlin\nThe answer is: A. Paris\n","which color is not a primary color?\nPlease choose one of the following options to answer the above question: A. Blue B. Red C. Yellow D. Green\nThe answer is: D. Green\n","Which sport is not included in the Summer Olympics?\nPlease choose one of the following options to answer the above question: A. Soccer B. Basketball C. Skiing D. Swimming\nThe answer is: C\n\n","What year did the Titanic sink?\nPlease choose one of the following options to answer the above question: A. 1909 B. 1912 C. 1915 D. 1920\nThe answer is: B\n\n" ]
    
    ict = ""
    for item in icts[:1]:
        ict += item
    print("#########################testing {}###########################".format(ckpt_dir.split("/")[-1]))
    result = deepcopy(stage_data)
    for stage in stage_data.keys():
        for data in stage_data[stage].keys():
            sub_data = stage_data[stage][data]
            print(f"testing stage:{stage} task:{data}")
            for i in tqdm(range(len(sub_data))):
                question = sub_data[i]["question"]
                candidates = sub_data[i]["candidates"]
                choices = candidates_to_choices(candidates)
                answer = answer_map[sub_data[i]["answer"]]
                hint = "The answer is: "
                input = [question.strip()  + " Please choose one of the following options to answer the above question: " + choices + hint]                
                print(input)
                predict = generator.text_completion(input, max_gen_len=max_gen_len, temperature=temperature, top_p=top_p, logprobs=True, echo=True)
                result[stage][data][i]["answer"] = answer
                print(predict)
                result[stage][data][i]["predict"] = predict[0]['generation']
    result_path = './result/'+ckpt_dir
    if not os.path.exists(result_path):
        os.makedirs(result_path)
    with open(result_path+"/result.json", "w") as f:
        json.dump(result, f, indent="\t")
        
    print("done")

if __name__ == "__main__":
    fire.Fire(main)
