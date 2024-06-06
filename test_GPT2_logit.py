import json
import os
from copy import deepcopy
from tqdm import tqdm
from transformers import pipeline, set_seed
import torch
import numpy as np
import warnings
from transformers import GPT2Tokenizer, GPT2LMHeadModel
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
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    cans = ['gpt2', 'gpt2-medium', 'gpt2-large', 'gpt2-xl']
    dataset_directory = "./data"
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
        tokenizer = GPT2Tokenizer.from_pretrained(can)
        model = GPT2LMHeadModel.from_pretrained(can)
        model = model.to(device)
        for stage in stage_data.keys():
            for data in stage_data[stage].keys():
                sub_data = stage_data[stage][data]
                print(f"testing stage:{stage} task:{data}")
                for i in tqdm(range(len(sub_data))):
                    question = sub_data[i]["question"]
                    candidates = sub_data[i]["candidates"]
                    choices = candidates_to_choices(candidates)
                    answer = answer_map[sub_data[i]["answer"]]
                    scores = []
                    hint = "The answer is: "
                    for j in range(len(candidates)):
                        input = question.strip() + "\n" + hint + candidates[j]
                    # print(input)
                        encoded_input = tokenizer.encode(input, add_special_tokens=False, return_tensors='pt')
                        predict = model(encoded_input.to(device), labels=encoded_input.to(device))
                   
                        predictions = predict[0]
                        score = np.exp(predictions.cpu().detach().numpy())
                        scores.append(score)
                    #print("score:", score)
                    #log_probs = torch.nn.functional.log_softmax(predictions, dim=-1)
                    #print(log_probs)
                    # seq_log_probs = torch.sum(torch.gather(log_probs, 1, input_ids), dim=1)
                    # print(seq_log_prob)
                    
                    # print(predict)
                    # predict = generator(input, max_length=1024, num_return_sequences=1)
                    result[stage][data][i]["answer"] = answer
                    # for item in predict:
                    #    item["generated_text"] = item["generated_text"].replace(input, "")
                    print(scores)
                    print(answer_map[scores.index(min(scores))])
                    result[stage][data][i]["predict"] = answer_map[scores.index(min(scores))]
        result_path = './result/'+can
        if not os.path.exists(result_path):
            os.makedirs(result_path, exist_ok=True)
        with open(result_path+"/result.json", "w") as f:
            json.dump(result, f, indent="\t")
        
    print("done")
