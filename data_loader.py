import os
import pandas as pd

# 檢查檔案是否存在
file_name = 'magnus_carlsen_all_online_games_cleaned.csv'
if not os.path.exists(file_name):
    print(f"錯誤：找不到檔案 '{file_name}'！")
    print(f"目前目錄是：{os.getcwd()}")
else:
    try:
        df = pd.read_csv(file_name)
        print("成功讀取檔案！")
        print(df.head())
    except Exception as e:
        print(f"讀取時發生錯誤: {e}")

# 延續您剛才讀取的 df
# 這一行會把每一場比賽的 moves 拆開，並全部存成一個清單
all_moves = []
for moves_str in df['moves']:
    all_moves.extend(moves_str.split(' '))

print(f"總共處理了 {len(all_moves)} 個棋步")
print(f"前 10 個棋步範例: {all_moves[:10]}")