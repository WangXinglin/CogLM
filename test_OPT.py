import json
import os
from copy import deepcopy
from tqdm import tqdm
from transformers import pipeline, set_seed
import torch
import warnings
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
        out_str += answer_map[i] + "." + choices[i] + " "
    return "Options: " + out_str.strip()+"\n"

def data_vadality_check(stage_data):
    for i in range(len(sub_data)):
                question = sub_data[i]["question"]
                candidates = sub_data[i]["candidates"]
                choices = candidates_to_choices(candidates)
                answer = answer_map[sub_data[i]["answer"]]
                hint = "The answer is: "
                input = question + choices + hint

    print("data validation check pass !!!")

if __name__ == "__main__":
    cans = ['opt-125m', 'opt-1.3b', 'opt-2.7b', 'opt-6.7b']
    dataset_directory = "./dataset"
    stages = os.listdir(dataset_directory)
    stage_data = {}
    for i in stages:
        data = read_json_files_in_directory(dataset_directory + "/{}".format(i))
        stage_data[i] = data

    answer_map = {0:"A", 1:"B", 2:"C", 3:"D", 4:"E", 5:"F"}
    result = deepcopy(stage_data)
    # data_vadality_check(stage_data)

    ICT = ["Where is the capital of France?\nPlease choose one of the following options to answer the above question.\nOptions: A. Paris B. London C. Marid D. Berlin\nThe answer is: A\n\n","which color is not a primary color?\nPlease choose one of the following options to answer the above question.\nOptions: A. Blue B. Red C. Yellow D. Green\nThe answer is: D\n\n","Which sport is not included in the Summer Olympics?\nPlease choose one of the following options to answer the above question.\nOptions: A. Soccer B. Basketball C. Skiing D. Swimming\nThe answer is: C\n\n","What year did the Titanic sink?\nPlease choose one of the following options to answer the above question.\nOptions: A. 1909 B. 1912 C. 1915 D. 1920\nThe answer is: B\n\n" ]
    ict = ""
    for item in ICT[:0]:
        ict += item

    for can in cans:
        print("#########################testing {}###########################".format(can))
        result = deepcopy(stage_data)
        generator = pipeline('text-generation', model=can, device=torch.device(0))
        set_seed(42)
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
                    input = ict + question.strip() + "\n" + "Please choose one of the following options to answer the above question.\n" + choices + hint
                    
                    predict = generator(input, max_length=1024, num_return_sequences=1)
                    result[stage][data][i]["answer"] = answer
                    for item in predict:
                        item["generated_text"] = item["generated_text"].replace(input, "")
                    result[stage][data][i]["predict"] = predict
        result_path = './result/'+can
        if not os.path.exists(result_path):
            os.makedirs(result_path)
        with open(result_path+"/result.json", "w") as f:
            json.dump(result, f, indent="\t")
        
    print("done")
