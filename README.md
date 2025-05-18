# 💳 Digital Wallet System with Fraud Detection

A secure backend system that allows users to register, log in, and manage virtual cash — including transfers, withdrawals, and fraud detection. Built using Python Flask with RESTful API architecture.

---

## 🚀 Features

- 🔐 User registration and JWT-based login
- 💰 Wallet operations (deposit, withdraw, transfer)
- 📜 Transaction history
- 🔎 Basic fraud detection
  - 🚨 Large withdrawals flagged
  - 🔁 Multiple rapid transfers flagged
- 🛡 Admin reports
  - Flagged transactions
  - Total user balances
  - Top users by transaction volume
- 🕒 Daily scheduled fraud scans (APS cheduler)
- 📧 Mock email alerts for suspicious activity (via logs)

---

## 📦 Tech Stack

- Python 3.x
- Flask
- Flask-JWT-Extended
- Flask-SQLAlchemy
- APScheduler
- SQLite (for demo)

---

## 🔧 Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone https://github.com/TheSensibleLunatic/digital-wallet-system.git
   cd digital-wallet-system
2. **WATCH THE 2 MINUTE VIDEO**
   ```bash
   https://www.youtube.com/watch?v=6srnrm5llF8
