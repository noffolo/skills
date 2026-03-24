---
name: vn-stock-analyst
description: "Phân tích và tư vấn đầu tư tài sản toàn cầu — cổ phiếu VN, US equities, vàng, crypto, DCA. Kết hợp phân tích kỹ thuật real-time (RSI, MACD, EMA, Bollinger Bands) từ TradingView với phân tích cơ bản (P/E, ROE, Sharpe, CAGR, định giá ngành). Use when: (1) user hỏi về giá cổ phiếu VN hoặc toàn cầu, (2) user muốn biết nên mua tài sản nào, (3) user hỏi về danh mục đầu tư, (4) user muốn tính DCA tích lũy hàng tháng, (5) user hỏi nên đầu tư bao nhiêu/tháng, (6) user muốn estimate lợi nhuận theo thời gian, (7) user muốn so sánh các loại tài sản toàn cầu, (8) user hỏi về vàng, crypto, S&P 500, ETF, (9) user hỏi về lướt sóng, swing trading, scalping, day trading VN."
---

# VN Stock Analyst

Phân tích cổ phiếu Việt Nam — kỹ thuật real-time + cơ bản + định giá + estimate sinh lời.

## ⚠️ Nguyên tắc quan trọng nhất

**CAGR lịch sử ≠ kỳ vọng từ giá hiện tại.**
Luôn hỏi: *"Nếu mua HÔM NAY ở giá này, P/E là bao nhiêu? Còn rẻ không?"*

Ví dụ: MCH CAGR 73%/năm từ đáy 30k → nhưng ở giá 161k hiện tại P/E ~37x là **đắt**.
Sharpe 2.19 là lịch sử từ vùng giá thấp — không apply cho người mua hôm nay.

---

## Step 0: Hiểu rõ yêu cầu & Check Macro

Trước khi phân tích bất kỳ tài sản nào, luôn check:

**Macro context hiện tại (cập nhật 23/03/2026):**
- FED rate: **3.5-3.75%** (giữ nguyên 18/3/2026, hawkish — chỉ 1 lần cắt dự kiến 2026)
- PCE inflation forecast: **2.7%** (nâng từ 2.4%)
- **🔴 Iran War đang diễn ra** — dầu WTI $95-99, đe dọa Eo Hormuz
- **🔴 VN-Index: ~1,604** — giảm 14% trong tháng, khối ngoại bán ròng -27,591 tỷ YTD
- **🟢 FTSE upgrade VN** → hiệu lực 21/09/2026 → catalyst lớn nhất
- Vàng XAUUSD: ~$4,362 (điều chỉnh -15% từ ATH $5,608)
- BNB: Áp lực risk-off, ecosystem vẫn mạnh (TVL $6.7B, #3 globally)

**Tác động lên danh mục:**
- 🟢 Mua tích lũy: MBB (P/E 6.5x), Vàng, S&P 500 ETF
- 🟢 DCA: FPT (P/E 13-14x, rẻ bất thường nhưng dưới EMA200)
- ⏳ Hold: BNB (chờ FED cắt), TCB
- 🔴 Tránh: VCB (P/E đắt), BĐS (lãi suất tăng), crypto mới
- 🟢 Mua mới: GAS/PVS (hưởng lợi dầu cao)

Xem chi tiết: `references/macro-update-2026-03.md`, `references/crypto-analysis.md`, `references/gold-analysis.md`.

---

Xác định:
- **Mục tiêu**: Tìm cổ phiếu mới? Phân tích mã cụ thể? Estimate lợi nhuận? Scan thị trường?
- **Thời gian nắm giữ**: Ngắn hạn (< 3 tháng), trung hạn (3-12 tháng), dài hạn (> 1 năm)
- **Vốn**: Để estimate portfolio allocation và risk
- **Khẩu vị rủi ro**: Bảo thủ / Cân bằng / Tích cực

---

## Step 1: Real-time Data (TradingView Scanner)

TradingView scanner hoạt động **KHÔNG cần auth**:

```bash
# Scan toàn HOSE tìm oversold
python3 ~/.openclaw/workspace/skills/vn-stock-analyst/scripts/scan_market.py --rsi 40 --exchange HOSE

# Phân tích kỹ thuật sâu 1 mã
python3 ~/.openclaw/workspace/skills/vn-stock-analyst/scripts/analyze_stock.py FPT HOSE

# Estimate lợi nhuận theo thời gian
python3 ~/.openclaw/workspace/skills/vn-stock-analyst/scripts/estimate_returns.py MBB
```

**Fetch thủ công nhiều mã:**
```python
import urllib.request, json

payload = {
    "symbols": {"tickers": ["HOSE:MBB","HOSE:TCB","HOSE:FPT"]},
    "columns": ["name","close","change","volume","RSI","EMA20","EMA50","EMA200",
                "MACD.macd","MACD.signal","BB.upper","BB.lower",
                "price_52_week_high","price_52_week_low","Stoch.K","Stoch.D"]
}
req = urllib.request.Request(
    "https://scanner.tradingview.com/vietnam/scan",
    data=json.dumps(payload).encode(),
    headers={"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"},
    method="POST"
)
with urllib.request.urlopen(req, timeout=10) as r:
    data = json.loads(r.read())
```

---

## Step 2: Phân tích Kỹ thuật

Đọc từng chỉ báo theo thứ tự ưu tiên:

### 1. EMA200 — Kiểm tra TRƯỚC TIÊN
- `close > EMA200` ✅ → Long-term uptrend còn nguyên → **có thể xem xét mua**
- `close < EMA200` ❌ → Downtrend dài hạn → **thận trọng, chỉ mua nếu có catalyst đặc biệt**

**⚠️ Không mua cổ phiếu RSI oversold nhưng dưới EMA200** (FPT case: RSI 31 + -21% dưới EMA200 → TRÁNH)

### 2. RSI(14)
| RSI | Tín hiệu | Hành động |
|---|---|---|
| < 30 | 🟢🟢 Oversold cực mạnh | Xem xét mua mạnh nếu trên EMA200 |
| 30–40 | 🟢 Oversold | DCA nếu trên EMA200 |
| 40–60 | 🟡 Neutral | Giữ / chờ |
| 60–70 | 🔴 Cận overbought | Không thêm vị thế |
| > 70 | 🔴🔴 Overbought | Cân nhắc chốt lời |

### 3. MACD
- `macd > signal` → 🟢 Bullish momentum
- `macd < signal` → 🔴 Bearish momentum
- MACD vừa cắt lên signal ở vùng âm → **tín hiệu mua mạnh**

### 4. Bollinger Bands
- `close ≤ BB.lower` → Gần đáy dải → tiềm năng bounce
- BB co lại (squeeze) → sắp biến động mạnh, chờ breakout

### 5. Stochastic K/D
- K < 20: Oversold | K > 80: Overbought
- K cắt lên D ở vùng < 20 → mua signal

### 6. 52W Position
```
pos52 = (close - low52w) / (high52w - low52w) × 100
```
- < 20%: Gần đáy 52W — vùng value tốt
- > 80%: Gần đỉnh 52W — momentum cao nhưng rủi ro

### 🎯 Buy Zone Score (tổng hợp)
```python
score = 0
if rsi < 30: score += 3
elif rsi < 40: score += 2
if close > ema200: score += 2
if pe_discount > 20%: score += 3  # P/E < Fair P/E - 20%
elif pe_discount > 0: score += 2
if pos52 < 20: score += 2
elif pos52 < 40: score += 1
if close <= bb_lower * 1.02: score += 2
if macd > macd_signal: score += 1
# Max: 15 điểm
# ≥ 10: Mua mạnh | 7-9: DCA | 4-6: Theo dõi | < 4: Bỏ qua
```

---

## Step 3: Phân tích Định giá — BẮT BUỘC

**Không đưa ra khuyến nghị MUA nếu chưa check định giá.**

### P/E Analysis
```
Upside = (Fair P/E - Current P/E) / Fair P/E × 100%
```

| Upside | Đánh giá |
|---|---|
| > 25% | 🟢 Rất rẻ — mua |
| 10–25% | 🟡 Hơi rẻ — tích lũy |
| 0–10% | 🟡 Hợp lý — OK |
| < 0% | 🔴 Đắt — chờ điều chỉnh |
| < -15% | 🔴🔴 Đắt nhiều — tránh |

**Fair P/E theo ngành VN:**
- Ngân hàng: 10–12x | Công nghệ: 20–25x | Thép: 8–12x
- Tiêu dùng: 15–22x | BĐS: 12–18x | Dầu khí: 10–14x

Xem chi tiết trong `references/sector-fundamentals.md`

### Các chỉ số cơ bản khác
- **ROE > 15%**: tốt | **> 20%**: xuất sắc
- **D/E < 1.0**: ít nợ (ngân hàng ngoại lệ)
- **FCF dương**: công ty sinh tiền thực
- **EPS CAGR**: driver chính của giá dài hạn

Xem framework đầy đủ trong `references/financial-analysis-knowledge.md`

---

## Step 4: Phân tích Ngành & Catalyst

Reference `references/sector-fundamentals.md`.

Luôn trả lời:
1. **Ngành đang ở đâu trong chu kỳ?** (tăng trưởng / đỉnh / suy thoái / đáy)
2. **Catalyst 1-3 năm tới là gì?**
3. **Rủi ro chính là gì?**

**Catalyst chung cho VN 2026-2028:**
- Nâng hạng thị trường FTSE/MSCI → vốn ngoại đổ vào
- Lãi suất giảm → P/E hợp lý cao hơn, BĐS phục hồi
- Đầu tư công tăng → thép, vật liệu xây dựng
- Chuyển đổi số → FPT, tech
- GDP 6-7%/năm → ngân hàng, tiêu dùng

---

## Step 5: Estimate Sinh lời

```bash
python3 ~/.openclaw/workspace/skills/vn-stock-analyst/scripts/estimate_returns.py [TICKER] [--capital X] [--years N]
```

Script tính từ VNDirect historical data:
- **CAGR** 3Y/5Y (tỷ lệ tăng trưởng kép)
- **Volatility** hàng năm (độ biến động)
- **Max Drawdown** (mức giảm tối đa từ đỉnh)
- **Sharpe Ratio** (return/risk)
- **3 kịch bản** Bear/Base/Bull × 6M/1Y/3Y/5Y

**⚠️ Luôn nhắc user:**
- CAGR lịch sử là từ giá VÀO của quá khứ, không phải từ giá hiện tại
- Nếu P/E hiện tại đã cao → estimate thực tế thấp hơn CAGR lịch sử
- So sánh với: gửi ngân hàng 5.5%/năm và VN-Index ~11%/năm

Xem phương pháp đầy đủ trong `references/return-estimation.md`

---

## Step 6: Portfolio Allocation

Khi user hỏi nên phân bổ vốn như thế nào:

### Sizing theo Sharpe
| Sharpe | Tỷ trọng tối đa |
|---|---|
| > 1.5 | 35% |
| 1.0–1.5 | 25% |
| 0.5–1.0 | 15% |
| < 0.5 | 10% |

### Sizing theo Max Drawdown
| Max DD | Tỷ trọng tối đa |
|---|---|
| < 30% | 30% |
| 30–50% | 20% |
| 50–70% | 10% |
| > 70% | 5% |

### DCA Strategy
- Không all-in một lúc
- Chia 3–5 lần mua trong 4–8 tuần
- Mua thêm khi RSI giảm về vùng oversold

---

## Step 7: Output Format

```
## 📊 [TICKER] — [Tên công ty]
Giá: X,XXX VND | Hôm nay: +/-X.XX% | Volume: XM

### Kỹ thuật
- RSI: XX.X [tín hiệu]
- EMA200: X,XXX [▲ Trên / ▼ Dưới] — [Long-term uptrend / Downtrend]
- MACD: [🟢 Bullish / 🔴 Bearish]
- Bollinger: [vị trí]
- 52W: High X,XXX | Low X,XXX | Vị trí: XX%
- Score: X/15

### Định giá
- P/E hiện tại: XX.Xx (Fair: XX-XXx)
- Upside định giá: +/-XX%
- ROE: XX% | D/E: XX

### Cơ bản & Ngành
- Ngành: [tên]
- Catalyst: [1-2 điểm chính]
- Rủi ro: [1-2 điểm chính]

### Estimate (Base case)
- 1 năm: +/-XX% (~Xtr từ 10tr)
- 3 năm: +/-XX% (~Xtr từ 10tr)
- Sharpe: X.XX | Max DD: -XX%

### Kết luận
[🟢 MUA / 🟡 THEO DÕI / ⏳ CHỜ / 🔴 TRÁNH]
Lý do: [1-2 câu ngắn gọn]
Vùng mua lý tưởng: [X,XXX – X,XXX VND]
```

---

## Step 8: Swing Trading & Lướt Sóng

Khi user hỏi về **lướt sóng, swing trading, scalping, day trading**, hoặc muốn trade ngắn hạn (2-10 ngày):

Reference đầy đủ: `references/swing-trading-vn.md`

### Quick Workflow

1. **Screening:** Chạy swing screener tìm mã phù hợp
   ```bash
   # Hoặc dùng scan_market.py với RSI thấp + volume cao
   python3 ~/.openclaw/workspace/skills/vn-stock-analyst/scripts/scan_market.py --rsi 45 --exchange HOSE
   ```

2. **Technical check (swing-specific):**
   - RSI divergence (bullish/bearish) trên D1
   - MACD crossover position (vùng âm = mua mạnh)
   - Bollinger squeeze → chờ breakout
   - ADX > 25 → trend đủ mạnh để swing
   - Williams %R, CCI, MFI → confirm thêm
   - Ichimoku: Price vs Cloud, TK cross

3. **Entry criteria:**
   - R:R tối thiểu 1:2 (KHÔNG trade nếu < 1:2)
   - Volume xác nhận (> 1.5x avg 20 phiên)
   - Candlestick pattern tại S/R (hammer, engulfing, morning star)
   - Stop loss xác định TRƯỚC khi vào lệnh

4. **Position sizing:**
   - 2% rule: Max risk 2% vốn per trade
   - Kelly Criterion (Half Kelly): `Kelly % = W - [(1-W)/R]`, dùng 50%
   - Max 3-5 vị thế swing cùng lúc

5. **Risk management:**
   - Stop loss: 3-5% (VN30), 5-7% (midcap)
   - Daily loss limit: -2% → dừng trade
   - Max drawdown: -10% → dừng 1 tuần
   - Pyramiding (thêm khi lời), KHÔNG averaging down mã swing

### Scalping/Day Trading VN:
- ATO/ATC strategies (gap & go, ATC momentum)
- T+2.5 rule: Mua chiều nay → bán chiều T+2
- VWAP pullback, Opening Range Breakout
- Pivot Points (daily) cho intraday levels

### Output Format (Swing)
```
## 🏄 [TICKER] — Swing Analysis
Setup: [RSI Divergence / BB Squeeze / MACD Cross / ...]
Entry: X,XXX VND | Stop Loss: X,XXX (-X%) | Target: X,XXX (+X%)
R:R: 1:X | Position Size: X% vốn (XX CP)
ADX: XX | Williams %R: -XX | Ichimoku: [Trên/Dưới Cloud]
Timeframe: X-X ngày
⚡ Confidence: [Cao/Trung bình/Thấp]
```

---

## References

- `references/sector-fundamentals.md` — P/E chuẩn, catalyst, risk từng ngành VN
- `references/sector-update-2026.md` — Cập nhật sector Q1/2026: P/E mới, catalyst mới, ranking ngành
- `references/financial-analysis-knowledge.md` — RSI, MACD, P/E, Sharpe, DCA, Global portfolio, lessons learned
- `references/macro-update-2026-03.md` — Macro context 03/2026: FED, VN-Index, Iran War, dầu, lãi suất
- `references/crypto-analysis.md` — Framework phân tích crypto/BNB: on-chain, tokenomics, DeFi, ecosystem
- `references/gold-analysis.md` — Framework phân tích vàng XAUUSD: factors, indicators, strategy
- `references/advanced-ta.md` — Fibonacci Retracement/Extension, Elliott Wave, Volume Profile
- `references/return-estimation.md` — Methodology estimate sinh lời
- `references/swing-trading-vn.md` — Swing trading, scalping, lướt sóng VN: indicators, strategies, risk management

## Scripts

- `scripts/scan_market.py` — Scan toàn sàn tìm cơ hội
- `scripts/analyze_stock.py` — Phân tích kỹ thuật sâu 1 mã
- `scripts/estimate_returns.py` — Estimate lợi nhuận theo lịch sử
- `scripts/dca_calculator.py` — Tính DCA tích lũy hàng tháng

**DCA Calculator:**
```bash
python3 ~/.openclaw/workspace/skills/vn-stock-analyst/scripts/dca_calculator.py [monthly_vnd] [years]
# Ví dụ: 2 triệu/tháng, 10 năm
python3 ~/.openclaw/workspace/skills/vn-stock-analyst/scripts/dca_calculator.py 2000000 10
```

---

*⚠️ Phân tích mang tính tham khảo, không phải khuyến nghị đầu tư. DYOR.*
