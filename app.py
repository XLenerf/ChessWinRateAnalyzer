from flask import Flask, send_from_directory, jsonify, request
import mysql.connector
from flask_cors import CORS

# 設定 static_folder 為 'frontend'，讓所有 CSS/JS/IMG 都在這裡找
app = Flask(__name__, static_folder='frontend')
CORS(app)

# 連線設定
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "20050428",
    "database": "chesswinrate"
}

# 1. 指定首頁路由，指向 frontend 資料夾下的 index.html
@app.route('/')
def index():
    return send_from_directory('frontend', 'index.html')

# 2. 處理勝率查詢的 API
@app.route('/get_win_rate', methods=['GET'])
def get_win_rate():
    fen = request.args.get('fen')
    if not fen:
        return jsonify({"error": "Missing FEN"}), 400
        
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    
    try:
        cursor.execute("SELECT next_move, win_count, total_count FROM Board_Stats WHERE state_id = %s", (fen,))
        results = cursor.fetchall()
        
        data = []
        for row in results:
            rate = (row['win_count'] / row['total_count']) * 100
            data.append({
                "move": row['next_move'],
                "win_rate": round(rate, 2)
            })
        return jsonify(data)
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    # 這裡只需要一個啟動點
    app.run(debug=True, port=5000)