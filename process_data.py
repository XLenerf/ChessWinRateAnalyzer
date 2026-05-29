import pandas as pd
import chess
import mysql.connector
import re

db_config = {
    "host": "localhost",
    "user": "root",
    "password": "20050428",
    "database": "chesswinrate",
    "use_pure": True
}

def process_games():
    print("正在連線至 MySQL...", flush=True)
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    print("連線成功！", flush=True)
    
    csv_file = 'data/magnus_carlsen_all_online_games_cleaned.csv'
    
    # 1. 自動檢測 CSV 欄位，確保不卡死
    try:
        sample_df = pd.read_csv(csv_file, nrows=1)
        columns = sample_df.columns.tolist()
        print(f"偵測到 CSV 欄位: {columns}", flush=True)
        # 如果你的欄位不是 FEN，這裡會自動修正
        target_col = 'FEN' if 'FEN' in columns else columns[0]
        print(f"將使用 '{target_col}' 欄位進行解析...", flush=True)
    except Exception as e:
        print(f"無法讀取 CSV: {e}")
        return

    reader = pd.read_csv(csv_file, chunksize=500)
    sql = """INSERT INTO Board_Stats (state_id, next_move, win_count, total_count)
             VALUES (%s, %s, %s, %s)
             ON DUPLICATE KEY UPDATE 
             total_count = total_count + VALUES(total_count),
             win_count = win_count + VALUES(win_count)"""
    
    batch_data = []
    total_games = 0
    LIMIT = 100000

    print("開始處理每一行數據...", flush=True)

    for chunk in reader:
        for _, row in chunk.iterrows():
            if total_games >= LIMIT: break
            
            try:
                # 使用動態抓取的 target_col
                raw_moves = str(row[target_col])
                moves = re.sub(r'\d+\.\s*', '', raw_moves).split(' ')
                
                board = chess.Board()
                for move in moves:
                    if len(move) < 2: continue
                    fen = board.fen()
                    batch_data.append((fen, move, 0, 1))
                    
                    if len(batch_data) >= 500:
                        cursor.executemany(sql, batch_data)
                        conn.commit()
                        batch_data = []
                    
                    board.push_san(move)
            except Exception:
                continue
            
            total_games += 1
            if total_games % 10 == 0:
                print(f"進度: {total_games}/{LIMIT} 場", flush=True)
        
        if total_games >= LIMIT: break

    print("處理完畢！")
    conn.close()

if __name__ == "__main__":
    process_games()