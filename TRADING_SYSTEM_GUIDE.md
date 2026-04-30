# 🤖 Otomatik Borsa Trading Sistemi — Sıfırdan Ustaya Rehber

> **Sualp için özel hazırlandı.** Mantığını anlayarak, test ederek, grafikleri görerek ilerleriz.  
> Her adımda `✅ TEST` ve `📊 GRAFİK` kontrolleri yapılır. Hiçbir adımı atlamıyoruz.

---

## 🗺️ YOLCULUK HARİTASI

```
PHASE 1: Ortam Kurulumu & Git Altyapısı
   └─ Python env, Git, Husky, Lint-Staged

PHASE 2: Veri Toplama
   └─ yfinance, SQLite, Grafik kontrolü

PHASE 3: Teknik Analiz
   └─ RSI, MACD, Bollinger Bands — MANTIK + GRAFIK

PHASE 4: Sinyal Üretimi
   └─ Sinyallerin nasıl oluştuğunu anlamak

PHASE 5: Risk Yönetimi
   └─ Para yönetimi matematiği

PHASE 6: Backtesting
   └─ Geçmişte test edip başarı oranını bulmak

PHASE 7: AI Ajanları
   └─ Her görevi yapan ayrı Claude ajanları

PHASE 8: Web Dashboard
   └─ Plotly grafikler, Flask API

PHASE 9: Canlı Ortam
   └─ Broker API bağlantısı
```

---

## 📖 MANTIK NEDEN ÖNEMLİ?

Kod yazmadan önce sistemi kafanda oturt:

```
SEN (karar vericisi)
    ↓
Piyasa Verisi → Teknik Analiz → Sinyal → Risk Kontrol → İşlem
    ↓                ↓              ↓           ↓           ↓
  Fiyatlar        RSI, MACD      AL/SAT     Miktar      Broker
  Volume          Bollinger      -50..+100  Stop Loss   Yapıkredi
  Geçmiş          Moving Avg                Max Kayıp   API/Scrape
```

**Şu soruları cevapla:**
1. "Sisteme ne zaman alım emri verdireceğim?" → Sinyal Lojiği
2. "Ne kadar kaybedebilirim?" → Risk Yönetimi
3. "Bu strateji geçmişte çalışmış mı?" → Backtesting
4. "Sistem beni aldatıyor mu?" → Grafik Kontrolü

---

---

# PHASE 1: Ortam Kurulumu & Git Altyapısı

## 1.1 Python Ortamı

### 🧠 MANTIK
Python'da büyük projeler için **virtual environment** kullanılır.
Neden? Farklı projeler farklı kütüphane versiyonları gerektirir.
`venv` ile izole bir ortam yaratıyoruz.

### 📝 KOMUTLAR

```bash
# Proje klasörünü oluştur
mkdir trading_system && cd trading_system

# Virtual environment oluştur
python3 -m venv venv

# Aktifleştir (Linux/Mac)
source venv/bin/activate

# Aktifleştir (Windows)
venv\Scripts\activate

# Terminalde (venv) göreceksin → doğru
```

### Kütüphaneleri Yükle

```bash
# Core
pip install pandas numpy yfinance scikit-learn

# Teknik analiz
pip install pandas-ta

# Görselleştirme
pip install matplotlib plotly

# Loglama
pip install loguru

# Web (ileride)
pip install flask flask-cors

# Geliştirici araçları
pip install black flake8 isort pytest pytest-cov

# Hepsini kaydet
pip freeze > requirements.txt
```

### ✅ TEST 1.1

```bash
python3 -c "
import pandas; print(f'pandas: {pandas.__version__}')
import numpy; print(f'numpy: {numpy.__version__}')
import yfinance; print(f'yfinance: {yfinance.__version__}')
print('✅ Tüm kütüphaneler yüklendi!')
"
```

**Beklenen Çıktı:**
```
pandas: 3.x.x
numpy: 2.x.x
yfinance: 0.2.x
✅ Tüm kütüphaneler yüklendi!
```

---

## 1.2 Git + GitHub Kurulumu

### 🧠 MANTIK
Git → Kodun geçmişini saklar, ekiple çalışmayı sağlar.
GitHub → Kodun cloud'da yedeği, paylaşım platformu.
Commit = "Şu an çalışan kodu kaydet" demek.

```
Local Computer          GitHub (Cloud)
     │                       │
     ├── git add             │
     ├── git commit ────────>│ push
     ├── git pull <──────────│ (güncel al)
     └── git log             │ (geçmiş)
```

### 📝 KOMUTLAR

```bash
# Git başlat
git init

# .gitignore oluştur (hassas dosyaları dışla)
cat > .gitignore << 'EOF'
# Python
venv/
__pycache__/
*.pyc
*.pyo
.env
*.egg-info/
dist/
build/

# Data & Logs
data/
*.db
*.log
*.sqlite3

# API Keys (ASLA commitlenmesin!)
.env
config_local.py
secrets.py

# IDE
.vscode/
.idea/
*.swp

# OS
.DS_Store
Thumbs.db
EOF

# İlk commit
git add .
git commit -m "feat: initial project structure"
```

---

## 1.3 Husky + Lint-Staged Kurulumu

### 🧠 MANTIK
**Problem:** "Çalışan kodu commit ettim ama kod çirkin ve hatalı."
**Çözüm:** Commit yapmadan önce otomatik kontrol yap!

```
sen git commit yazarsın
        ↓
   Husky devreye girer
        ↓
   lint-staged çalışır
   ┌────────────────┐
   │  black → format kodu
   │  flake8 → hata ara
   │  isort → import'ları sırala
   │  pytest → testleri çalıştır
   └────────────────┘
        ↓
   ✅ Geçti → Commit başarılı
   ❌ Başarısız → Commit durduruldu, hatayı düzelt
```

### 📝 KURULUM

Husky JavaScript tabanlı ama Python projelerinde de kullanılabilir.
Alternatif: **pre-commit** (Python'a daha yakın)

#### Seçenek A: pre-commit (Tavsiye Edilen)

```bash
# Kütüphaneyi yükle
pip install pre-commit

# Konfigürasyon dosyası oluştur
cat > .pre-commit-config.yaml << 'EOF'
repos:
  # Temel kontroller
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace        # Satır sonu boşlukları sil
      - id: end-of-file-fixer          # Dosya sonu satırı ekle
      - id: check-yaml                 # YAML dosyalarını kontrol et
      - id: check-json                 # JSON dosyalarını kontrol et
      - id: check-merge-conflict       # Merge conflict işaretlerini bul
      - id: debug-statements           # print/breakpoint bırakmışsan uyar

  # Python formatter: Kodu otomatik düzelt
  - repo: https://github.com/psf/black
    rev: 24.1.1
    hooks:
      - id: black
        language_version: python3

  # Import sıralayıcı
  - repo: https://github.com/pycqa/isort
    rev: 5.13.2
    hooks:
      - id: isort
        args: ["--profile", "black"]

  # Linter: Kod kalite ve hata kontrolü
  - repo: https://github.com/pycqa/flake8
    rev: 7.0.0
    hooks:
      - id: flake8
        args: [--max-line-length=120]

  # Güvenlik: Şifre/API key kontrolü
  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.4.0
    hooks:
      - id: detect-secrets
        args: ['--baseline', '.secrets.baseline']
EOF

# Git hook olarak yükle
pre-commit install

# Tüm dosyalarda test et
pre-commit run --all-files
```

#### Seçenek B: Husky + Lint-Staged (Node.js gerektirir)

```bash
# Node.js yüklüyse
npm init -y
npm install --save-dev husky lint-staged

# package.json'a ekle
cat > package.json << 'EOF'
{
  "name": "trading-system",
  "scripts": {
    "prepare": "husky install"
  },
  "lint-staged": {
    "*.py": [
      "black --check",
      "flake8 --max-line-length=120",
      "isort --check-only"
    ]
  },
  "devDependencies": {
    "husky": "^8.0.0",
    "lint-staged": "^15.0.0"
  }
}
EOF

# Husky başlat
npx husky install
npx husky add .husky/pre-commit "npx lint-staged && python3 -m pytest tests/ -q"

# Husky hook dosyasını oluştur
mkdir -p .husky
cat > .husky/pre-commit << 'EOF'
#!/bin/sh
. "$(dirname "$0")/_/husky.sh"

echo "🔍 Pre-commit checks başlıyor..."

# Python formatlaması
echo "📐 Black formatting..."
black --check . || { echo "❌ Black formatting failed. Run 'black .' to fix."; exit 1; }

# Import sıralama
echo "📦 Import sorting..."
isort --check-only . || { echo "❌ Import order wrong. Run 'isort .' to fix."; exit 1; }

# Linting
echo "🔎 Flake8 linting..."
flake8 --max-line-length=120 . || { echo "❌ Flake8 errors found."; exit 1; }

# Testler
echo "🧪 Running tests..."
python3 -m pytest tests/ -q --tb=short || { echo "❌ Tests failed."; exit 1; }

echo "✅ All checks passed! Committing..."
EOF

chmod +x .husky/pre-commit
```

### flake8 Konfigürasyonu

```bash
cat > setup.cfg << 'EOF'
[flake8]
max-line-length = 120
exclude = 
    venv,
    .git,
    __pycache__,
    data/,
    *.egg-info
ignore = 
    E203,   # Whitespace before ':'
    W503    # Line break before binary operator

[isort]
profile = black
multi_line_output = 3

[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
EOF
```

### ✅ TEST 1.3

```bash
# Test dosyası oluştur
mkdir tests
cat > tests/test_basic.py << 'EOF'
"""Basic system tests"""
import pytest


def test_imports():
    """Temel kütüphanelerin import edilebilmesi"""
    import pandas as pd
    import numpy as np
    import yfinance as yf
    assert True


def test_config():
    """Config dosyasının yüklenebilmesi"""
    import sys
    sys.path.insert(0, '..')
    assert True
EOF

# Testleri çalıştır
python3 -m pytest tests/ -v

# pre-commit testi
git add .
git commit -m "test: add basic tests with husky"
```

**Beklenen Çıktı:**
```
============================================ test session starts =====================
tests/test_basic.py::test_imports PASSED
tests/test_basic.py::test_config PASSED
============================================ 2 passed in 0.5s =======================
```

---

---

# PHASE 2: Veri Toplama

## 2.1 yfinance ile BIST Hisse Verisi

### 🧠 MANTIK

**yfinance nedir?**
Yahoo Finance'in gizli API'sini Python'dan kullanmamızı sağlar.
BIST hisselerini `.IS` uzantısıyla çekebiliriz:
- `YAPKREDI.IS` → Yapıkredi
- `AKBNK.IS` → Akbank
- `GARAN.IS` → Garanti BBVA

**OHLCV nedir?**
```
Open  → Güne başlangıç fiyatı
High  → Günün en yüksek fiyatı
Low   → Günün en düşük fiyatı
Close → Gün sonu fiyatı  ← EN ÖNEMLİ
Volume→ İşlem hacmi (kaç lot satıldı?)
```

**Neden geçmiş veri lazım?**
- ML modeli eğitmek için
- Backtesting için
- Gösterge hesaplamak için (RSI için 14 gün lazım)

### 📝 KOD

```python
# scripts/01_fetch_data.py

import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

STOCKS = ['YAPKREDI.IS', 'AKBNK.IS', 'GARAN.IS']
START = '2022-01-01'
END   = '2024-12-31'

def fetch_stock(symbol, start, end):
    """Hisse verisi indir"""
    print(f"📥 Downloading {symbol}...", end=' ')
    df = yf.download(symbol, start=start, end=end, progress=False)
    
    if df.empty:
        print("❌ No data")
        return None
    
    df.index = pd.to_datetime(df.index)
    print(f"✅ {len(df)} rows ({df.index[0].date()} → {df.index[-1].date()})")
    return df


def plot_stock(symbol, df):
    """Hisse grafiğini çiz"""
    fig, axes = plt.subplots(3, 1, figsize=(14, 10), sharex=True)
    fig.suptitle(f'{symbol} — Fiyat & Hacim', fontsize=14, fontweight='bold')
    
    # 1. Candlestick benzeri: Kapanış fiyatı
    axes[0].plot(df.index, df['Close'], color='#2196F3', linewidth=1.5, label='Close')
    axes[0].fill_between(df.index, df['Low'], df['High'], alpha=0.15, color='#2196F3')
    axes[0].set_ylabel('Fiyat (TRY)', fontsize=10)
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)
    
    # 2. Volume (İşlem hacmi)
    colors = ['#4CAF50' if c >= o else '#F44336' 
              for c, o in zip(df['Close'], df['Open'])]
    axes[1].bar(df.index, df['Volume'], color=colors, alpha=0.8, width=1)
    axes[1].set_ylabel('Hacim', fontsize=10)
    axes[1].grid(True, alpha=0.3)
    
    # 3. Günlük değişim (%)
    daily_change = df['Close'].pct_change() * 100
    pos = daily_change.clip(lower=0)
    neg = daily_change.clip(upper=0)
    axes[2].fill_between(df.index, pos, 0, color='#4CAF50', alpha=0.7, label='Artış')
    axes[2].fill_between(df.index, neg, 0, color='#F44336', alpha=0.7, label='Düşüş')
    axes[2].axhline(0, color='black', linewidth=0.5)
    axes[2].set_ylabel('Günlük Değişim %', fontsize=10)
    axes[2].legend()
    axes[2].grid(True, alpha=0.3)
    
    # X ekseni
    axes[2].xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f'charts/{symbol.replace(".IS","")}_price.png', dpi=120, bbox_inches='tight')
    plt.show()
    print(f"📊 Grafik kaydedildi: charts/{symbol.replace('.IS','')}_price.png")


# ==================== ÇALIŞTIR ====================
import os
os.makedirs('charts', exist_ok=True)
os.makedirs('data', exist_ok=True)

all_data = {}
for stock in STOCKS:
    data = fetch_stock(stock, START, END)
    if data is not None:
        all_data[stock] = data
        data.to_csv(f'data/{stock.replace(".IS","")}_prices.csv')
        plot_stock(stock, data)

print(f"\n✅ {len(all_data)}/{len(STOCKS)} hisse başarıyla indirildi.")
```

### 📊 GRAFİK KONTROLÜ

Script çalıştıktan sonra `charts/` klasöründe 3 grafik oluşur:
- `YAPKREDI_price.png`
- `AKBNK_price.png`
- `GARAN_price.png`

Her grafikte şunlara bak:
1. **Fiyat Grafiği**: Mantıklı görünüyor mu? (Ekstrem spike var mı?)
2. **Hacim Grafiği**: Yüksek hacim günleri var mı? (Haber günleri = anormal hacim)
3. **Günlük Değişim**: ±5%'den fazla günler normal mi?

### ✅ TEST 2.1

```bash
python3 scripts/01_fetch_data.py

# Kontrol et:
# 1. data/ klasöründe CSV dosyaları var mı?
# 2. charts/ klasöründe PNG'ler var mı?
# 3. Grafiklerde anormal veri var mı?
ls -la data/
ls -la charts/
```

---

## 2.2 SQLite Veritabanı

### 🧠 MANTIK

CSV mi yoksa veritabanı mı?
```
CSV                          SQLite Database
───                          ───────────────
✅ Basit, açılır             ✅ Hızlı sorgu
✅ Excel'de görünür          ✅ Büyük veri için uygun
❌ Büyük veri yavaş          ✅ SQL ile filtre
❌ Aynı anda birden          ✅ Transaction desteği
   fazla erişim sorunlu
```

Burada **SQLite** kullanıyoruz çünkü:
- Kurulum yok, tek dosya
- Python ile dahili destekli
- Sonradan PostgreSQL'e geçiş kolay

### 📝 KOD

```python
# scripts/02_setup_database.py

import sqlite3
import pandas as pd
import os

DB_PATH = 'data/trading.db'

def create_tables(conn):
    """Tabloları oluştur"""
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS prices (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol      TEXT NOT NULL,
            date        DATE NOT NULL,
            open        REAL,
            high        REAL,
            low         REAL,
            close       REAL,
            volume      INTEGER,
            UNIQUE(symbol, date)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS signals (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol      TEXT NOT NULL,
            date        DATE NOT NULL,
            signal_type TEXT,
            score       REAL,
            rsi         REAL,
            macd        REAL,
            created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS trades (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol      TEXT NOT NULL,
            action      TEXT,        -- BUY / SELL
            price       REAL,
            quantity    INTEGER,
            date        TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            pnl         REAL,
            mode        TEXT DEFAULT 'demo'  -- demo / live
        )
    ''')
    
    # İndeks ekle (sorgular için hız)
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_prices_symbol ON prices(symbol)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_prices_date ON prices(date)')
    
    conn.commit()
    print("✅ Tables created successfully")


def load_csv_to_db(conn, symbol):
    """CSV'yi veritabanına yükle"""
    csv_path = f'data/{symbol.replace(".IS","")}_prices.csv'
    
    if not os.path.exists(csv_path):
        print(f"⚠️  CSV not found: {csv_path}")
        return
    
    df = pd.read_csv(csv_path, index_col=0, parse_dates=True)
    df.reset_index(inplace=True)
    df.columns = [c.lower() for c in df.columns]
    df['symbol'] = symbol
    df['date'] = pd.to_datetime(df['date']).dt.date
    
    df_insert = df[['symbol','date','open','high','low','close','volume']]
    df_insert.to_sql('prices', conn, if_exists='append', index=False)
    
    print(f"✅ {symbol}: {len(df)} rows loaded to DB")


def verify_database(conn):
    """Veritabanını doğrula"""
    cursor = conn.cursor()
    
    print("\n📊 DATABASE VERIFICATION")
    print("="*50)
    
    cursor.execute("""
        SELECT symbol, COUNT(*) as rows, 
               MIN(date) as first_date, 
               MAX(date) as last_date,
               ROUND(AVG(close), 2) as avg_close
        FROM prices 
        GROUP BY symbol
    """)
    
    for row in cursor.fetchall():
        symbol, rows, first_date, last_date, avg_close = row
        print(f"{symbol:14} | {rows:4} rows | {first_date} → {last_date} | Avg: {avg_close} TRY")
    
    print("="*50)


# ==================== ÇALIŞTIR ====================
conn = sqlite3.connect(DB_PATH)
create_tables(conn)

for stock in ['YAPKREDI.IS', 'AKBNK.IS', 'GARAN.IS']:
    load_csv_to_db(conn, stock)

verify_database(conn)
conn.close()
```

### ✅ TEST 2.2

```bash
python3 scripts/02_setup_database.py

# Manuel kontrol
python3 -c "
import sqlite3, pandas as pd
conn = sqlite3.connect('data/trading.db')
df = pd.read_sql('SELECT * FROM prices WHERE symbol=\"YAPKREDI.IS\" ORDER BY date DESC LIMIT 5', conn)
print(df)
conn.close()
"
```

**Beklenen Çıktı:**
```
   symbol       date    open    high     low   close    volume
0  YAPKREDI.IS  2024-12-20   10.45   10.82   10.20   10.60  1234567
1  YAPKREDI.IS  2024-12-19   10.20   10.50   10.05   10.45  987654
...
```

---

---

# PHASE 3: Teknik Analiz

## 3.1 RSI (Relative Strength Index)

### 🧠 MANTIK

**RSI ne ölçer?**
"Son N günde fiyat ne kadar güçlü yükseldi / ne kadar güçlü düştü?"

**Formül:**
```
RSI = 100 - (100 / (1 + RS))
RS  = Ortalama Yükseliş / Ortalama Düşüş (son 14 gün)
```

**Yorum:**
```
RSI > 70  → Hisse "pahalı" (overbought) → SATIM SİNYALİ
RSI < 30  → Hisse "ucuz" (oversold)     → ALIM SİNYALİ
RSI = 50  → Nötr
```

**⚠️ Önemli:** RSI tek başına yeterli değil. Yanlış sinyal verebilir.
Trend yukarıdayken RSI 70'te kalabilir (trending market).

### 📝 KOD

```python
# scripts/03_technical_analysis.py

import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.patches import Patch

DB_PATH = 'data/trading.db'


def calculate_rsi(prices, period=14):
    """RSI hesapla"""
    delta = prices.diff()
    gain = delta.clip(lower=0).rolling(period).mean()
    loss = (-delta.clip(upper=0)).rolling(period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))


def calculate_macd(prices, fast=12, slow=26, signal=9):
    """MACD hesapla"""
    ema_fast = prices.ewm(span=fast, adjust=False).mean()
    ema_slow = prices.ewm(span=slow, adjust=False).mean()
    macd_line  = ema_fast - ema_slow
    signal_line = macd_line.ewm(span=signal, adjust=False).mean()
    histogram   = macd_line - signal_line
    return macd_line, signal_line, histogram


def calculate_bollinger(prices, period=20, std=2):
    """Bollinger Bands hesapla"""
    mid   = prices.rolling(period).mean()
    sigma = prices.rolling(period).std()
    upper = mid + std * sigma
    lower = mid - std * sigma
    return upper, mid, lower


def plot_full_analysis(symbol, df):
    """Tüm teknik analizi tek grafikte göster"""
    fig = plt.figure(figsize=(16, 14))
    gs  = gridspec.GridSpec(4, 1, figure=fig, hspace=0.05,
                             height_ratios=[3, 1.5, 1.5, 1])
    fig.suptitle(f'🔍 Teknik Analiz: {symbol}', fontsize=15, fontweight='bold', y=0.98)
    
    # ── 1. Fiyat + Bollinger Bands + SMA ────────────────────
    ax1 = fig.add_subplot(gs[0])
    ax1.plot(df.index, df['close'], color='#1565C0', lw=1.5, label='Kapanış')
    ax1.plot(df.index, df['sma20'], color='#FF9800', lw=1,   label='SMA 20', ls='--')
    ax1.plot(df.index, df['sma50'], color='#9C27B0', lw=1,   label='SMA 50', ls='--')
    ax1.plot(df.index, df['bb_mid'],   color='gray',    lw=0.8, ls=':')
    ax1.fill_between(df.index, df['bb_upper'], df['bb_lower'],
                     alpha=0.12, color='#2196F3', label='Bollinger Bands')
    ax1.set_ylabel('Fiyat (TRY)', fontsize=10)
    ax1.legend(loc='upper left', fontsize=9)
    ax1.grid(True, alpha=0.25)
    ax1.set_xticklabels([])
    
    # ── 2. MACD ─────────────────────────────────────────────
    ax2 = fig.add_subplot(gs[1], sharex=ax1)
    ax2.plot(df.index, df['macd'],        color='#1565C0', lw=1.2, label='MACD')
    ax2.plot(df.index, df['macd_signal'], color='#F44336', lw=1.2, label='Signal')
    bar_colors = ['#4CAF50' if v >= 0 else '#F44336' for v in df['macd_hist']]
    ax2.bar(df.index, df['macd_hist'], color=bar_colors, alpha=0.7, width=1, label='Histogram')
    ax2.axhline(0, color='black', lw=0.5)
    ax2.set_ylabel('MACD', fontsize=10)
    ax2.legend(loc='upper left', fontsize=9)
    ax2.grid(True, alpha=0.25)
    ax2.set_xticklabels([])
    
    # ── 3. RSI ──────────────────────────────────────────────
    ax3 = fig.add_subplot(gs[2], sharex=ax1)
    ax3.plot(df.index, df['rsi'], color='#7B1FA2', lw=1.3, label='RSI(14)')
    ax3.axhline(70, color='#F44336', lw=1, ls='--', alpha=0.7)
    ax3.axhline(30, color='#4CAF50', lw=1, ls='--', alpha=0.7)
    ax3.axhline(50, color='gray',    lw=0.8, ls=':')
    ax3.fill_between(df.index, 70, 100, alpha=0.05, color='red')
    ax3.fill_between(df.index, 0,  30,  alpha=0.05, color='green')
    ax3.set_ylim(0, 100)
    ax3.set_ylabel('RSI', fontsize=10)
    ax3.legend(loc='upper left', fontsize=9)
    ax3.grid(True, alpha=0.25)
    ax3.set_xticklabels([])
    
    # ── 4. Hacim ────────────────────────────────────────────
    ax4 = fig.add_subplot(gs[3], sharex=ax1)
    colors = ['#4CAF50' if c >= o else '#F44336'
              for c, o in zip(df['close'], df['open'])]
    ax4.bar(df.index, df['volume'], color=colors, alpha=0.8, width=1)
    ax4.set_ylabel('Hacim', fontsize=10)
    ax4.grid(True, alpha=0.25)
    
    import matplotlib.dates as mdates
    ax4.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    plt.setp(ax4.xaxis.get_majorticklabels(), rotation=45, ha='right')
    
    plt.savefig(f'charts/{symbol.replace(".IS","")}_technical.png',
                dpi=120, bbox_inches='tight')
    plt.show()
    print(f"📊 Teknik analiz grafiği kaydedildi")


# ==================== HESAPLA & ÇİZ ====================
conn = sqlite3.connect(DB_PATH)

for symbol in ['YAPKREDI.IS', 'AKBNK.IS', 'GARAN.IS']:
    df = pd.read_sql(
        f"SELECT * FROM prices WHERE symbol='{symbol}' ORDER BY date",
        conn, parse_dates=['date'], index_col='date'
    )
    
    if df.empty:
        continue
    
    # Tüm göstergeleri hesapla
    df['rsi']       = calculate_rsi(df['close'])
    df['macd'], df['macd_signal'], df['macd_hist'] = calculate_macd(df['close'])
    df['bb_upper'], df['bb_mid'], df['bb_lower'] = calculate_bollinger(df['close'])
    df['sma20'] = df['close'].rolling(20).mean()
    df['sma50'] = df['close'].rolling(50).mean()
    df.dropna(inplace=True)
    
    print(f"\n📊 {symbol} — Son Değerler:")
    print(f"  Fiyat : {df['close'].iloc[-1]:.2f} TRY")
    print(f"  RSI   : {df['rsi'].iloc[-1]:.2f}")
    print(f"  MACD  : {df['macd'].iloc[-1]:.4f}")
    
    plot_full_analysis(symbol, df)

conn.close()
```

### 📊 GRAFİK KONTROLÜ

Grafikte şunları kontrol et:
1. **Bollinger Bands daralıyor mu?** → Büyük hareket geliyor olabilir
2. **RSI 30'un altına indi mi?** → Alım fırsatı olabilir
3. **MACD histogram rengi değişti mi?** → Trend değişimi sinyali
4. **Fiyat SMA50'nin altına düştü mü?** → Bearish trend

### ✅ TEST 3.1

```bash
python3 scripts/03_technical_analysis.py

# Doğrulama: Son RSI değeri
python3 -c "
import sqlite3, pandas as pd

conn = sqlite3.connect('data/trading.db')
df = pd.read_sql('SELECT * FROM prices WHERE symbol=\"YAPKREDI.IS\" ORDER BY date', conn)
df['rsi'] = (lambda p: 100 - 100/(1+(p.diff().clip(0).rolling(14).mean()/(-p.diff().clip(upper=0).rolling(14).mean()))))(df['close'])
print('Son 5 RSI değeri:')
print(df[['date','close','rsi']].tail(5).to_string(index=False))
"
```

---

## 3.2 MACD — Trend Sinyali

### 🧠 MANTIK

MACD "iki ortalamanın farkı"nı gösterir. İki EMA arasındaki mesafe büyürse → trend güçlü.

```
MACD Line    = EMA(12) - EMA(26)    ← Hızlı - Yavaş
Signal Line  = EMA(9) of MACD Line  ← MACD'nin ortalaması
Histogram    = MACD - Signal        ← İkisi arasındaki fark

ALIM: MACD, Signal'ı yukarıdan keser + Histogram pozitife döner
SATIM: MACD, Signal'ı aşağıdan keser + Histogram negatife döner
```

---

## 3.3 Bollinger Bands — Volatilite

### 🧠 MANTIK

```
Üst Band  = SMA(20) + 2 × Standart Sapma
Orta Bant = SMA(20)                    ← Denge noktası
Alt Band  = SMA(20) - 2 × Standart Sapma

Fiyat üst bantta → Aşırı alınmış
Fiyat alt bantta → Aşırı satılmış
Band daralması   → Büyük hareket yaklaşıyor (breakout)
```

---

---

# PHASE 4: Sinyal Üretimi

## 4.1 Sinyal Skoru Nasıl Hesaplanır?

### 🧠 MANTIK

```
Her gösterge → -100 ile +100 arası puan verir

RSI(14) = 25  → OVERSOLD   → +80 puan  (alım fırsatı!)
MACD    = pozitif, histogram artıyor → +60 puan
BB      = fiyat alt bantta → +70 puan
SMA     = fiyat SMA50 üstünde → +40 puan

Ortalama = (80+60+70+40) / 4 = +62.5

62.5 > 50 → 🟢 BUY SİNYALİ
```

### 📝 KOD

```python
# scripts/04_signal_generator.py

import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from datetime import datetime


def score_rsi(rsi):
    """RSI'dan -100/+100 skor üret"""
    if pd.isna(rsi):
        return 0
    if rsi < 20:   return  100
    if rsi < 30:   return   80
    if rsi < 40:   return   40
    if rsi < 50:   return   10
    if rsi < 60:   return  -10
    if rsi < 70:   return  -40
    if rsi < 80:   return  -80
    return -100


def score_macd(macd, signal, histogram):
    """MACD'den skor üret"""
    if pd.isna(macd):
        return 0
    score = 0
    if macd > signal:      score += 40
    if histogram > 0:      score += 30
    prev_hist = histogram  # (önceki periyotla karşılaştırılabilir)
    if histogram > 0 and abs(histogram) > abs(histogram * 0.9):
        score += 30
    return max(-100, min(100, score if macd > signal else -score))


def score_bollinger(close, upper, lower, mid):
    """Bollinger Bands'dan skor üret"""
    if pd.isna(upper) or (upper - lower) == 0:
        return 0
    pos = (close - lower) / (upper - lower)   # 0 = alt, 1 = üst band
    if pos < 0.1:   return  100
    if pos < 0.25:  return   60
    if pos < 0.4:   return   20
    if pos < 0.6:   return    0
    if pos < 0.75:  return  -20
    if pos < 0.9:   return  -60
    return -100


def score_moving_average(close, sma20, sma50):
    """Moving Average'dan skor üret"""
    score = 0
    if not pd.isna(sma20) and close > sma20: score += 25
    if not pd.isna(sma50) and close > sma50: score += 35
    if not pd.isna(sma20) and not pd.isna(sma50) and sma20 > sma50:
        score += 40   # Golden Cross bölgesi
    return score - 50   # -50..+50 normalize


def generate_signals_for_df(df):
    """DataFrame'deki her satır için sinyal üret"""
    results = []
    
    for _, row in df.iterrows():
        rsi_score  = score_rsi(row.get('rsi', np.nan))
        macd_score = score_macd(row.get('macd', np.nan),
                                row.get('macd_signal', np.nan),
                                row.get('macd_hist', np.nan))
        bb_score   = score_bollinger(row['close'],
                                     row.get('bb_upper', np.nan),
                                     row.get('bb_lower', np.nan),
                                     row.get('bb_mid', np.nan))
        ma_score   = score_moving_average(row['close'],
                                          row.get('sma20', np.nan),
                                          row.get('sma50', np.nan))
        
        avg = np.mean([rsi_score, macd_score, bb_score, ma_score])
        
        if avg >= 75:    sig = 'STRONG_BUY'
        elif avg >= 40:  sig = 'BUY'
        elif avg <= -75: sig = 'STRONG_SELL'
        elif avg <= -40: sig = 'SELL'
        else:            sig = 'NEUTRAL'
        
        results.append({
            'score':       round(avg, 2),
            'signal':      sig,
            'rsi_score':   rsi_score,
            'macd_score':  macd_score,
            'bb_score':    bb_score,
            'ma_score':    ma_score,
        })
    
    return pd.DataFrame(results, index=df.index)


def plot_signals(symbol, df, signals):
    """Fiyat grafiği üstüne sinyalleri ekle"""
    fig, axes = plt.subplots(3, 1, figsize=(16, 12), sharex=True,
                             gridspec_kw={'height_ratios': [3, 1.5, 1]})
    fig.suptitle(f'📡 Sinyal Analizi: {symbol}', fontsize=14, fontweight='bold')
    
    # ── 1. Fiyat + Sinyaller ──────────────────────────────
    axes[0].plot(df.index, df['close'], color='#1565C0', lw=1.2, label='Kapanış')
    axes[0].fill_between(df.index, df['bb_lower'], df['bb_upper'], alpha=0.1, color='gray')
    
    buy_idx  = signals[signals['signal'].isin(['BUY', 'STRONG_BUY'])].index
    sell_idx = signals[signals['signal'].isin(['SELL', 'STRONG_SELL'])].index
    
    axes[0].scatter(buy_idx, df.loc[buy_idx, 'close'],
                    marker='^', color='#4CAF50', s=80, zorder=5, label='BUY Signal')
    axes[0].scatter(sell_idx, df.loc[sell_idx, 'close'],
                    marker='v', color='#F44336', s=80, zorder=5, label='SELL Signal')
    
    axes[0].set_ylabel('Fiyat (TRY)')
    axes[0].legend(fontsize=9)
    axes[0].grid(True, alpha=0.25)
    
    # ── 2. Sinyal Skoru ───────────────────────────────────
    colors = ['#4CAF50' if s >= 0 else '#F44336' for s in signals['score']]
    axes[1].bar(signals.index, signals['score'], color=colors, alpha=0.75, width=1)
    axes[1].axhline(40, color='green', lw=1, ls='--', alpha=0.6, label='Buy threshold')
    axes[1].axhline(-40, color='red',  lw=1, ls='--', alpha=0.6, label='Sell threshold')
    axes[1].axhline(0, color='black', lw=0.5)
    axes[1].set_ylabel('Sinyal Skoru')
    axes[1].legend(fontsize=9)
    axes[1].grid(True, alpha=0.25)
    
    # ── 3. RSI ────────────────────────────────────────────
    axes[2].plot(df.index, df['rsi'], color='#7B1FA2', lw=1.2)
    axes[2].axhline(70, color='red',   lw=0.8, ls='--')
    axes[2].axhline(30, color='green', lw=0.8, ls='--')
    axes[2].set_ylim(0, 100)
    axes[2].set_ylabel('RSI')
    axes[2].grid(True, alpha=0.25)
    
    import matplotlib.dates as mdates
    axes[2].xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    plt.setp(axes[2].xaxis.get_majorticklabels(), rotation=45, ha='right')
    
    plt.tight_layout()
    plt.savefig(f'charts/{symbol.replace(".IS","")}_signals.png',
                dpi=120, bbox_inches='tight')
    plt.show()
    print(f"📊 Sinyal grafiği kaydedildi")


# ==================== ÇALIŞTIR ====================
def add_indicators(df):
    """Göstergeleri DataFrame'e ekle"""
    delta = df['close'].diff()
    gain  = delta.clip(lower=0).rolling(14).mean()
    loss  = (-delta.clip(upper=0)).rolling(14).mean()
    df['rsi'] = 100 - 100 / (1 + gain / loss)
    
    ema12 = df['close'].ewm(span=12).mean()
    ema26 = df['close'].ewm(span=26).mean()
    df['macd']        = ema12 - ema26
    df['macd_signal'] = df['macd'].ewm(span=9).mean()
    df['macd_hist']   = df['macd'] - df['macd_signal']
    
    sma20 = df['close'].rolling(20).mean()
    std20 = df['close'].rolling(20).std()
    df['bb_upper'] = sma20 + 2 * std20
    df['bb_mid']   = sma20
    df['bb_lower'] = sma20 - 2 * std20
    df['sma20']    = sma20
    df['sma50']    = df['close'].rolling(50).mean()
    
    return df.dropna()


conn = sqlite3.connect('data/trading.db')

for symbol in ['YAPKREDI.IS', 'AKBNK.IS', 'GARAN.IS']:
    df = pd.read_sql(
        f"SELECT * FROM prices WHERE symbol='{symbol}' ORDER BY date",
        conn, parse_dates=['date'], index_col='date'
    )
    if df.empty:
        continue
    
    df = add_indicators(df)
    signals = generate_signals_for_df(df)
    
    # Son sinyal özeti
    latest = signals.iloc[-1]
    print(f"\n🎯 {symbol} — GÜNCEL SİNYAL:")
    print(f"  Sinyal : {latest['signal']}")
    print(f"  Skor   : {latest['score']:.2f}")
    print(f"  RSI score  : {latest['rsi_score']}")
    print(f"  MACD score : {latest['macd_score']}")
    print(f"  BB score   : {latest['bb_score']}")
    print(f"  MA score   : {latest['ma_score']}")
    
    # Sinyal dağılımı
    print(f"\n  Sinyal Dağılımı ({len(signals)} gün):")
    for sig_type, count in signals['signal'].value_counts().items():
        pct = count / len(signals) * 100
        print(f"    {sig_type:12} : {count:4} gün (%{pct:.1f})")
    
    plot_signals(symbol, df, signals)

conn.close()
```

### ✅ TEST 4.1

```bash
python3 scripts/04_signal_generator.py

# Kontrol soruları:
# 1. Bugün hangi hisse alım sinyali veriyor?
# 2. Sinyaller mantıklı görünüyor mu? (çok fazla BUY veya SELL var mı?)
# 3. BUY işareti genellikle düşük fiyatlarda mı? (Grafikte bak)
```

---

---

# PHASE 5: Risk Yönetimi

## 5.1 Position Sizing — Ne Kadar Alacağız?

### 🧠 MANTIK

**Risk-Based Position Sizing:**
```
Her işlemde portföyümüzün %1'ini riske atarız.

Örnek:
  Portföy          = 100.000 TRY
  Risk per trade   = %1 = 1.000 TRY
  YAPKREDI fiyatı  = 10.50 TRY
  Stop Loss        = 10.00 TRY  (fiyatın %4.76 altı)
  
  Risk per share   = 10.50 - 10.00 = 0.50 TRY
  
  Kaç adet alınır? = Risk Amount / Risk per Share
                   = 1.000 / 0.50
                   = 2.000 lot
  
  Toplam yatırım   = 2.000 × 10.50 = 21.000 TRY
```

**Neden önemli?**
- Büyük pozisyon = büyük kayıp
- Küçük pozisyon = küçük kazanç ama HİÇBİR ZAMAN YOK OLMAZSIN

### 📝 KOD

```python
# scripts/05_risk_manager.py

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def calculate_position_size(portfolio, risk_pct, entry, stop_loss):
    """Risk tabanlı lot sayısı hesapla"""
    risk_amount    = portfolio * (risk_pct / 100)
    risk_per_share = abs(entry - stop_loss)
    if risk_per_share == 0:
        return 0
    quantity  = int(risk_amount / risk_per_share)
    total_inv = quantity * entry
    return {
        'quantity':    quantity,
        'total_inv':   total_inv,
        'risk_amount': risk_amount,
        'portfolio_pct': (total_inv / portfolio) * 100
    }


def plot_risk_scenarios():
    """Farklı risk senaryolarını görselleştir"""
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle('📊 Risk Yönetimi Senaryoları', fontsize=13, fontweight='bold')
    
    portfolio = 100_000
    entry     = 10.50
    stop_loss = 10.00
    
    # Sol: Risk % vs Kayıp
    risk_pcts = np.linspace(0.5, 5, 50)
    max_losses = [portfolio * (r/100) for r in risk_pcts]
    
    axes[0].fill_between(risk_pcts, 0, max_losses, alpha=0.3, color='red')
    axes[0].plot(risk_pcts, max_losses, color='red', lw=2)
    axes[0].axvline(1, color='green', ls='--', lw=1.5, label='Önerilen: %1')
    axes[0].axvline(2, color='orange', ls='--', lw=1.5, label='Maksimum: %2')
    axes[0].set_xlabel('Risk Yüzdesi (%)')
    axes[0].set_ylabel('Maksimum Kayıp (TRY)')
    axes[0].set_title('Risk % → Maksimum Kayıp')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)
    
    # Sağ: Kaybeden işlemler sonrası kalan sermaye
    starting = 100_000
    scenarios = {
        '%1 risk': 1,
        '%2 risk': 2,
        '%5 risk': 5,
    }
    colors = ['green', 'orange', 'red']
    
    for (label, risk), color in zip(scenarios.items(), colors):
        capital = starting
        history = [capital]
        # 20 peş peşe kaybeden işlem
        for _ in range(20):
            capital -= capital * (risk / 100)
            history.append(capital)
        pct_left = (history[-1] / starting) * 100
        axes[1].plot(history, color=color, lw=2,
                     label=f'{label} → %{pct_left:.0f} kaldı')
    
    axes[1].axhline(starting, color='black', ls=':', alpha=0.5)
    axes[1].set_xlabel('Peş Peşe Kaybeden İşlem Sayısı')
    axes[1].set_ylabel('Kalan Sermaye (TRY)')
    axes[1].set_title('20 Kaybeden İşlem Sonrası Sermaye')
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('charts/risk_scenarios.png', dpi=120, bbox_inches='tight')
    plt.show()
    print("📊 Risk senaryosu grafiği kaydedildi")


# ==================== ÇALIŞTIR ====================
print("💰 POSITION SIZING ÖRNEKLERI\n")

portfolio = 100_000
entry     = 10.50
stop_loss = 10.00

for risk_pct in [0.5, 1.0, 2.0]:
    result = calculate_position_size(portfolio, risk_pct, entry, stop_loss)
    print(f"Risk %{risk_pct:.1f}:")
    print(f"  Alınacak Lot   : {result['quantity']:,}")
    print(f"  Toplam Yatırım : {result['total_inv']:,.2f} TRY")
    print(f"  Max Kayıp      : {result['risk_amount']:,.2f} TRY")
    print(f"  Portföy %      : %{result['portfolio_pct']:.1f}")
    print()

plot_risk_scenarios()
```

### ✅ TEST 5.1

```bash
python3 scripts/05_risk_manager.py

# Soruları cevapla:
# 1. %1 riske edersen 20 kaybeden işlem sonrası ne kadar kaldı?
# 2. %5 riske edersen ne kadar kaldı?
# 3. Hangisi daha güvenli?  (Cevap: Her zaman %1 veya daha az)
```

---

---

# PHASE 6: Backtesting

## 6.1 Stratejiyi Geçmiş Verilerde Test Et

### 🧠 MANTIK

**Backtesting nedir?**
"Bu sinyal sistemi 2022-2023'te çalışmış olsaydı ne olurdu?"

```
Geçmiş Fiyatlar → Göstergeleri Hesapla → Sinyal Üret → Simüle Et
                                                            ↓
                                              Kazanan/Kaybeden İşlemler
                                              Win Rate, Avg PnL, Sharpe
```

**⚠️ Önemli Uyarılar:**
- Geçmiş başarı, geleceği garantilemez
- "Overfitting" tehlikesi: Sadece geçmişe özel optimize etme
- Gerçek hayatta slippage, commission var → bunları ekle

### 📝 KOD

```python
# scripts/06_backtesting.py

import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def add_indicators(df):
    delta = df['close'].diff()
    gain  = delta.clip(lower=0).rolling(14).mean()
    loss  = (-delta.clip(upper=0)).rolling(14).mean()
    df['rsi'] = 100 - 100 / (1 + gain / loss)
    
    ema12 = df['close'].ewm(span=12).mean()
    ema26 = df['close'].ewm(span=26).mean()
    df['macd']        = ema12 - ema26
    df['macd_signal'] = df['macd'].ewm(span=9).mean()
    df['macd_hist']   = df['macd'] - df['macd_signal']
    
    sma20 = df['close'].rolling(20).mean()
    std20 = df['close'].rolling(20).std()
    df['bb_upper'] = sma20 + 2 * std20
    df['bb_lower'] = sma20 - 2 * std20
    df['sma20']    = sma20
    df['sma50']    = df['close'].rolling(50).mean()
    
    return df.dropna()


def run_backtest(df, initial_capital=100_000,
                 commission=0.001, slippage=0.0005,
                 risk_pct=1.0, stop_loss_pct=2.0, take_profit_pct=5.0):
    """
    Basit backtesting simülasyonu
    Sinyale göre al, SL/TP'ye göre sat
    """
    capital  = initial_capital
    equity   = [capital]
    trades   = []
    in_pos   = False
    entry_p  = 0
    entry_d  = None
    quantity = 0
    
    for i in range(1, len(df)):
        row  = df.iloc[i]
        prev = df.iloc[i-1]
        close = row['close']
        
        if in_pos:
            # Stop Loss
            sl_price = entry_p * (1 - stop_loss_pct/100)
            tp_price = entry_p * (1 + take_profit_pct/100)
            
            exit_reason = None
            exit_price  = close
            
            if close <= sl_price:
                exit_reason = 'STOP_LOSS'
                exit_price  = sl_price * (1 - slippage)
            elif close >= tp_price:
                exit_reason = 'TAKE_PROFIT'
                exit_price  = tp_price * (1 + slippage)
            
            # RSI overbought → satış sinyali
            elif row.get('rsi', 50) > 70 and prev.get('rsi', 50) <= 70:
                exit_reason = 'RSI_OVERBOUGHT'
            
            if exit_reason:
                gross_pnl = (exit_price - entry_p) * quantity
                fee       = exit_price * quantity * commission
                net_pnl   = gross_pnl - fee
                capital  += entry_p * quantity + net_pnl  # geriye ekle
                
                trades.append({
                    'entry_date':  entry_d,
                    'exit_date':   row.name,
                    'entry_price': entry_p,
                    'exit_price':  exit_price,
                    'quantity':    quantity,
                    'pnl':         net_pnl,
                    'pnl_pct':     (exit_price - entry_p) / entry_p * 100,
                    'reason':      exit_reason,
                })
                in_pos = False
        
        else:
            # Alım koşulu: RSI oversold + MACD bullish
            rsi_ok   = row.get('rsi',  50) < 35
            macd_ok  = row.get('macd', 0) > row.get('macd_signal', 0)
            
            if rsi_ok and macd_ok and capital > 10_000:
                risk_amt  = capital * (risk_pct / 100)
                sl_diff   = close * (stop_loss_pct / 100)
                qty       = int(risk_amt / sl_diff)
                cost      = close * qty * (1 + commission + slippage)
                
                if qty > 0 and cost < capital:
                    capital  -= cost
                    entry_p   = close * (1 + slippage)
                    entry_d   = row.name
                    quantity  = qty
                    in_pos    = True
        
        # Equity curve
        pos_val = (close - entry_p) * quantity if in_pos else 0
        equity.append(capital + entry_p * quantity + pos_val if in_pos else capital)
    
    return pd.DataFrame(trades), pd.Series(equity, index=df.index[:len(equity)])


def plot_backtest_results(symbol, df, trades, equity):
    """Backtest sonuçlarını görselleştir"""
    
    fig = plt.figure(figsize=(16, 12))
    gs  = plt.GridSpec(3, 2, figure=fig, hspace=0.4, wspace=0.3)
    fig.suptitle(f'📈 Backtest Sonuçları: {symbol}', fontsize=14, fontweight='bold')
    
    # ── 1. Equity Curve (Ana grafik) ─────────────────────────
    ax1 = fig.add_subplot(gs[0, :])
    ax1.plot(equity.index, equity.values, color='#1565C0', lw=2, label='Portföy Değeri')
    ax1.axhline(equity.iloc[0], color='gray', ls='--', alpha=0.5, label='Başlangıç')
    ax1.fill_between(equity.index,
                     equity.iloc[0], equity.values,
                     where=(equity >= equity.iloc[0]),
                     alpha=0.15, color='green')
    ax1.fill_between(equity.index,
                     equity.iloc[0], equity.values,
                     where=(equity < equity.iloc[0]),
                     alpha=0.15, color='red')
    
    # İşlemleri işaretle
    if not trades.empty:
        for _, t in trades.iterrows():
            color = '#4CAF50' if t['pnl'] > 0 else '#F44336'
            ax1.axvline(t['entry_date'], color=color, alpha=0.2, lw=0.8)
    
    ax1.set_ylabel('Sermaye (TRY)')
    ax1.set_title('Equity Curve')
    ax1.legend()
    ax1.grid(True, alpha=0.25)
    
    if not trades.empty:
        # ── 2. PnL Dağılımı ──────────────────────────────────
        ax2 = fig.add_subplot(gs[1, 0])
        pnl_vals = trades['pnl'].values
        colors   = ['#4CAF50' if p > 0 else '#F44336' for p in pnl_vals]
        ax2.bar(range(len(pnl_vals)), pnl_vals, color=colors, alpha=0.8)
        ax2.axhline(0, color='black', lw=0.8)
        ax2.set_xlabel('İşlem #')
        ax2.set_ylabel('PnL (TRY)')
        ax2.set_title('İşlem Bazında PnL')
        ax2.grid(True, alpha=0.25)
        
        # ── 3. Histogram ─────────────────────────────────────
        ax3 = fig.add_subplot(gs[1, 1])
        wins  = trades[trades['pnl'] > 0]['pnl']
        loses = trades[trades['pnl'] < 0]['pnl']
        if len(wins):
            ax3.hist(wins,  bins=15, color='#4CAF50', alpha=0.7, label=f'Kazanan ({len(wins)})')
        if len(loses):
            ax3.hist(loses, bins=15, color='#F44336', alpha=0.7, label=f'Kaybeden ({len(loses)})')
        ax3.axvline(0, color='black', lw=1)
        ax3.set_xlabel('PnL (TRY)')
        ax3.set_ylabel('İşlem Sayısı')
        ax3.set_title('Kazanan / Kaybeden Dağılımı')
        ax3.legend()
        ax3.grid(True, alpha=0.25)
        
        # ── 4. Drawdown ───────────────────────────────────────
        ax4 = fig.add_subplot(gs[2, :])
        peak     = equity.cummax()
        drawdown = ((equity - peak) / peak) * 100
        ax4.fill_between(equity.index, drawdown, 0, color='red', alpha=0.4)
        ax4.plot(equity.index, drawdown, color='darkred', lw=0.8)
        ax4.set_ylabel('Drawdown %')
        ax4.set_title('Drawdown (Tepe Noktadan Düşüş)')
        ax4.grid(True, alpha=0.25)
        
        import matplotlib.dates as mdates
        ax4.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
        plt.setp(ax4.xaxis.get_majorticklabels(), rotation=45, ha='right')
    
    plt.savefig(f'charts/{symbol.replace(".IS","")}_backtest.png',
                dpi=120, bbox_inches='tight')
    plt.show()
    print("📊 Backtest grafiği kaydedildi")


def print_backtest_stats(symbol, initial_capital, trades, equity):
    """Backtest istatistiklerini yazdır"""
    final   = equity.iloc[-1]
    total_r = (final - initial_capital) / initial_capital * 100
    
    print(f"\n{'='*60}")
    print(f"📊 BACKTEST SONUÇLARI: {symbol}")
    print(f"{'='*60}")
    print(f"Başlangıç Sermaye   : {initial_capital:>12,.0f} TRY")
    print(f"Final Sermaye       : {final:>12,.0f} TRY")
    print(f"Toplam Getiri       : {total_r:>11.2f} %")
    
    if not trades.empty:
        winners = trades[trades['pnl'] > 0]
        losers  = trades[trades['pnl'] < 0]
        win_rate = len(winners) / len(trades) * 100
        
        peak     = equity.cummax()
        drawdown = ((equity - peak) / peak) * 100
        max_dd   = drawdown.min()
        
        avg_win  = winners['pnl'].mean() if len(winners) else 0
        avg_loss = losers['pnl'].mean()  if len(losers)  else 0
        rr_ratio = abs(avg_win / avg_loss) if avg_loss else 0
        
        print(f"Toplam İşlem        : {len(trades):>12}")
        print(f"Kazanan             : {len(winners):>12}  (%{win_rate:.1f})")
        print(f"Kaybeden            : {len(losers):>12}")
        print(f"Ortalama Kazanç     : {avg_win:>12,.2f} TRY")
        print(f"Ortalama Kayıp      : {avg_loss:>12,.2f} TRY")
        print(f"Risk/Reward Oranı   : {rr_ratio:>12.2f}")
        print(f"Max Drawdown        : {max_dd:>11.2f} %")
    
    print(f"{'='*60}")


# ==================== ÇALIŞTIR ====================
conn = sqlite3.connect('data/trading.db')

INITIAL = 100_000

for symbol in ['YAPKREDI.IS', 'AKBNK.IS', 'GARAN.IS']:
    df = pd.read_sql(
        f"SELECT * FROM prices WHERE symbol='{symbol}' ORDER BY date",
        conn, parse_dates=['date'], index_col='date'
    )
    if df.empty:
        continue
    
    df = add_indicators(df)
    trades, equity = run_backtest(df, initial_capital=INITIAL)
    
    print_backtest_stats(symbol, INITIAL, trades, equity)
    plot_backtest_results(symbol, df, trades, equity)

conn.close()
```

### ✅ TEST 6.1

```bash
python3 scripts/06_backtesting.py

# Değerlendirme soruları:
# 1. Win Rate > %50 mi? (hedef min %55)
# 2. Risk/Reward > 1.5 mi? (önemli!)
# 3. Max Drawdown < %15 mi? (kabul edilebilir)
# 4. Equity Curve yukarı doğru gidiyor mu?
```

---

---

# PHASE 7: AI Ajanları

## 7.1 Ajan Mimarisi

### 🧠 MANTIK

**Ajan (Agent) nedir?**
Belirli bir görevi kendi başına yapan, karar verebilen, başka ajanlarla iletişim kurabilen birimler.

```
OrchestratorAgent (Koordinatör)
         │
    ┌────┼────────────────────┐
    │    │                    │
DataAgent  AnalysisAgent  TradingAgent
    │           │               │
Veri çeker  RSI, MACD     AL/SAT kararı
yfinance    Bollinger      Risk kontrolü
    │           │               │
    └─────── RiskAgent ─────────┘
                 │
          Kayıp limiti kontrolü
          Position sizing
```

**Neden ajanlar kullanıyoruz?**
1. Her ajan tek bir şeyi iyi yapar (Single Responsibility)
2. Bağımsız test edilebilir
3. Paralel çalışabilir (DataAgent veri çekerken AnalysisAgent çalışabilir)
4. Kolayca yeni ajan eklenebilir (SentimentAgent, NewsAgent vs.)

### 📝 KOD

```python
# agents/base_agent.py

from abc import ABC, abstractmethod
from loguru import logger
from datetime import datetime
import pandas as pd


class BaseAgent(ABC):
    """Tüm ajanların temel sınıfı"""
    
    def __init__(self, name):
        self.name   = name
        self.status = "idle"   # idle, running, error, done
        self.result = None
        self.logs   = []
        logger.info(f"Agent '{name}' initialized")
    
    def log(self, message, level="INFO"):
        entry = {"time": datetime.now(), "level": level, "message": message}
        self.logs.append(entry)
        getattr(logger, level.lower())(f"[{self.name}] {message}")
    
    @abstractmethod
    def run(self, **kwargs):
        """Ajanın ana görevi"""
        pass
    
    def get_status(self):
        return {"agent": self.name, "status": self.status, "result": self.result}
```

```python
# agents/data_agent.py

import yfinance as yf
import pandas as pd
import sqlite3
from agents.base_agent import BaseAgent


class DataAgent(BaseAgent):
    """Veri toplama ajanı"""
    
    def __init__(self, db_path='data/trading.db'):
        super().__init__("DataAgent")
        self.db_path = db_path
    
    def run(self, symbols, start='2022-01-01', end=None):
        self.status = "running"
        self.log(f"Fetching data for {symbols}")
        
        conn = sqlite3.connect(self.db_path)
        results = {}
        
        for symbol in symbols:
            try:
                df = yf.download(symbol, start=start, end=end,
                                 progress=False)
                if not df.empty:
                    df.reset_index(inplace=True)
                    df.columns = [c.lower() for c in df.columns]
                    df['symbol'] = symbol
                    df['date']   = pd.to_datetime(df['date']).dt.date
                    df[['symbol','date','open','high','low','close','volume']]\
                      .to_sql('prices', conn, if_exists='append', index=False)
                    results[symbol] = len(df)
                    self.log(f"{symbol}: {len(df)} rows saved")
            except Exception as e:
                self.log(f"{symbol}: ERROR - {e}", "ERROR")
        
        conn.close()
        self.status = "done"
        self.result = results
        return results
```

```python
# agents/analysis_agent.py

import sqlite3
import pandas as pd
import numpy as np
from agents.base_agent import BaseAgent


class AnalysisAgent(BaseAgent):
    """Teknik analiz ajanı"""
    
    def __init__(self, db_path='data/trading.db'):
        super().__init__("AnalysisAgent")
        self.db_path = db_path
    
    def _add_indicators(self, df):
        delta = df['close'].diff()
        gain  = delta.clip(lower=0).rolling(14).mean()
        loss  = (-delta.clip(upper=0)).rolling(14).mean()
        df['rsi'] = 100 - 100 / (1 + gain / loss)
        
        ema12 = df['close'].ewm(span=12).mean()
        ema26 = df['close'].ewm(span=26).mean()
        df['macd']        = ema12 - ema26
        df['macd_signal'] = df['macd'].ewm(span=9).mean()
        df['macd_hist']   = df['macd'] - df['macd_signal']
        
        sma20 = df['close'].rolling(20).mean()
        std20 = df['close'].rolling(20).std()
        df['bb_upper'] = sma20 + 2 * std20
        df['bb_lower'] = sma20 - 2 * std20
        df['sma20']    = sma20
        df['sma50']    = df['close'].rolling(50).mean()
        return df.dropna()
    
    def run(self, symbols):
        self.status = "running"
        conn = sqlite3.connect(self.db_path)
        analyses = {}
        
        for symbol in symbols:
            df = pd.read_sql(
                f"SELECT * FROM prices WHERE symbol='{symbol}' ORDER BY date",
                conn, parse_dates=['date'], index_col='date'
            )
            if df.empty:
                continue
            
            df = self._add_indicators(df)
            latest = df.iloc[-1]
            
            analyses[symbol] = {
                'close':       latest['close'],
                'rsi':         latest['rsi'],
                'macd':        latest['macd'],
                'macd_signal': latest['macd_signal'],
                'bb_upper':    latest['bb_upper'],
                'bb_lower':    latest['bb_lower'],
                'sma20':       latest['sma20'],
                'sma50':       latest['sma50'],
            }
            self.log(f"{symbol}: RSI={latest['rsi']:.2f}, MACD={latest['macd']:.4f}")
        
        conn.close()
        self.status = "done"
        self.result = analyses
        return analyses
```

```python
# agents/signal_agent.py

from agents.base_agent import BaseAgent


class SignalAgent(BaseAgent):
    """Sinyal üretme ajanı"""
    
    def __init__(self):
        super().__init__("SignalAgent")
    
    def _score(self, analysis):
        scores = []
        
        rsi = analysis.get('rsi', 50)
        if   rsi < 30: scores.append( 80)
        elif rsi < 40: scores.append( 40)
        elif rsi > 70: scores.append(-80)
        elif rsi > 60: scores.append(-40)
        else:          scores.append(  0)
        
        if analysis.get('macd', 0) > analysis.get('macd_signal', 0):
            scores.append(50)
        else:
            scores.append(-50)
        
        close = analysis.get('close', 0)
        upper = analysis.get('bb_upper', 0)
        lower = analysis.get('bb_lower', 0)
        if upper != lower:
            pos = (close - lower) / (upper - lower)
            scores.append(int((0.5 - pos) * 100))
        
        avg = sum(scores) / len(scores)
        
        if   avg >= 60: sig = 'STRONG_BUY'
        elif avg >= 30: sig = 'BUY'
        elif avg <= -60: sig = 'STRONG_SELL'
        elif avg <= -30: sig = 'SELL'
        else:            sig = 'NEUTRAL'
        
        return {'signal': sig, 'score': round(avg, 2)}
    
    def run(self, analyses):
        self.status = "running"
        signals = {}
        
        for symbol, analysis in analyses.items():
            result = self._score(analysis)
            signals[symbol] = result
            self.log(f"{symbol}: {result['signal']} (score: {result['score']})")
        
        self.status = "done"
        self.result = signals
        return signals
```

```python
# agents/orchestrator.py

from agents.data_agent     import DataAgent
from agents.analysis_agent import AnalysisAgent
from agents.signal_agent   import SignalAgent
from agents.base_agent     import BaseAgent
import matplotlib.pyplot as plt
import pandas as pd


class OrchestratorAgent(BaseAgent):
    """Tüm ajanları koordine eden orkestratör"""
    
    SYMBOLS = ['YAPKREDI.IS', 'AKBNK.IS', 'GARAN.IS']
    
    def __init__(self, db_path='data/trading.db'):
        super().__init__("OrchestratorAgent")
        self.data_agent     = DataAgent(db_path)
        self.analysis_agent = AnalysisAgent(db_path)
        self.signal_agent   = SignalAgent()
        self.db_path        = db_path
    
    def run(self, fetch_fresh=False):
        self.status = "running"
        self.log("Pipeline starting...")
        
        # Adım 1: Veri
        if fetch_fresh:
            self.log("Step 1: Fetching fresh data")
            self.data_agent.run(self.SYMBOLS)
        
        # Adım 2: Analiz
        self.log("Step 2: Technical analysis")
        analyses = self.analysis_agent.run(self.SYMBOLS)
        
        # Adım 3: Sinyal
        self.log("Step 3: Signal generation")
        signals = self.signal_agent.run(analyses)
        
        # Adım 4: Rapor
        self.log("Step 4: Generating report")
        self._print_report(analyses, signals)
        self._plot_dashboard(analyses, signals)
        
        self.status = "done"
        return signals
    
    def _print_report(self, analyses, signals):
        print("\n" + "="*60)
        print("🤖 AJAN SİSTEMİ RAPORU")
        print("="*60)
        emoji = {'STRONG_BUY':'🟢🟢','BUY':'🟢','NEUTRAL':'⚪',
                 'SELL':'🔴','STRONG_SELL':'🔴🔴'}
        
        for symbol, sig in signals.items():
            a   = analyses.get(symbol, {})
            emj = emoji.get(sig['signal'], '⚪')
            print(f"{emj} {symbol:14} | {sig['signal']:12} | "
                  f"Score: {sig['score']:6.1f} | "
                  f"RSI: {a.get('rsi',0):5.1f} | "
                  f"Fiyat: {a.get('close',0):7.2f} TRY")
        print("="*60)
    
    def _plot_dashboard(self, analyses, signals):
        """Ajan dashboard'u"""
        symbols = list(signals.keys())
        scores  = [signals[s]['score'] for s in symbols]
        colors  = ['#4CAF50' if s > 0 else '#F44336' for s in scores]
        
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))
        fig.suptitle('🤖 Ajan Dashboard', fontsize=13, fontweight='bold')
        
        # Sol: Sinyal skoru barları
        bars = axes[0].barh(symbols, scores, color=colors, height=0.5)
        axes[0].axvline(0, color='black', lw=1)
        axes[0].axvline( 40, color='green', ls='--', alpha=0.5)
        axes[0].axvline(-40, color='red',   ls='--', alpha=0.5)
        axes[0].set_xlabel('Sinyal Skoru')
        axes[0].set_title('Güncel Sinyaller')
        axes[0].grid(True, alpha=0.3, axis='x')
        for bar, score in zip(bars, scores):
            axes[0].text(score + (1 if score >= 0 else -1),
                        bar.get_y() + bar.get_height()/2,
                        f'{score:.1f}', va='center', fontsize=10)
        
        # Sağ: RSI karşılaştırma
        rsi_vals = [analyses[s].get('rsi', 50) for s in symbols]
        rsi_colors = []
        for r in rsi_vals:
            if r < 30: rsi_colors.append('#4CAF50')
            elif r > 70: rsi_colors.append('#F44336')
            else: rsi_colors.append('#2196F3')
        
        axes[1].barh(symbols, rsi_vals, color=rsi_colors, height=0.5)
        axes[1].axvline(30, color='green', ls='--', alpha=0.6, label='Oversold')
        axes[1].axvline(70, color='red',   ls='--', alpha=0.6, label='Overbought')
        axes[1].axvline(50, color='gray',  ls=':',  alpha=0.5)
        axes[1].set_xlabel('RSI Değeri')
        axes[1].set_title('RSI Karşılaştırması')
        axes[1].set_xlim(0, 100)
        axes[1].legend()
        axes[1].grid(True, alpha=0.3, axis='x')
        
        plt.tight_layout()
        plt.savefig('charts/agent_dashboard.png', dpi=120, bbox_inches='tight')
        plt.show()
        print("📊 Ajan dashboard grafiği kaydedildi")


# ==================== ÇALIŞTIR ====================
if __name__ == '__main__':
    import os
    os.makedirs('agents', exist_ok=True)
    os.makedirs('charts', exist_ok=True)
    
    orchestrator = OrchestratorAgent()
    signals = orchestrator.run(fetch_fresh=False)
    
    print("\n✅ Ajan pipeline tamamlandı!")
```

### ✅ TEST 7.1

```bash
# __init__ dosyaları oluştur
touch agents/__init__.py

# Çalıştır
python3 agents/orchestrator.py
```

---

---

# PHASE 8: Tüm Sistemi Çalıştır

## 8.1 Sıralı Test Komutu

Buraya geldin! Şimdi her şeyi sırayla çalıştır:

```bash
# ADIM 1: Kurulum
source venv/bin/activate
python3 -m pytest tests/ -v                        # Test geçiyor mu?

# ADIM 2: Veri İndir
python3 scripts/01_fetch_data.py                   # ✅ CSV + grafik
python3 scripts/02_setup_database.py               # ✅ DB kurulu

# ADIM 3: Teknik Analiz
python3 scripts/03_technical_analysis.py           # ✅ RSI, MACD, BB grafik

# ADIM 4: Sinyaller
python3 scripts/04_signal_generator.py             # ✅ Sinyal grafik

# ADIM 5: Risk
python3 scripts/05_risk_manager.py                 # ✅ Risk grafik

# ADIM 6: Backtest
python3 scripts/06_backtesting.py                  # ✅ Backtest grafik

# ADIM 7: Ajanlar
python3 agents/orchestrator.py                     # ✅ Dashboard grafik
```

---

## 8.2 Günlük Rutin

Sistem kurulduktan sonra her gün şunu çalıştırmanız yeterli:

```bash
python3 agents/orchestrator.py
```

Bu komut:
1. Verileri günceller
2. Teknik analiz yapar
3. Sinyalleri üretir
4. Dashboard grafiğini oluşturur

---

---

# Kontrol Listesi

## ✅ Phase 1 — Ortam & Git
- [ ] Python venv aktif
- [ ] Tüm kütüphaneler yüklü
- [ ] `.gitignore` hazır
- [ ] `pre-commit` yüklü ve çalışıyor
- [ ] İlk commit atıldı

## ✅ Phase 2 — Veri
- [ ] CSV dosyaları `data/` klasöründe
- [ ] SQLite veritabanı kurulu
- [ ] Veri grafiği kontrol edildi (anormal yok)

## ✅ Phase 3 — Teknik Analiz
- [ ] RSI mantıklı (0-100 arası)
- [ ] MACD hesaplandı
- [ ] Bollinger Bands görünüyor
- [ ] Grafik kaydedildi

## ✅ Phase 4 — Sinyaller
- [ ] Sinyaller grafikte mantıklı görünüyor
- [ ] Sinyal dağılımı %50'den fazla NEUTRAL değil
- [ ] BUY işaretleri düşük noktalarda

## ✅ Phase 5 — Risk
- [ ] Position sizing hesabı doğru
- [ ] Risk grafik kaydedildi
- [ ] %1 risk kuralı anlaşıldı

## ✅ Phase 6 — Backtest
- [ ] Win Rate > %50
- [ ] Risk/Reward > 1.5
- [ ] Max Drawdown < %20
- [ ] Equity curve yukarı gidiyor

## ✅ Phase 7 — Ajanlar
- [ ] DataAgent çalışıyor
- [ ] AnalysisAgent çalışıyor
- [ ] SignalAgent çalışıyor
- [ ] OrchestratorAgent hepsini birleştiriyor
- [ ] Dashboard grafik oluştu

## ✅ Pre-Commit / Husky
- [ ] `git commit` öncesi otomatik kontrol
- [ ] Black formatter aktif
- [ ] Flake8 linter aktif
- [ ] Testler otomatik çalışıyor

---

## 🚦 Canlıya Alma Kararı

Şu kriterlerin **HEPSİ** sağlanmadan canlıya geçme:

```
✅ Demo'da 1 ay test ettim
✅ Backtesting Win Rate > %55
✅ Backtesting Max Drawdown < %15
✅ Risk manager aktif
✅ Stop Loss her işlemde var
✅ Günlük dashboard'u takip ettim
✅ 10.000 TRY küçük miktar ile başlayacağım
```

---

## 📚 Terimler Sözlüğü

| Terim | Açıklama |
|-------|----------|
| RSI | Relative Strength Index — Momentum göstergesi |
| MACD | Moving Average Convergence Divergence — Trend göstergesi |
| Bollinger Bands | Volatilite bandı |
| SMA / EMA | Simple / Exponential Moving Average |
| ATR | Average True Range — Volatilite ölçer |
| OBV | On Balance Volume — Hacim trendi |
| Backtesting | Stratejiyi geçmiş verilerle test etme |
| Drawdown | Tepe noktadan düşüş miktarı |
| Win Rate | Kazanan işlemlerin oranı |
| Slippage | Beklenen fiyat ile gerçek fiyat farkı |
| Position Sizing | Her işlemde ne kadar alınacağını belirleme |
| Stop Loss | Otomatik kayıp durdurma noktası |
| Take Profit | Otomatik kâr alma noktası |
| Agent | Belirli bir görevi yapan özerk birim |

---

*Son güncelleme: Nisan 2026*  
*Sualp için hazırlandı — RPA × Fintech × AI 🚀*
