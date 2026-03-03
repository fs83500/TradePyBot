# TradePyBot

Trading Bot Multi-IA - Dashboard with multiple AI agents for trading decisions.

## 🚀 Features

- **Multi-IA** : Multiple AI agents with different strategies
- **Dashboard** : Modern UI with stats, charts, and trade history
- **Login** : Token-based authentication (like OpenClaw gateway)
- **Docker** : Easy deployment with Docker Compose

## 📁 Structure

```
TradePyBot/
├── backend/           # Python FastAPI
├── frontend/          # React/HTML
├── ModelUI/           # UI/UX Mockups (Prisme)
│   ├── login.html
│   ├── dashboard.html
│   ├── integrations.html
│   └── stats.html
├── docker-compose.yml
├── Dockerfile
└── README.md
```

## 🎨 Design System

- **Login** : White background, gradient violet-rose button
- **Dashboard** : Light gray background, white cards
- **Colors** : Primary #8B5CF6, Success #22C55E, Warning #F59E0B, Error #EF4444

## 📋 Workflow

1. **Prisme** : UI/UX mockups (HTML + PNG)
2. **Syntax** : Backend + Frontend implementation
3. **Docker** : Deployment configuration

## 🔧 Installation

```bash
# Clone
git clone https://github.com/fs83500/TradePyBot.git
cd TradePyBot

# Docker
docker-compose up -d

# Access
http://localhost:3000
```

## 📝 License

MIT License

## 👥 Authors

- **Heliox** - Orchestrator
- **Prisme** - UI/UX Design
- **Syntax** - Development