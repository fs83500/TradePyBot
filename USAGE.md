# Guide d'Usage - TradePyBot

Documentation complète pour utiliser TradePyBot - Trading Bot Multi-IA avec Dashboard.

## 📋 Prérequis

- ✅ TradePyBot installé (voir [INSTALLER.md](./INSTALLER.md))
- ✅ Backend fonctionnel sur `http://localhost:8000`
- ✅ Frontend fonctionnel sur `http://localhost:3000`
- ✅ Token d'authentification (voir section Authentification)

---

## 🔐 Authentification

TradePyBot utilise un système d'authentification basé sur tokens (comme OpenClaw gateway).

### 1. Se connecter

#### Via l'interface web

1. Ouvrir `http://localhost:3000/login`
2. Le token est généré automatiquement (aucun formulaire nécessaire)
3. Vous êtes redirigé vers le dashboard

#### Via l'API

```bash
# Endpoint
POST http://localhost:8000/api/auth/login

# Réponse
{
  "token": "abc123xyz...",
  "user": "trader",
  "expires_at": "2026-03-04T04:00:00"
}
```

### 2. Utiliser le token

#### Dans les requêtes HTTP

```bash
# Exemple avec curl
curl -X GET http://localhost:8000/api/agents \
  -H "Authorization: Bearer abc123xyz..."
```

#### Dans l'interface web

Le token est automatiquement stocké dans le stockage local du navigateur.

### 3. Se déconnecter

```bash
# Endpoint
POST http://localhost:8000/api/auth/logout
Authorization: Bearer <token>
```

### 4. Vérifier le token

```bash
# Endpoint
GET http://localhost:8000/api/auth/me
Authorization: Bearer <token>
```

---

## 📊 Dashboard

Le dashboard est la page principale après authentification.

### Accès

```
http://localhost:3000/dashboard
```

### Fonctionnalités

#### 1. Vue d'ensemble

- Balance courante
- Profit/Perte total
- Nombre de trades
- Taux de réussite

#### 2. Agents IA

| Agent | Stratégie | Niveau de risque | Statut |
|-------|-----------|------------------|--------|
| Heliox 🌟 | Momentum | 5/10 (Modéré) | 🔵 Actif |
| Syntax 🔧 | Mean Reversion | 4/10 (Conservateur) | 🔵 Actif |
| Prisme 🎨 | Sentiment | 3/10 (Conservateur) | 🔴 Inactif |

#### 3. Trades actifs

Liste des trades en cours avec:
- Symbole (ex: BTC/USDT)
- Direction (Long/Short)
- Prix d'entrée
- Profit/Perte

---

## 🤖 Gestion des Agents IA

### Accès

```
http://localhost:8000/api/agents
```

### Lister les agents

```bash
# Endpoint
GET http://localhost:8000/api/agents

# Réponse
[
  {
    "id": 1,
    "name": "heliox",
    "provider": "openai",
    "model": "gpt-4o",
    "strategy": "momentum",
    "risk_level": "medium",
    "risk_slider_value": 0.5,
    "is_active": true
  },
  {
    "id": 2,
    "name": "syntax",
    "provider": "claude",
    "model": "claude-3-sonnet",
    "strategy": "mean_reversion",
    "risk_level": "low",
    "risk_slider_value": 0.3,
    "is_active": true
  },
  {
    "id": 3,
    "name": "prisme",
    "provider": "gemini",
    "model": "gemini-2.0-flash",
    "strategy": "sentiment",
    "risk_level": "low",
    "risk_slider_value": 0.3,
    "is_active": false
  }
]
```

### Créer un agent

```bash
# Endpoint
POST http://localhost:8000/api/agents

# Corps de la requête
{
  "name": "nouvel-agent",
  "provider": "openai",
  "model": "gpt-4o",
  "strategy": "momentum"
}

# Réponse
{
  "id": 4,
  "name": "nouvel-agent",
  "provider": "openai",
  "model": "gpt-4o",
  "strategy": "momentum",
  "risk_level": "medium",
  "risk_slider_value": 0.5
}
```

### Configurer un agent (slider de risque)

```bash
# Endpoint
POST http://localhost:8000/api/agents/heliox/configure

# Corps de la requête
{
  "risk_slider_value": 0.8  # 8/10 = Aggressive
}

# Réponse
{
  "id": 1,
  "name": "heliox",
  "risk_level": "high",
  "risk_slider_value": 0.8
}
```

### Niveaux de risque

| Slider | Risk Level | Description |
|--------|------------|-------------|
| 0.0 - 0.33 | Low | Conservateur - Petites positions |
| 0.34 - 0.66 | Medium | Modéré - Équilibré |
| 0.67 - 1.0 | High | Aggressif - Grosses positions |

### Lister les providers IA

```bash
# Endpoint
GET http://localhost:8000/api/agents/providers

# Réponse
{
  "providers": {
    "gemini": { ... },
    "claude": { ... },
    "openai": { ... },
    "groq": { ... },
    "deepseek": { ... },
    "mistral": { ... },
    "ollama": { ... }
  },
  "available": ["gemini", "claude", "openai", "groq", "deepseek", "mistral", "ollama"]
}
```

### Models d'un provider

```bash
# Endpoint
GET http://localhost:8000/api/agents/providers/openai/models

# Réponse
{
  "provider": "openai",
  "models": ["gpt-4o", "gpt-4-turbo", "gpt-3.5-turbo"]
}
```

---

## 💱 Gestion des Trades

### Accès

```
http://localhost:8000/api/trades
```

### Lister les trades

```bash
# Endpoint
GET http://localhost:8000/api/trades

# Paramètres optionnels
GET http://localhost:8000/api/trades?status=closed&symbol=BTC/USDT&limit=50

# Réponse
[
  {
    "id": 1,
    "symbol": "BTC/USDT",
    "direction": "long",
    "entry_price": 45000.0,
    "exit_price": 46000.0,
    "amount": 0.1,
    "profit": 1000.0,
    "status": "closed",
    "agent_name": "heliox",
    "exchange": "paper",
    "created_at": "2026-03-03T12:00:00",
    "reason": "Momentum breakout detected"
  }
]
```

### Créer un trade

```bash
# Endpoint
POST http://localhost:8000/api/trades

# Corps de la requête
{
  "symbol": "BTC/USDT",
  "direction": "long",
  "amount": 0.1,
  "agent_name": "heliox",
  "reason": "Momentum breakout detected"
}

# Réponse
{
  "id": 2,
  "symbol": "BTC/USDT",
  "direction": "long",
  "amount": 0.1,
  "status": "pending",
  "agent_name": "heliox",
  "created_at": "2026-03-03T13:00:00"
}
```

### Fermer un trade

```bash
# Endpoint
PUT http://localhost:8000/api/trades/2/close

# Corps de la requête
{
  "exit_price": 47000.0
}

# Réponse
{
  "id": 2,
  "profit": 2000.0,
  "status": "closed",
  "closed_at": "2026-03-03T14:00:00"
}
```

---

## 📈 Portfolio

### Accès

```
http://localhost:8000/api/portfolio
```

### Lister les portfolios

```bash
# Endpoint
GET http://localhost:8000/api/portfolio

# Réponse
[
  {
    "id": 1,
    "name": "default",
    "type": "paper",
    "initial_balance": 1000.0,
    "current_balance": 1250.0,
    "free_balance": 1250.0,
    "total_trades": 15,
    "is_active": true
  }
]
```

### Créer un portfolio

```bash
# Endpoint
POST http://localhost:8000/api/portfolio

# Corps de la requête
{
  "name": "portfolio-2",
  "initial_balance": 5000.0
}

# Réponse
{
  "id": 2,
  "name": "portfolio-2",
  "initial_balance": 5000.0,
  "current_balance": 5000.0
}
```

### Obtenir les statistiques

```bash
# Endpoint
GET http://localhost:8000/api/stats

# Réponse
{
  "agents": [
    {
      "name": "heliox",
      "total_predictions": 150,
      "accuracy": 0.68,
      "total_profit": 2500.0
    }
  ],
  "trades": {
    "total": 150,
    "winning": 102,
    "losing": 48,
    "win_rate": 68
  },
  "portfolio": {
    "initial_balance": 1000.0,
    "current_balance": 1250.0,
    "total_pnl": 250.0
  }
}
```

---

## 🌐 WebSockets - Temps réel

### Endpoint de marché

```
ws://localhost:8000/ws/market/{symbol}
```

#### Exemple de connexion JavaScript

```javascript
const ws = new WebSocket('ws://localhost:8000/ws/market/BTC/USDT')

ws.onopen = () => {
  console.log('Connected to market data stream')
  ws.send(JSON.stringify({ type: 'subscribe' }))
}

ws.onmessage = (event) => {
  const data = JSON.parse(event.data)
  console.log('Market data:', data)
  
  if (data.type === 'market_data') {
    console.log(`BTC/USDT: $${data.data.last}`)
  }
}

ws.onclose = () => {
  console.log('Disconnected. Reconnecting...')
  setTimeout(() => {
    // Auto-reconnect after 3 seconds
    new WebSocket('ws://localhost:8000/ws/market/BTC/USDT')
  }, 3000)
}
```

### Endpoint de feedback IA

```
ws://localhost:8000/ws/feedback
```

#### Exemple de connexion JavaScript

```javascript
const ws = new WebSocket('ws://localhost:8000/ws/feedback')

ws.onopen = () => {
  console.log('Connected to AI feedback stream')
}

ws.onmessage = (event) => {
  const data = JSON.parse(event.data)
  console.log('AI Feedback:', data)
  
  if (data.type === 'feedback') {
    console.log(`Agent: ${data.data.agent}, Signal: ${data.data.signal}`)
  }
}
```

### Format des messages

#### Message de type 'market_data'

```json
{
  "type": "market_data",
  "symbol": "BTC/USDT",
  "data": {
    "last": 45500.0,
    "bid": 45499.5,
    "ask": 45500.5,
    "volume": 1250.5,
    "high": 46000.0,
    "low": 45000.0
  },
  "timestamp": 1741000000000
}
```

#### Message de type 'feedback'

```json
{
  "type": "feedback",
  "data": {
    "agent": "heliox",
    "signal": "buy",
    "confidence": 0.85,
    "reasoning": "Strong momentum detected",
    "timestamp": "2026-03-03T12:00:00"
  },
  "timestamp": 1741000000000
}
```

---

## 📱 Interface Web

### Pages disponibles

| Page | URL | Description |
|------|-----|-------------|
| Login | `/login` | Authentification |
| Dashboard | `/dashboard` | Vue d'ensemble |
| Integrations | `/integrations` | Gestion des intégrations |
| Stats | `/stats` | Statistiques et analyse |

### Navigation

```
┌─────────────────────────────────┐
│  📊 TradePyBot                  │
├─────────────────────────────────┤
│  📊 Dashboard                   │
│  🔗 Integrations                │
│  📈 Stats                       │
├─────────────────────────────────┤
│  [User ▼]                       │
│    - Déconnexion                │
└─────────────────────────────────┘
```

---

## 🔧 Configuration

### Modifier les paramètres

Éditer le fichier `.env` à la racine du projet:

```bash
# Base de données
DATABASE_URL=sqlite+aiosqlite:///./trading.db
DATABASE_ECHO=false

# Authentification
AUTH_SECRET_KEY=TradePyBot-Secret-Key-Change-This
AUTH_TOKEN_EXPIRY_HOURS=24

# Trading
TRADING_PAPER_MODE=true
TRADING_MAX_RISK_PERCENT=2.0
TRADING_MAX_DAILY_LOSS=100.0

# AI Providers (optionnel)
GEMINI_API_KEY=your-key
CLAUDE_API_KEY=your-key
OPENAI_API_KEY=your-key
```

### Redémarrer l'application

```bash
# Docker
docker compose restart backend

# Local
# Arrêter et relancer les services
```

---

## ❓ FAQ

### Je n'arrive pas à me connecter

1. Vérifier que le backend est lancé:
   ```bash
   curl http://localhost:8000/health
   ```

2. Vérifier les logs:
   ```bash
   docker compose logs backend
   ```

3. Vérifier le token:
   ```bash
   curl http://localhost:8000/api/auth/login
   ```

### Les données ne s'affichent pas

1. Vérifier la base de données:
   ```bash
   docker compose exec backend sqlite3 /app/trading.db "SELECT * FROM trades;"
   ```

2. Vérifier les agents:
   ```bash
   curl http://localhost:8000/api/agents
   ```

### Le WebSocket ne se connecte pas

1. Vérifier que le backend écoute sur le port 8000
2. Vérifier la configuration CORS
3. Vérifier que WebSocket est autorisé dans le navigateur

---

## 📞 Support

### Documentation

- [GitHub Repository](https://github.com/fs83500/TradePyBot)
- [API Documentation](http://localhost:8000/docs)
- [Installation Guide](./INSTALLER.md)
- [Security Guide](./docs/SECURITY.md)

### Communauté

- [GitHub Discussions](https://github.com/fs83500/TradePyBot/discussions)
- [Twitter](https://twitter.com/tradepybot)
- [Email](support@tradepybot.com)

---

**Dernière mise à jour:** Mars 2026

**Auteur:** SYNTAX - TradePyBot Development Team
