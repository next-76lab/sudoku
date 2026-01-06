"""
✨ STARLIGHT SUDOKU ✨
=====================
可愛いナンプレ（数独）ゲーム！100ステージ搭載
動く背景 + ステージセレクト + スマホ完全対応
"""

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Starlight Sudoku", page_icon="🔢", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
    #MainMenu, header, footer {visibility: hidden;}
    .stApp { margin: 0; padding: 0; }
    .block-container { padding: 0 !important; margin: 0 !important; max-width: 100% !important; }
    iframe { border: none !important; }
</style>
""", unsafe_allow_html=True)

game_html = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="mobile-web-app-capable" content="yes">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.9.0/p5.min.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Fredoka+One&family=Nunito:wght@400;700&display=swap" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; -webkit-tap-highlight-color: transparent; }
        html, body { 
            width: 100%; height: 100%; 
            overflow: hidden; 
            touch-action: none;
            overscroll-behavior: none;
            -webkit-overflow-scrolling: none;
            font-family: 'Nunito', sans-serif; 
            user-select: none;
            -webkit-user-select: none;
            position: fixed;
            top: 0; left: 0;
        }
        
        #bg-canvas { position: fixed; top: 0; left: 0; width: 100%; height: 100%; z-index: 0; }
        
        #game-container {
            position: relative; z-index: 10;
            width: 100%; height: 100%;
            display: flex; flex-direction: column;
            align-items: center; justify-content: center;
            padding: 8px;
            padding-top: max(8px, env(safe-area-inset-top));
            padding-bottom: max(8px, env(safe-area-inset-bottom));
        }
        
        #title {
            font-family: 'Fredoka One', cursive;
            font-size: clamp(14px, 4vw, 26px);
            color: #ffe066;
            text-shadow: 2px 2px 0 #8b5a2b, 0 0 10px rgba(255,224,102,0.5);
            background: linear-gradient(180deg, #a67c52 0%, #8b5a2b 100%);
            padding: 6px 20px;
            border-radius: 10px;
            border: 3px solid #5d3a1a;
            box-shadow: 0 4px 8px rgba(0,0,0,0.3);
            margin-bottom: 6px;
            cursor: pointer;
        }
        
        #stage-display {
            font-family: 'Fredoka One', cursive;
            font-size: clamp(10px, 2.5vw, 15px);
            color: #fff;
            background: linear-gradient(180deg, #7c5cbf 0%, #5a3d9e 100%);
            padding: 4px 16px;
            border-radius: 12px;
            border: 2px solid #3d2a6e;
            margin-bottom: 8px;
            cursor: pointer;
        }
        
        #timer {
            font-size: clamp(11px, 2.5vw, 15px);
            color: #fff;
            background: rgba(0,0,0,0.4);
            padding: 3px 12px;
            border-radius: 8px;
            margin-bottom: 8px;
        }
        
        #sudoku-grid {
            display: grid;
            grid-template-columns: repeat(9, 1fr);
            gap: 1px;
            background: rgba(93, 58, 26, 0.95);
            border: 3px solid #8b5a2b;
            border-radius: 10px;
            padding: 2px;
            width: min(85vw, 85vh, 360px);
            aspect-ratio: 1;
            box-shadow: 0 5px 15px rgba(0,0,0,0.4);
        }
        
        .cell {
            aspect-ratio: 1;
            display: flex; align-items: center; justify-content: center;
            font-family: 'Nunito', sans-serif;
            font-weight: 700;
            font-size: clamp(12px, 3.5vw, 20px);
            background: rgba(255, 253, 245, 0.98);
            cursor: pointer;
            transition: all 0.1s;
            border-radius: 2px;
        }
        .cell:active { background: rgba(255, 230, 200, 1); }
        .cell.selected { background: #ffe4b3 !important; box-shadow: inset 0 0 0 2px #f0a030; }
        .cell.fixed { color: #5d3a1a; background: rgba(232, 220, 200, 0.98); font-weight: 800; }
        .cell.user { color: #4a7aca; }
        .cell.error { color: #d32f2f !important; background: rgba(255, 205, 210, 0.98) !important; }
        .cell.same-number { background: rgba(200, 230, 201, 0.98); }
        .cell:nth-child(3n) { border-right: 2px solid rgba(93, 58, 26, 0.8); }
        .row-border-bottom { border-bottom: 2px solid rgba(93, 58, 26, 0.8) !important; }
        
        #number-palette {
            display: flex; gap: 4px; margin-top: 10px;
            flex-wrap: wrap; justify-content: center;
            max-width: min(90vw, 380px);
        }
        .num-btn {
            width: clamp(28px, 7vw, 38px); height: clamp(28px, 7vw, 38px);
            border: 2px solid #5d3a1a; border-radius: 8px;
            background: linear-gradient(180deg, #f5e6c8 0%, #e8d4a8 100%);
            color: #5d3a1a;
            font-family: 'Nunito', sans-serif; font-weight: 700;
            font-size: clamp(13px, 3.5vw, 17px);
            cursor: pointer;
            box-shadow: 0 2px 4px rgba(0,0,0,0.2);
        }
        .num-btn:active { transform: scale(0.95); background: #e8d4a8; }
        .num-btn.erase { background: linear-gradient(180deg, #ffcdd2 0%, #ef9a9a 100%); color: #c62828; }
        
        #button-bar { display: flex; gap: 8px; margin-top: 10px; flex-wrap: wrap; justify-content: center; }
        .action-btn {
            padding: 7px 14px;
            border: 2px solid #5d3a1a; border-radius: 10px;
            background: linear-gradient(180deg, #a67c52 0%, #8b5a2b 100%);
            color: #ffe4c4; font-weight: 700;
            font-size: clamp(10px, 2.2vw, 12px);
            cursor: pointer; box-shadow: 0 2px 5px rgba(0,0,0,0.25);
        }
        .action-btn:active { transform: scale(0.95); }
        
        #stage-select-overlay {
            position: fixed; top: 0; left: 0; right: 0; bottom: 0;
            background: rgba(0,0,0,0.9);
            display: none; flex-direction: column;
            align-items: center;
            z-index: 2000;
            padding: 15px;
            padding-top: max(15px, env(safe-area-inset-top));
            overflow-y: auto;
            -webkit-overflow-scrolling: touch;
            touch-action: pan-y;
        }
        #stage-select-title {
            font-family: 'Fredoka One', cursive;
            font-size: clamp(18px, 5vw, 28px);
            color: #ffe066;
            text-shadow: 0 0 15px rgba(255,224,102,0.6);
            margin-bottom: 12px;
            margin-top: 10px;
        }
        #stage-page-nav {
            display: flex; gap: 12px; margin-bottom: 12px; align-items: center;
        }
        .page-btn {
            width: 40px; height: 40px;
            border: 2px solid #5d3a1a; border-radius: 50%;
            background: linear-gradient(180deg, #a67c52 0%, #8b5a2b 100%);
            color: #ffe4c4; font-weight: 700; font-size: 18px;
            cursor: pointer;
        }
        .page-btn:active { transform: scale(0.95); }
        .page-btn:disabled { opacity: 0.4; }
        #page-indicator { color: #fff; font-size: 14px; min-width: 50px; text-align: center; }
        
        #stage-grid {
            display: grid;
            grid-template-columns: repeat(5, 1fr);
            gap: 10px;
            max-width: min(95vw, 340px);
            margin-bottom: 15px;
        }
        .stage-btn {
            width: clamp(48px, 14vw, 58px); height: clamp(48px, 14vw, 58px);
            border: 2px solid #5d3a1a; border-radius: 10px;
            background: linear-gradient(180deg, #7c5cbf 0%, #5a3d9e 100%);
            color: #fff; font-family: 'Nunito', sans-serif; font-weight: 700;
            font-size: clamp(15px, 4vw, 19px);
            cursor: pointer;
        }
        .stage-btn:active { transform: scale(0.95); }
        .stage-btn.cleared { background: linear-gradient(180deg, #81c784 0%, #4caf50 100%); border-color: #2e7d32; }
        .stage-btn.current { background: linear-gradient(180deg, #ffb74d 0%, #ff9800 100%); border-color: #e65100; }
        
        #close-stage-select {
            padding: 12px 40px;
            border: 2px solid #5d3a1a; border-radius: 15px;
            background: linear-gradient(180deg, #a67c52 0%, #8b5a2b 100%);
            color: #ffe4c4; font-weight: 700;
            font-size: 15px; cursor: pointer;
            margin-bottom: 20px;
        }
        
        #clear-overlay {
            position: fixed; top: 0; left: 0; right: 0; bottom: 0;
            background: rgba(0,0,0,0.85);
            display: none; justify-content: center; align-items: center;
            flex-direction: column; z-index: 2000;
        }
        #clear-text {
            font-family: 'Fredoka One', cursive;
            font-size: clamp(24px, 7vw, 42px);
            color: #ffe066;
            text-shadow: 0 0 20px rgba(255,224,102,0.8);
            margin-bottom: 12px;
        }
        #clear-time { font-size: clamp(14px, 4vw, 20px); color: #fff; margin-bottom: 18px; }
        #next-btn {
            background: linear-gradient(180deg, #81c784 0%, #4caf50 100%);
            border: 3px solid #2e7d32;
            color: #fff; font-family: 'Fredoka One', cursive;
            font-size: clamp(14px, 4vw, 18px);
            padding: 12px 32px; border-radius: 25px; cursor: pointer;
        }
        #next-btn:active { transform: scale(0.95); }
    </style>
</head>
<body>
    <div id="bg-canvas"></div>
    
    <div id="game-container">
        <div id="title" onclick="showStageSelect()">⭐ STARLIGHT SUDOKU ⭐</div>
        <div id="stage-display" onclick="showStageSelect()">STAGE <span id="stage-num">1</span> / 100 ▼</div>
        <div id="timer">⏱ 00:00</div>
        <div id="sudoku-grid"></div>
        <div id="number-palette"></div>
        <div id="button-bar">
            <button class="action-btn" id="hint-btn">💡 ヒント</button>
            <button class="action-btn" id="select-btn">📋 選択</button>
            <button class="action-btn" id="reset-btn">🔄 リセット</button>
        </div>
    </div>
    
    <div id="stage-select-overlay">
        <div id="stage-select-title">⭐ STAGE SELECT ⭐</div>
        <div id="stage-page-nav">
            <button class="page-btn" id="prev-page">◀</button>
            <span id="page-indicator">1-10</span>
            <button class="page-btn" id="next-page">▶</button>
        </div>
        <div id="stage-grid"></div>
        <button id="close-stage-select">✕ 閉じる</button>
    </div>
    
    <div id="clear-overlay">
        <div id="clear-text">✨ STAGE CLEAR! ✨</div>
        <div id="clear-time">Time: 00:00</div>
        <button id="next-btn">NEXT STAGE →</button>
    </div>
    
    <script>
        document.addEventListener('touchmove', function(e) {
            if (!e.target.closest('#stage-select-overlay')) {
                e.preventDefault();
            }
        }, { passive: false });
        
        let clouds = [], moon, stars = [], shootingStars = [];
        
        class Cloud {
            constructor() {
                this.x = random(width); this.y = random(40, 150);
                this.size = random(50, 90); this.speed = random(0.15, 0.35);
                this.bobPhase = random(TWO_PI); this.hasFace = random() > 0.4;
            }
            update() { this.x += this.speed; if (this.x > width + 100) this.x = -100; this.bobPhase += 0.015; }
            draw() {
                const bobY = this.y + sin(this.bobPhase) * 5;
                push(); translate(this.x, bobY);
                fill(255, 255, 255, 200); noStroke();
                ellipse(0, 0, this.size * 1.2, this.size * 0.7);
                ellipse(-this.size * 0.4, 0, this.size * 0.8, this.size * 0.55);
                ellipse(this.size * 0.4, 0, this.size * 0.85, this.size * 0.6);
                if (this.hasFace) {
                    fill(80, 60, 60);
                    ellipse(-this.size * 0.12, 0, 5, 6); ellipse(this.size * 0.12, 0, 5, 6);
                    fill(255, 180, 180, 130);
                    ellipse(-this.size * 0.25, this.size * 0.08, 10, 6); ellipse(this.size * 0.25, this.size * 0.08, 10, 6);
                    noFill(); stroke(80, 60, 60); strokeWeight(1.5);
                    arc(0, this.size * 0.08, 12, 8, 0, PI);
                }
                pop();
            }
        }
        
        class Moon {
            constructor() { this.glowPhase = 0; }
            draw() {
                const size = min(width, height) * 0.1;
                const x = width - size - 20, y = size + 45;
                this.glowPhase += 0.02;
                push(); translate(x, y); noStroke();
                for (let i = 3; i > 0; i--) { fill(255, 240, 200, 20 + sin(this.glowPhase) * 8); ellipse(0, 0, size + i * 15); }
                fill(255, 248, 220); ellipse(0, 0, size);
                noFill(); stroke(80, 60, 60); strokeWeight(2);
                arc(-size * 0.18, -size * 0.05, size * 0.15, size * 0.1, PI, TWO_PI);
                arc(size * 0.18, -size * 0.05, size * 0.15, size * 0.1, PI, TWO_PI);
                arc(0, size * 0.12, size * 0.28, size * 0.2, 0, PI);
                noStroke(); fill(255, 180, 180, 130);
                ellipse(-size * 0.3, size * 0.08, size * 0.14, size * 0.09);
                ellipse(size * 0.3, size * 0.08, size * 0.14, size * 0.09);
                pop();
            }
        }
        
        class Star {
            constructor() { this.x = random(width); this.y = random(height * 0.7); this.size = random(1.5, 4); this.tw = random(TWO_PI); this.spd = random(0.03, 0.08); }
            draw() { this.tw += this.spd; fill(255, 255, 255, 120 + sin(this.tw) * 80); noStroke(); ellipse(this.x, this.y, this.size); }
        }
        
        class ShootingStar {
            constructor() { this.reset(); this.active = false; }
            reset() { this.x = random(width * 0.2, width * 0.7); this.y = random(40, 150); this.vx = random(8, 14); this.vy = random(3, 6); this.life = 1; }
            update() { if (!this.active) { if (random() > 0.997) this.active = true; return; } this.x += this.vx; this.y += this.vy; this.life -= 0.025; if (this.life <= 0) { this.reset(); this.active = false; } }
            draw() { if (!this.active) return; stroke(255, 240, 150, this.life * 200); strokeWeight(2.5); line(this.x, this.y, this.x - this.vx * 4, this.y - this.vy * 4); noStroke(); fill(255, 255, 200, this.life * 255); ellipse(this.x, this.y, 6); }
        }
        
        const TOTAL_STAGES = 100;
        const SAVE_KEY = 'starlight_sudoku_v5';
        
        let currentStage = 1, clearedStages = [];
        let board = [], solution = [], fixed = [];
        let selectedCell = -1, startTime = Date.now(), timerInterval;
        let currentPage = 0;
        
        function getEmptyCells(stage) { return Math.min(55, 25 + Math.floor(stage * 0.3)); }
        
        function generateSudoku() {
            solution = Array(81).fill(0); fillBoard(solution, 0);
            board = [...solution]; fixed = Array(81).fill(true);
            const emptyCells = getEmptyCells(currentStage);
            const indices = [...Array(81).keys()]; shuffleArray(indices);
            for (let i = 0; i < emptyCells; i++) { board[indices[i]] = 0; fixed[indices[i]] = false; }
        }
        
        function fillBoard(b, pos) {
            if (pos >= 81) return true;
            const nums = [1,2,3,4,5,6,7,8,9]; shuffleArray(nums);
            for (const num of nums) { if (isValidPlacement(b, pos, num)) { b[pos] = num; if (fillBoard(b, pos + 1)) return true; b[pos] = 0; } }
            return false;
        }
        
        function isValidPlacement(b, pos, num) {
            const row = Math.floor(pos / 9), col = pos % 9;
            for (let c = 0; c < 9; c++) if (b[row * 9 + c] === num) return false;
            for (let r = 0; r < 9; r++) if (b[r * 9 + col] === num) return false;
            const br = Math.floor(row / 3) * 3, bc = Math.floor(col / 3) * 3;
            for (let r = br; r < br + 3; r++) for (let c = bc; c < bc + 3; c++) if (b[r * 9 + c] === num) return false;
            return true;
        }
        
        function shuffleArray(arr) { for (let i = arr.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [arr[i], arr[j]] = [arr[j], arr[i]]; } }
        
        function hasError(pos) {
            if (board[pos] === 0) return false;
            const num = board[pos], row = Math.floor(pos / 9), col = pos % 9;
            for (let c = 0; c < 9; c++) if (row * 9 + c !== pos && board[row * 9 + c] === num) return true;
            for (let r = 0; r < 9; r++) if (r * 9 + col !== pos && board[r * 9 + col] === num) return true;
            const br = Math.floor(row / 3) * 3, bc = Math.floor(col / 3) * 3;
            for (let r = br; r < br + 3; r++) for (let c = bc; c < bc + 3; c++) if (r * 9 + c !== pos && board[r * 9 + c] === num) return true;
            return false;
        }
        
        function renderGrid() {
            const grid = document.getElementById('sudoku-grid'); grid.innerHTML = '';
            for (let i = 0; i < 81; i++) {
                const cell = document.createElement('div'); cell.className = 'cell';
                const row = Math.floor(i / 9);
                if (row === 2 || row === 5) cell.classList.add('row-border-bottom');
                if (fixed[i]) cell.classList.add('fixed'); else cell.classList.add('user');
                if (board[i] !== 0) { cell.textContent = board[i]; if (hasError(i)) cell.classList.add('error'); }
                if (i === selectedCell) cell.classList.add('selected');
                if (selectedCell >= 0 && board[selectedCell] !== 0 && board[i] === board[selectedCell] && i !== selectedCell) cell.classList.add('same-number');
                const idx = i;
                cell.addEventListener('click', function(e) { e.preventDefault(); selectedCell = idx; renderGrid(); });
                cell.addEventListener('touchend', function(e) { e.preventDefault(); selectedCell = idx; renderGrid(); });
                grid.appendChild(cell);
            }
        }
        
        function inputNumber(num) {
            if (selectedCell < 0 || fixed[selectedCell]) return;
            board[selectedCell] = num; renderGrid();
            if (!board.includes(0)) { let hasErr = false; for (let i = 0; i < 81; i++) if (hasError(i)) { hasErr = true; break; } if (!hasErr) { clearInterval(timerInterval); showClear(); } }
        }
        
        function showClear() {
            const elapsed = Math.floor((Date.now() - startTime) / 1000);
            document.getElementById('clear-time').textContent = 'Time: ' + String(Math.floor(elapsed/60)).padStart(2,'0') + ':' + String(elapsed%60).padStart(2,'0');
            document.getElementById('clear-overlay').style.display = 'flex';
            if (!clearedStages.includes(currentStage)) clearedStages.push(currentStage);
            saveProgress();
        }
        
        function createPalette() {
            const palette = document.getElementById('number-palette'); palette.innerHTML = '';
            for (let n = 1; n <= 9; n++) {
                const btn = document.createElement('button'); btn.className = 'num-btn'; btn.textContent = n;
                btn.addEventListener('click', function(e) { e.preventDefault(); inputNumber(n); });
                btn.addEventListener('touchend', function(e) { e.preventDefault(); inputNumber(n); });
                palette.appendChild(btn);
            }
            const eraseBtn = document.createElement('button'); eraseBtn.className = 'num-btn erase'; eraseBtn.textContent = '✕';
            eraseBtn.addEventListener('click', function(e) { e.preventDefault(); inputNumber(0); });
            eraseBtn.addEventListener('touchend', function(e) { e.preventDefault(); inputNumber(0); });
            palette.appendChild(eraseBtn);
        }
        
        function updateTimer() {
            const elapsed = Math.floor((Date.now() - startTime) / 1000);
            document.getElementById('timer').textContent = '⏱ ' + String(Math.floor(elapsed/60)).padStart(2,'0') + ':' + String(elapsed%60).padStart(2,'0');
        }
        
        function initStage() {
            generateSudoku(); selectedCell = -1; startTime = Date.now();
            document.getElementById('stage-num').textContent = currentStage;
            document.getElementById('clear-overlay').style.display = 'none';
            document.getElementById('stage-select-overlay').style.display = 'none';
            renderGrid(); createPalette();
            if (timerInterval) clearInterval(timerInterval);
            timerInterval = setInterval(updateTimer, 1000);
        }
        
        function saveProgress() { localStorage.setItem(SAVE_KEY, JSON.stringify({ stage: currentStage, cleared: clearedStages })); }
        function loadProgress() {
            try { const data = JSON.parse(localStorage.getItem(SAVE_KEY)); if (data) { currentStage = data.stage || 1; clearedStages = data.cleared || []; } } catch (e) {}
        }
        
        function showStageSelect() {
            document.getElementById('stage-select-overlay').style.display = 'flex';
            currentPage = Math.floor((currentStage - 1) / 10);
            renderStageGrid();
        }
        
        function hideStageSelect() { document.getElementById('stage-select-overlay').style.display = 'none'; }
        
        function renderStageGrid() {
            const grid = document.getElementById('stage-grid'); grid.innerHTML = '';
            const start = currentPage * 10 + 1;
            const end = Math.min(start + 9, TOTAL_STAGES);
            
            document.getElementById('page-indicator').textContent = start + '-' + end;
            document.getElementById('prev-page').disabled = currentPage === 0;
            document.getElementById('next-page').disabled = currentPage >= 9;
            
            for (let s = start; s <= end; s++) {
                const btn = document.createElement('button'); btn.className = 'stage-btn'; btn.textContent = s;
                if (clearedStages.includes(s)) btn.classList.add('cleared');
                if (s === currentStage) btn.classList.add('current');
                const stage = s;
                btn.addEventListener('click', function(e) { e.preventDefault(); currentStage = stage; initStage(); });
                btn.addEventListener('touchend', function(e) { e.preventDefault(); currentStage = stage; initStage(); });
                grid.appendChild(btn);
            }
        }
        
        function setup() {
            const canvas = createCanvas(windowWidth, windowHeight); canvas.parent('bg-canvas');
            colorMode(RGB, 255);
            for (let i = 0; i < 5; i++) clouds.push(new Cloud());
            moon = new Moon();
            for (let i = 0; i < 40; i++) stars.push(new Star());
            for (let i = 0; i < 2; i++) shootingStars.push(new ShootingStar());
            
            loadProgress(); initStage();
            
            document.getElementById('hint-btn').addEventListener('click', function(e) { e.preventDefault(); for (let i = 0; i < 81; i++) { if (board[i] === 0) { board[i] = solution[i]; renderGrid(); break; } } });
            document.getElementById('reset-btn').addEventListener('click', function(e) { e.preventDefault(); initStage(); });
            document.getElementById('select-btn').addEventListener('click', function(e) { e.preventDefault(); showStageSelect(); });
            document.getElementById('close-stage-select').addEventListener('click', function(e) { e.preventDefault(); hideStageSelect(); });
            document.getElementById('prev-page').addEventListener('click', function(e) { e.preventDefault(); if (currentPage > 0) { currentPage--; renderStageGrid(); } });
            document.getElementById('next-page').addEventListener('click', function(e) { e.preventDefault(); if (currentPage < 9) { currentPage++; renderStageGrid(); } });
            document.getElementById('next-btn').addEventListener('click', function(e) { e.preventDefault(); currentStage = Math.min(currentStage + 1, TOTAL_STAGES); initStage(); });
        }
        
        function draw() {
            for (let y = 0; y < height; y += 2) {
                const t = y / height;
                let r, g, b;
                if (t < 0.35) { r = lerp(25, 55, t / 0.35); g = lerp(18, 40, t / 0.35); b = lerp(55, 80, t / 0.35); }
                else if (t < 0.65) { const tt = (t - 0.35) / 0.3; r = lerp(55, 110, tt); g = lerp(40, 60, tt); b = lerp(80, 100, tt); }
                else { const tt = (t - 0.65) / 0.35; r = lerp(110, 160, tt); g = lerp(60, 90, tt); b = lerp(100, 130, tt); }
                stroke(r, g, b); line(0, y, width, y);
            }
            for (let s of stars) s.draw();
            for (let ss of shootingStars) { ss.update(); ss.draw(); }
            moon.draw();
            for (let c of clouds) { c.update(); c.draw(); }
        }
        
        function windowResized() { resizeCanvas(windowWidth, windowHeight); }
    </script>
</body>
</html>
"""

components.html(game_html, height=800, scrolling=False)
