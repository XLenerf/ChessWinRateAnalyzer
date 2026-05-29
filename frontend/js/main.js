var board = null;
var game = new Chess(); // 處理西洋棋規則的邏輯引擎
var $winRateList = $('#win-rate-list');

function onDrop (source, target) {
    // 檢查移動是否合法
    var move = game.move({
        from: source,
        to: target,
        promotion: 'q' // 預設升變為皇后
    });

    // 如果非法移動，棋子彈回原位
    if (move === null) return 'snapback';

    // 移動成功後，取得當前 FEN 並向 Flask 請求勝率
    fetchWinRate(game.fen());
}

function fetchWinRate(fen) {
    $winRateList.html('查詢中...');
    
    // 向你的 Flask 後端發送請求
    fetch(`http://127.0.0.1:5000/get_win_rate?fen=${encodeURIComponent(fen)}`)
        .then(response => response.json())
        .then(data => {
            if (data.length === 0) {
                $winRateList.html('資料庫中尚無此盤面的後續統計。');
                return;
            }

            let html = '';
            data.forEach(item => {
                html += `
                    <div class="move-row">
                        <span><strong>${item.move}</strong></span>
                        <span>勝率: ${item.win_rate}%</span>
                    </div>`;
            });
            $winRateList.html(html);
        })
        .catch(err => {
            $winRateList.html('無法連線到後端伺服器。');
            console.error(err);
        });
}

// 棋盤設定
var config = {
    draggable: true,
    position: 'start',
    onDrop: onDrop,
    pieceTheme: 'img/chesspieces/wikipedia/{piece}.png' // 指向你解壓縮後的圖片路徑
};

board = Chessboard('myBoard', config);