import json
import re
import operator

if __name__ == "__main__":
    file_name= "result/GPT3.5"
    # file_name= "result/GPT4"
    with open('{}.json'.format(file_name),"r")as f:
        datas = json.load(f)
        f.close()
    answer_map = {0:"A", 1:"B", 2:"C", 3:"D", 4:"E", 5:"F"}

    data_dict = {}
    for tem in datas:
        if tem["type"] not in data_dict.keys():
            data_dict[tem["type"]]=[]
        data_dict[tem["type"]].append(tem)

    all_avg,all_cnt=0,0
    for key in data_dict.keys():
        datas = data_dict[key]
        all_right,all_count,random_acc=0,0,0
        cur_data = []
        for tem in datas:
            random_acc+=1/len(tem["candidates"])
            answer = answer_map[tem["answer"]]
            pre_dict = {}
            for t in tem["generated_answer"]:
                match = re.search(r'\\boxed\{(.+?)\}', t)#[0])
                if match:
                    pre = match.group(1)
                    if pre not in ["A", "B", "C", "D"]:
                        pre = pre.split(".")[0]
                    pre_dict[pre] = pre_dict.get(pre, 0) + 1
                else:
                    pre="Not Found"
            res = sorted(pre_dict.items(), key=operator.itemgetter(1), reverse=True)

            if len(res) and res[0][0] == answer:
                all_right+=1
            tem["is_right"] = pre==answer
            cur_data.append(tem)
            # if pre not in ["A","B","C","D"]:
                # print(pre)
            all_count+=1
        with open("result/{}.json".format(key),"w")as f:
            json.dump(cur_data,f,indent="\t")
            f.close()
        # print("{}:{}".format(key, (all_right / all_count - random_acc / all_count) / (1 - random_acc / all_count)))
        print("{}:{}".format(key,(all_right/all_count-random_acc/all_count)/(1-random_acc/all_count)))
        all_avg+=(all_right/all_count-random_acc/all_count)/(1-random_acc/all_count)
        all_cnt+=1
        # print("True-{}:{}".format(key, all_right / all_count))
    print("Avg:{}".format(all_avg/all_cnt))