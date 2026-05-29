import pandas as pd
import os

file_path = 'data/magnus_carlsen_all_online_games_cleaned.csv'

if os.path.exists(file_path):
    df = pd.read_csv(file_path, nrows=5)
    print("檔案找到！以下是欄位名稱：")
    print(df.columns.tolist())
    print("\n前 5 行資料如下：")
    print(df.head())
else:
    print(f"錯誤：找不到檔案，請確認 {os.path.abspath(file_path)} 是否存在")