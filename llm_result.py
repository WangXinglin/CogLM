import json
import os
def read_json_files_in_directory(directory_path):
    json_data = {}

    for filename in os.listdir(directory_path):
        if filename.endswith('.json'):
            file_path = os.path.join(directory_path, filename)
            with open(file_path, 'r') as file:
                try:
                    data = json.load(file)
                    json_data = data
                except json.JSONDecodeError as e:
                    print("Error decoding JSON:", e)

    return json_data

if __name__ == "__main__":
    path = "./result"
    cans = ["gpt2", "gpt2-medium", "gpt2-large", "gpt2-xl", "opt-125m", "opt-1.3b"]
    for can in cans:
        sub_path = path + "/" + can
        predict = read_json_files_in_directory(sub_path)
        print("##############{} result##############".format(can))
        count = 0
        for stage in predict.keys():
            print(stage)
            for subdataset in predict[stage].keys():
                random_acc = 0
                total = len(predict[stage][subdataset])
                correct = 0
                for item in predict[stage][subdataset]:
                    random_acc += 1 / len(item["candidates"])
                    pre = item["predict"]
                    pre_ans = pre
                    if pre_ans == item["answer"]:
                        correct += 1

                print(subdataset, (correct/total - random_acc / total) / (1 - random_acc / total))
            print()
