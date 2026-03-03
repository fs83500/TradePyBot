# TradePyBot

Trading Bot Multi-IA - Dashboard with multiple AI agents for trading decisions.

## 🚀 Features

- **Multi-IA Agents**: Heliox (Momentum), Syntax (Mean Reversion), Prisme (Sentiment)
- **Risk Sliders**: Adjustable risk level (1-10) for each AI agent
- **Modern Dashboard**: React + TypeScript + TailwindCSS
- **Real-time WebSockets**: Live market data and AI feedback
- **Token Auth**: Gateway-style authentication (like OpenClaw)
- **Docker Ready**: One-command deployment

## 📁 Project Structure

```
TradePyBot/
├── backend/                    # Python FastAPI Backend
│   ├── main.py                # FastAPI app entry point
│   ├── config.py              # Configuration settings
│   ├── api/                    # API endpoints
│   │   ├── auth.py            # Token authentication
│   │   ├── agents.py           # AI agents management
│   │   ├── trades.py           # Trade operations
│   │   ├── portfolio.py        # Portfolio management
│   │   ├── stats.py            # Statistics
│   │   └── websocket.py        # Real-time WebSockets
│   ├── models/                 # SQLAlchemy models
│   │   ├── user.py
│   │   ├── agent.py
│   │   ├── trade.py
│   │   └── portfolio.py
│   ├── agents/                 # AI Agent implementations
│   │   ├── base_agent.py
│   │   ├── heliox.py          # Momentum strategy
│   │   ├── syntax.py           # Mean reversion strategy
│   │   ├── prisme.py           # Sentiment strategy
│   │   └── provider.py         # AI provider configurations
│   ├── trading/                # Trading logic
│   │   ├── exchange.py
│   │   ├── paper_trading.py
│   │   └── risk_manager.py
│   └── database/               # Database operations
│       ├── db.py
│       └── crud.py
├── frontend/                   # React TypeScript Frontend
│   ├── src/
│   │   ├── App.tsx            # Main app with routing
│   │   ├── components/        # Reusable components
│   │   │   ├── Navbar.tsx
│   │   │   ├── AgentCard.tsx  # Risk slider component
│   │   │   ├── StatCard.tsx
│   │   │   └── TradeTable.tsx
│   │   ├── pages/              # Page components
│   │   │   ├── Login.tsx
│   │   │   ├── Dashboard.tsx
│   │   │   ├── Integrations.tsx
│   │   │   └── Stats.tsx
│   │   ├── hooks/              # Custom React hooks
│   │   │   ├── useAuthStore.ts
│   │   │   ├── useApi.ts
│   │   │   └── useWebSocket.ts
│   │   ├── main.tsx
│   │   └── index.css
│   ├── index.html
│   ├── package.json
│   ├── vite.config.ts
│   └── tailwind.config.js
├── ModelUI/                     # UI/UX Mockups (Prisme)
│   ├── login.html
│   ├── dashboard.html
│   ├── integrations.html
│   ├── stats.html
│   └── captures/*.png
├── docs/
│   └── SECURITY.md             # Security documentation
├── security/
│   └── fail2ban/               # Fail2Ban configuration
├── docker-compose.yml
├── Dockerfile.backend
├── Dockerfile.frontend
├── requirements.txt
└── README.md
```

## 🎨 Design System

| Element | Color |
|---------|-------|
| Background (Login) | `#FFFFFF` |
| Background (Dashboard) | `#F8FAFC` |
| Card | `#FFFFFF` |
| Text | `#1E293B` |
| Primary (Violet) | `#8B5CF6` |
| Secondary (Rose) | `#EC4899` |
| Success (Green) | `#22C55E` |
| Warning (Yellow) | `#F59E0B` |
| Error (Red) | `#EF4444` |

## 📡 API Endpoints

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/login` | Login (returns token) |
| GET | `/api/auth/me` | Get current user |
| POST | `/api/auth/logout` | Logout |

### Agents
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/agents` | List all agents |
| POST | `/api/agents` | Create agent |
| GET | `/api/agents/:name` | Get agent details |
| POST | `/api/agents/:name/configure` | Update risk slider |

### Trading
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/trades` | Trade history |
| POST | `/api/trades` | Create trade |
| GET | `/api/trades/:id` | Get trade |

### Portfolio & Stats
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/portfolio` | Portfolio summary |
| GET | `/api/stats` | Statistics |

### WebSockets
| Endpoint | Description |
|----------|-------------|
| `/ws/market/:symbol` | Real-time prices |
| `/ws/feedback` | AI feedback stream |

## 🤖 AI Agents

| Agent | Strategy | Risk Profile |
|-------|----------|--------------|
| Heliox 🌟 | Momentum | Aggressive (8/10) |
| Syntax 🔧 | Mean Reversion | Moderate (5/10) |
| Prisme 🎨 | Sentiment | Conservative (3/10) |

## 🔧 Quick Start

### Docker (Recommended)

```bash
# Clone
git clone https://github.com/fs83500/TradePyBot.git
cd TradePyBot

# Start all services
docker-compose up -d

# Access
open http://localhost:3000
```

### Manual Setup

#### Backend
```bash
cd TradePyBot

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows

# Install dependencies
pip install -r requirements.txt

# Run
uvicorn backend.main:app --reload --port 8000
```

#### Frontend
```bash
cd TradePyBot/frontend

# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build
```

## 🔐 Authentication

TradePyBot uses token-based authentication similar to OpenClaw gateway:

1. **Login**: POST `/api/auth/login` returns a token
2. **Authorization**: Include `Authorization: Bearer <token>` header
3. **Token Expiry**: 24 hours default

## 📊 Risk Sliders

Each AI agent has an adjustable risk slider (1-10):

- **1-3**: Conservative - Lower risk, smaller positions
- **4-6**: Moderate - Balanced approach
- **7-10**: Aggressive - Higher risk, larger positions

```typescript
// Example: Update agent risk
POST /api/agents/heliox/configure
{
  "risk_slider_value": 0.8  // 8/10 = Aggressive
}
```

## 🛡️ Security

See [docs/SECURITY.md](docs/SECURITY.md) for security best practices including:
- Fail2Ban configuration
- API rate limiting
- Token management
- HTTPS/TLS setup

## 📝 Development

```bash
# Run backend in development
uvicorn backend.main:app --reload --port 8000

# Run frontend in development
cd frontend && npm run dev

# Run tests (when available)
pytest backend/tests/
```

## 🐳 Docker Commands

```bash
# Build images
docker-compose build

# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Production (with PostgreSQL)
docker-compose --profile production up -d
```

## 📜 License

MIT License

## 👥 Authors

- **Heliox** - Orchestrator
- **Prisme** - UI/UX Design
- **Syntax** - Development