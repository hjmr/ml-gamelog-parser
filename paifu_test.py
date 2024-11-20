import argparse

from ml_utils import load_paifu, count_kyoku, extract_one_kyoku, extract_player_names
from ml_utils import Kyoku


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-k", "--kyoku_num", type=int, default=-1, help="kyoku number")
    parser.add_argument("file", help="paifu file")
    return parser.parse_args()


def show_one_kyoku(kyoku_json, player_names):
    kyoku = Kyoku(kyoku_json, player_names)
    while kyoku.step():
        if kyoku.was_tsumo:
            print("======== ツモ =========")
            kyoku.show()
        elif kyoku.was_sutehai:
            print("-------- 捨て ---------")
            kyoku.show()
    print("====== 終局 ======")
    kyoku.show()


if __name__ == "__main__":
    args = parse_args()
    json_data = load_paifu(args.file)
    if args.kyoku_num == -1:
        print("kyoku count:", count_kyoku(json_data))
    else:
        player_names = extract_player_names(json_data)
        kyoku_json = extract_one_kyoku(json_data, args.kyoku_num)
        show_one_kyoku(kyoku_json, player_names)
