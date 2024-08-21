import json
import argparse

from kyoku import Kyoku


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("files", nargs="+", help="paifu file")
    return parser.parse_args()


def load_paifu(file):
    with open(file) as f:
        json_data = json.load(f)
    return json_data


def count_kyoku(json_data):
    cnt = 0
    for entry in json_data:
        if entry["cmd"] == "kyokustart":
            cnt += 1
    return cnt


def extract_one_kyoku(json_data, kyoku_num):
    max_kyoku_num = count_kyoku(json_data)
    if kyoku_num < 0:
        raise ValueError("kyoku_num is too small")
    elif max_kyoku_num < kyoku_num:
        raise ValueError("kyoku_num is too large")

    kyoku_num += 1
    kyoku = []
    for entry in json_data:
        if entry["cmd"] == "kyokustart":
            kyoku_num -= 1
            if kyoku_num == 0:
                kyoku.append(entry)
        elif kyoku_num == 0:
            kyoku.append(entry)
            if entry["cmd"] == "kyokuend":
                break
    return kyoku


def show_kyoku(kyoku_data):
    all_data = []
    kyoku = Kyoku(kyoku_data)
    #print(f"{kyoku.is_sutehai}")
    if kyoku.is_sutehai == True:
        print("---------------------------")
        print(f"{kyoku.show()}")
        kyoku.show()
        trdata = kyoku.make_tr_data()
        print(trdata)
        all_data.append([trdata, "sutehai"])
    return all_data


if __name__ == "__main__":
    args = parse_args()
    hoge = []
    for file in args.files:
        json_data = load_paifu(file)
        #print(count_kyoku(json_data))
    
        for kyoku_num in range(count_kyoku(json_data)):
            kyoku_data = extract_one_kyoku(json_data, kyoku_num)
            train_kyoku_data = show_kyoku(kyoku_data)
            hoge.extend(train_kyoku_data)




