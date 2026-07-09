# 🍎 eBay Deal Detection System

An automated deal finder that monitors eBay listings, estimates resale value, calculates potential profit, and sends real-time Discord notifications for profitable opportunities.

Built to help resellers identify underpriced listings like MacBooks and PS5s before they disappear.

---

## ✨ Features

- 🔍 Monitor eBay for newly listed MacBooks
- 💰 Calculate potential profit using trade-in prices
- 📢 Send rich Discord notifications
- 🚫 Filter unwanted listings using configurable banned words
- 🖥️ Support multiple MacBook models and configurations
- 🐳 Docker support for 24/7 deployment
- 💾 Prevent duplicate alerts using persistent storage

---

## 🛠️ Tech Stack

- Python 3
- Playwright
- Docker
- eBay Browse API
- Discord Webhooks
- Ubuntu Server
- GitHub

---

## 📁 Project Structure

```text
MacBookTracker/
│
├── .github/workflows
│   └── deploy.yml
│
├── src/
│   ├── config.py
│   ├── discord_notifier.py
│   ├── ebay_client.py
│   ├── listing.py
│   ├── musicmagpie_macbook.py
│   ├── search_category.py
│   ├── seen_items_manager.py
│   ├── spec_parser.py
│   └── tracker.py
│
├── .env
├── main.py
├── README.md
├── requirements.txt
└── seen_items.json
```

---

## 🚀 Installation

Clone the repository.

```bash
git clone https://github.com/YOUR_USERNAME/MacBookTracker.git
cd MacBookTracker
```

Create a virtual environment.

```bash
python -m venv .venv
```

Activate it.

### macOS / Linux

```bash
source .venv/bin/activate
```

### Windows

```powershell
.venv\Scripts\activate
```

Install dependencies.

```bash
pip install -r requirements.txt
```

---

## ⚙️ Configuration

Create a `.env` file in the project root.

```env
EBAY_CLIENT_ID1=
EBAY_CLIENT_SECRET_1=

EBAY_CLIENT_ID_2=
EBAY_CLIENT_SECRET_2=

EBAY_CLIENT_ID_3=
EBAY_CLIENT_SECRET_3=

DISCORD_TOKEN=
DISCORD_WEBHOOK_URL=
DISCORD_AUCTION_WEBHOOK_URL=
```

---

## ▶️ Running

```bash
python3 main.py
```

---

## 🐳 Running with Docker

Build the container.

```bash
docker compose build
```

Start the tracker.

```bash
docker compose up -d
```

View logs.

```bash
docker compose logs -f
```

Stop the tracker.

```bash
docker compose down
```

---

## 📄 License

This project is licensed under the MIT License.

