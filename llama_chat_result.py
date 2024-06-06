import json
import os
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
                    json_data = data
                except json.JSONDecodeError as e:
                    print("Error decoding JSON:", e)

    return json_data

def process_pre(pre_ans):
    if pre_ans not in ['A', 'B', 'C', 'D']:
        pre_ans = pre.split("is:")[-1].strip()[0]
        if pre_ans not in ['A', 'B', 'C', 'D']:
            pre_ans = pre.split("is:")[-1].strip()[0]
            if pre_ans not in ['A', 'B', 'C', 'D']:
                pre_ans = pre.split("answer is (")[-1].strip()[0]
                if pre_ans not in ['A', 'B', 'C', 'D']:
                    pre_ans = pre.split("answer is")[-1].strip()[0]
                    if pre_ans not in ['A', 'B', 'C', 'D']:
                        pre_ans = pre.split("answer is:")[-1].strip()[0]
                        if pre_ans not in ['A', 'B', 'C', 'D']:
                            pre_ans = \
                            pre.split("The propositional relationship between sentence1 and sentence2 is")[-1].strip()[
                                0]
                            if pre_ans not in ['A', 'B', 'C', 'D']:
                                pre_ans = \
                                pre.split("The propositional relationship between sentence1 and sentence2 is option")[
                                    -1].strip()[0]
                                if pre_ans not in ['A', 'B', 'C', 'D']:
                                    pre_ans = pre.split("is option")[-1].strip()[0]
                                    if pre_ans not in ['A', 'B', 'C', 'D']:
                                        pre_ans = pre.split("would be")[-1].strip()[0]
                                        if pre_ans not in ['A', 'B', 'C', 'D']:
                                            pre_ans = pre.split("given holidays would be:")[-1].strip()[0]
                                            if pre_ans not in ['A', 'B', 'C', 'D']:
                                                pre_ans = \
                                                    pre.split("The correct sequence would be:")[-1].strip()[0]
    return pre_ans

if __name__ == "__main__":
    path = "./result"
    cans = ["llama-2-7b-chat", "llama-2-13b-chat", "llama-2-70b-chat"]
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
                    pre_ans = pre.split("boxed")[-1][1]
                    pre_ans = process_pre(pre_ans)

                    if pre_ans == item["answer"]:
                        correct += 1

                print(subdataset, (correct/total - random_acc / total) / (1 - random_acc / total))
            print()
