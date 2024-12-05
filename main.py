import csv
import os
import sys

from typing import Dict, List

simulation_contest_no_show_site_ids = []  # 模擬賽沒出席的
real_contest_no_show_site_ids = []  # 正式賽沒出席的


def load_data(filename: str) -> List[Dict[str, str]]:
    assert os.path.exists(filename), f"{filename} not exists."
    assert os.path.isfile(filename), f"{filename} is not a file."

    data = []
    with open(filename, "r") as f:
        data = list(csv.DictReader(f))

    return data


def main() -> None:
    assert len(sys.argv) >= 2, "No file set."

    filename = sys.argv[1]
    data = load_data(filename)

    assert data, "No data found in file."

    last_rank = None
    max_solved_count = None  # 最大正確題數

    headers = [
        "排名",
        "學校名稱",
        "崗位編號",
        "姓名",
        "術科時間",
        "解題數",
        "排名點數",
        "解題點數",
        "總分",
    ]
    rows = []
    for datum in data:
        rank_str = datum["Rank"]  # 排名
        team_affiliation = datum["TeamAffiliation"]  # 校名
        team_name = datum["TeamName"]  # 隊名（崗位編號_名字）
        solved_count_str = datum["SolvedCount"]  # 解題數
        total_time = datum["Score"]  # 術科時間

        if not rank_str and not team_affiliation and not team_name:
            continue  # 跳過加總

        site_id, name = team_name.split("_", 1)

        if not rank_str:
            assert last_rank is not None, "Can't found rank."
            rank_str = str(last_rank)

        assert rank_str.isdigit(), "Rank is not a number."
        assert solved_count_str.isdigit(), "Solved count is not a number."

        rank = int(rank_str)
        solved_count = int(solved_count_str)

        if site_id not in simulation_contest_no_show_site_ids:
            solved_count += 1

        if max_solved_count is None:
            max_solved_count = solved_count

        rank_point = 100 - int(rank) + 1  # 排名點數
        solved_point = 100 - (max_solved_count - solved_count) * 5  # 解題點數，跟最多比每多一台扣五分

        final_score = rank_point * solved_point / 100
        if (  # TODO: 兩場都沒出席的人直接零分（目前沒發生過這邊要再確認一下）
            site_id in simulation_contest_no_show_site_ids
            and site_id in real_contest_no_show_site_ids
        ):
            final_score = 0

        row = [
            rank,
            team_affiliation,
            site_id,
            name,
            total_time,
            solved_count,
            rank_point,
            solved_point,
            final_score,
        ]
        rows.append(row)

        last_rank = rank

    print(",".join(map(str, headers)))
    print("\n".join(map(lambda row: ",".join(map(str, row)), rows)))


if __name__ == "__main__":
    main()
