# Binance Futures Testnet Trading Bot

A Python CLI application for placing orders on Binance Futures Testnet (USDT-M).
Supports **MARKET** and **LIMIT** orders with structured logging and clean error handling.

---

## Project Structure

```
futures_bot/
├── bot/
│   ├── __init__.py
│   ├── client.py          # REST API client with HMAC-SHA256 signing
│   ├── orders.py          # Order placement, status, cancel logic
│   ├── validators.py      # Input validation
│   └── logging_config.py  # Rotating file + console logger
├── logs/                  # Auto-created on first run
├── cli.py                 # CLI entry point (argparse)
├── requirements.txt
├── .env.example
└── README.md
```

---

## Setup

**1. Clone the repository:**
```bash
git clone <repo-url>
cd futures_bot
```

**2. Create and activate a virtual environment:**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

**3. Install dependencies:**
```bash
pip install -r requirements.txt
```

**4. Get Futures Testnet API credentials:**
- Go to [testnet.binancefuture.com](https://testnet.binancefuture.com)
- Log in with GitHub
- Generate an API key under **API Key** section

**5. Configure your `.env` file:**
```bash
cp .env.example .env   # Mac/Linux
copy .env.example .env  # Windows
```

Edit `.env`:
```
BINANCE_API_KEY=your_actual_key
BINANCE_API_SECRET=your_actual_secret
```

---

## How to Run

### Place a MARKET order
```bash
# Buy 0.01 BTC at market price
python cli.py place --symbol BTCUSDT --side BUY --type MARKET --quantity 0.01

# Sell 0.01 BTC at market price
python cli.py place --symbol BTCUSDT --side SELL --type MARKET --quantity 0.01
```

### Place a LIMIT order
```bash
# Buy 0.01 BTC at $60,000
python cli.py place --symbol BTCUSDT --side BUY --type LIMIT --quantity 0.01 --price 60000

# Sell 0.01 BTC at $70,000
python cli.py place --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.01 --price 70000
```

### Check order status
```bash
python cli.py status --symbol BTCUSDT --order-id 123456789
```

### Cancel an open order
```bash
python cli.py cancel --symbol BTCUSDT --order-id 123456789
```

### Help
```bash
python cli.py --help
python cli.py place --help
```

---

## Sample Output

### MARKET BUY order:
```
─────────────────────────────────────────────
  ORDER REQUEST SUMMARY
─────────────────────────────────────────────
  Symbol    : BTCUSDT
  Side      : BUY
  Type      : MARKET
  Quantity  : 0.01
─────────────────────────────────────────────

  ORDER RESPONSE
─────────────────────────────────────────────
  Order ID    : 3291543
  Status      : FILLED
  Executed Qty: 0.01
  Avg Price   : 63500.10
  Symbol      : BTCUSDT
  Side        : BUY
  Type        : MARKET
─────────────────────────────────────────────

✅ Order placed successfully!
```

### LIMIT BUY order:
```
─────────────────────────────────────────────
  ORDER REQUEST SUMMARY
─────────────────────────────────────────────
  Symbol    : BTCUSDT
  Side      : BUY
  Type      : LIMIT
  Quantity  : 0.01
  Price     : 60000.0
─────────────────────────────────────────────

  ORDER RESPONSE
─────────────────────────────────────────────
  Order ID    : 3291601
  Status      : NEW
  Executed Qty: 0
  Avg Price   : 0
  Symbol      : BTCUSDT
  Side        : BUY
  Type        : LIMIT
─────────────────────────────────────────────

✅ Order placed successfully!
```

---

## Logging

- **Console**: INFO level and above (what you see when running commands)
- **`logs/trading_bot.log`**: DEBUG level — full request/response detail

Log files rotate at 10MB, keeping the last 3 files.

Sample log entries:
```
2024-01-15 14:32:01 | INFO     | Placing MARKET BUY order | Symbol: BTCUSDT | Qty: 0.01
2024-01-15 14:32:02 | INFO     | Order placed successfully | OrderId: 3291543 | Status: FILLED | ExecutedQty: 0.01 | AvgPrice: 63500.10
2024-01-15 14:32:10 | INFO     | Placing LIMIT BUY order | Symbol: BTCUSDT | Qty: 0.01 | Price: 60000.0
2024-01-15 14:32:11 | INFO     | Order placed successfully | OrderId: 3291601 | Status: NEW | ExecutedQty: 0 | AvgPrice: 0
```

---

## Assumptions

1. **Futures Testnet only** — All requests go to `https://testnet.binancefuture.com`. To use mainnet, change `BASE_URL` in `bot/client.py`.
2. **USDT-M Futures** — Designed for USDT-margined perpetual contracts (e.g., BTCUSDT, ETHUSDT).
3. **GTC time-in-force** — LIMIT orders use Good Till Cancelled by default.
4. **Quantity precision** — Binance enforces minimum quantity and step size per symbol. Use at least `0.01` for BTCUSDT on testnet.
5. **No leverage setting** — Default leverage from your testnet account is used. Adjust it on the testnet dashboard if needed.
6. **Python 3.10+** — Uses `X | Y` union type hint syntax.

---

## Dependencies

| Package | Purpose |
|---|---|
| `requests` | HTTP client for REST API calls |
| `python-dotenv` | Load API credentials from `.env` |
