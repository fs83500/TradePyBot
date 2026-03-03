# Installation de TradePyBot

Documentation complète pour installer TradePyBot sur différentes plateformes.

## 📋 Prérequis

### Minima requis
- **OS**: Linux, macOS, ou Windows (WSL2 recommandé)
- **RAM**: 4GB minimum (8GB recommandé pour les agents IA)
- **Disk**: 10GB d'espace disque libre
- **Internet**: Connexion stable pour les mises à jour

### Dépendances selon méthode

| Méthode | Dépendances |
|---------|-------------|
| Docker | Docker 24+, Docker Compose 2.20+ |
| Local | Python 3.11+, Node.js 18+, npm 9+ |
| Production | Docker, nginx, Certbot, systemd |

---

## 🐳 Méthode 1: Docker (Recommandée)

La méthode la plus simple pour avoir TradePyBot opérationnel en quelques minutes.

### Prérequis

```bash
# Docker
docker --version  # 24.0+

# Docker Compose
docker compose version  # 2.20+

# Vérifier Docker Desktop (Windows/macOS)
docker info
```

### Installation rapide

```bash
# Cloner le repo
git clone https://github.com/fs83500/TradePyBot.git
cd TradePyBot

# Démarrer avec Docker Compose
docker compose up -d
```

### Configuration

Créer un fichier `.env` à la racine du projet :

```bash
# Base de données (SQLite pour dev)
DATABASE_URL=sqlite+aiosqlite:///./trading.db
DATABASE_ECHO=false

# Authentification
AUTH_SECRET_KEY=TradePyBot-Secret-Key-Change-This-In-Production
AUTH_TOKEN_EXPIRY_HOURS=24

# Trading
TRADING_PAPER_MODE=true
TRADING_MAX_RISK_PERCENT=2.0
TRADING_MAX_DAILY_LOSS=100.0

# AI Providers (optionnel - pour production)
# GEMINI_API_KEY=your-key
# CLAUDE_API_KEY=your-key
# OPENAI_API_KEY=your-key
```

### Démarrage

```bash
# Lancer tous les services
docker compose up -d

# Vérifier le statut
docker compose ps

# Voir les logs en temps réel
docker compose logs -f

# Accès à l'interface
# http://localhost:3000
# http://localhost:8000/docs (API documentation)
```

### Arrêt

```bash
# Arrêter tous les services
docker compose down

# Arrêter et supprimer les volumes (DONNÉES PERDUES !)
docker compose down -v

# Réinitialiser complètement
docker compose down -v && docker system prune -a
```

### Mise à jour

```bash
# Arrêter les services actuels
docker compose down

# Récupérer les dernières modifications
git pull origin main

# Reconstruire les images
docker compose build --no-cache

# Démarrer
docker compose up -d
```

### Sauvegarde

```bash
# Copier les données SQLite
docker compose exec backend cp /app/trading.db /app/trading.db.backup

# Copier le fichier .env
cp .env .env.backup
```

---

## 💻 Méthode 2: Développement Local

Pour le développement et les tests locaux.

### Backend Python

#### 1. Prérequis

```bash
# Vérifier Python 3.11+
python3 --version  # doit être >= 3.11

# Vérifier pip
pip3 --version
```

#### 2. Installer les dépendances

```bash
# Créer un environnement virtuel
python3 -m venv venv

# Activer l'environnement
# Linux/macOS
source venv/bin/activate

# Windows
venv\Scripts\activate

# Installer les dépendances
pip install -r requirements.txt
```

#### 3. Lancer le backend

```bash
# Lancer avec uvicorn
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000

# Ou avec python -m
python -m uvicorn backend.main:app --reload
```

### Frontend React

#### 1. Prérequis

```bash
# Vérifier Node.js 18+
node --version  # doit être >= 18.0

# Vérifier npm
npm --version  # doit être >= 9.0
```

#### 2. Installer les dépendances

```bash
cd frontend

# Installer les packages
npm install

# Lancer en développement
npm run dev
```

L'interface sera disponible sur `http://localhost:3000`.

### Base de données

#### SQLite (Développement)

Par défaut, SQLite est utilisé. Aucune configuration supplémentaire.

#### PostgreSQL (Production)

```bash
# Créer la base de données
createdb trading_bot

# Créer l'utilisateur
createuser -s trading_user

# Modifier le fichier .env
DATABASE_URL=postgresql://trading_user@localhost/trading_bot
```

---

## 🖥️ Méthode 3: Production (Serveur VPS)

Déploiement sur un serveur cloud (Ubuntu/Debian).

### Serveur VPS

#### 1. Prérequis

```bash
# Serveur recommandé
# - CPU: 2 vCPU
# - RAM: 4GB
# - Disk: 50GB SSD
# - OS: Ubuntu 22.04 LTS ou Debian 12
```

#### 2. Installation préalable

```bash
# Mettre à jour le système
sudo apt update && sudo apt upgrade -y

# Installer Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Installer Docker Compose
sudo apt install docker-compose-plugin -y

# Redémarrer
reboot
```

#### 3. Déploiement

```bash
# Cloner le repo
git clone https://github.com/fs83500/TradePyBot.git
cd TradePyBot

# Copier l'exemple de configuration
cp .env.example .env

# Éditer la configuration
nano .env

# Démarrer en mode production
docker compose --profile production up -d
```

### nginx Reverse Proxy

#### 1. Installer nginx

```bash
sudo apt install nginx -y
```

#### 2. Configuration

Créer `/etc/nginx/sites-available/tradepybot` :

```nginx
server {
    listen 80;
    server_name your-domain.com;

    # Proxy pour le frontend
    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

    # Proxy pour l'API
    location /api {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

    # Proxy pour les WebSockets
    location /ws {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "Upgrade";
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

#### 3. Activer la configuration

```bash
# Créer le lien symbolique
sudo ln -s /etc/nginx/sites-available/tradepybot /etc/nginx/sites-enabled/

# Tester la configuration
sudo nginx -t

# Redémarrer nginx
sudo systemctl restart nginx
```

### HTTPS avec Let's Encrypt

```bash
# Installer Certbot
sudo apt install certbot python3-certbot-nginx -y

# Obtenir le certificat
sudo certbot --nginx -d your-domain.com

# Renouveler automatiquement
sudo systemctl enable certbot.timer
```

### Systemd Services

#### Backend service

Créer `/etc/systemd/system/tradepybot-backend.service` :

```ini
[Unit]
Description=TradePyBot Backend
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/tradepybot
ExecStart=/usr/local/bin/docker compose up
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

#### Frontend service

Créer `/etc/systemd/system/tradepybot-frontend.service` :

```ini
[Unit]
Description=TradePyBot Frontend
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/tradepybot/frontend
ExecStart=/usr/bin/npm run dev
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

#### Activer les services

```bash
sudo systemctl daemon-reload
sudo systemctl enable tradepybot-backend
sudo systemctl enable tradepybot-frontend
sudo systemctl start tradepybot-backend
```

### Monitoring

#### Logs

```bash
# Voir les logs Docker
docker compose logs -f

# Journal systemd
sudo journalctl -u tradepybot-backend -f
```

#### Health Check

```bash
# Endpoint de santé
curl http://localhost:8000/health

# Format JSON attendu
# {"status": "healthy"}
```

#### Monitoring avec Prometheus (optionnel)

```bash
# Ajouter dans docker-compose.yml
metrics:
  image: prom/prometheus
  ports:
    - "9090:9090"
  volumes:
    - ./prometheus.yml:/etc/prometheus/prometheus.yml
```

---

## ☁️ Méthode 4: Cloud

### AWS (EC2, RDS, S3)

#### 1. Créer l'EC2

```bash
# AMI: Ubuntu 22.04 LTS
# Instance: t3.medium (2 vCPU, 4GB RAM)

# Security Group
# - Port 22 (SSH)
# - Port 80 (HTTP)
# - Port 443 (HTTPS)
```

#### 2. Installer Docker

```bash
# Sur l'instance EC2
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker ubuntu
```

#### 3. Configurer RDS (PostgreSQL)

```bash
# Créer une base de données PostgreSQL
# - Version: 15.x
# - Instance class: db.t3.medium
# - Storage: 20GB SSD

# Modifier le fichier .env
DATABASE_URL=postgresql://username:password@endpoint.rds.amazonaws.com:5432/trading_bot
```

#### 4. Déployer

```bash
# Copier les fichiers
scp -i your-key.pem -r TradePyBot ubuntu@your-ec2:/home/ubuntu/

# SSH et déployer
ssh -i your-key.pem ubuntu@your-ec2
cd TradePyBot
docker compose up -d
```

### Google Cloud Platform

#### 1. Créer l'instance Compute Engine

```bash
# Zone: us-central1-a
# Machine type: e2-medium (2 vCPU, 4GB)

# Firewall rules
gcloud compute firewall-rules create tradepybot \
    --allow tcp:80,tcp:443,tcp:22
```

#### 2. Déployer

Même procédure que AWS (Docker Compose).

### Azure

#### 1. Créer la VM

```bash
# Image: Ubuntu 22.04 LTS
# Size: Standard_B2s (1 vCPU, 2GB)

# Open ports
az network nsg rule create \
    --resource-group tradepybot-rg \
    --nsg-name tradepybot-nsg \
    --name AllowHTTP \
    --priority 100 \
    --destination-port-ranges 80 443
```

#### 2. Déployer

Même procédure que AWS/GCP.

---

## 🍓 Méthode 5: Raspberry Pi / ARM

### Docker ARM

```bash
# Installer Docker sur Raspberry Pi
curl -sSL https://get.docker.com | sh

# Ajouter l'utilisateur au groupe docker
sudo usermod -aG docker pi

# Redémarrer
reboot
```

### Optimisations performances

#### 1. Configuration Docker Compose optimisée

```yaml
# docker-compose.rpi.yml
version: '3.8'

services:
  backend:
    build:
      context: .
      dockerfile: Dockerfile.backend
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 1G
    environment:
      - DATABASE_URL=sqlite+aiosqlite:///./trading.db
    volumes:
      - ./data:/app/data

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    ports:
      - "3000:3000"
    deploy:
      resources:
        limits:
          cpus: '0.25'
          memory: 512M
```

#### 2. Limitations connues

| Composant | Limitation | Solution |
|-----------|------------|----------|
| CPU | 4 cores @ 1.5GHz | Réduire le nombre d'agents actifs |
| RAM | 4GB | Surveiller la mémoire, utiliser SQLite |
| Storage | SD Card (lent) | Utiliser un SSD USB |
| Network | 100Mbps | WiFi > Ethernet pour performance |

---

## 🪟 Méthode 6: Windows (WSL2)

### Installation WSL2

```bash
# PowerShell (en tant qu'administrateur)
wsl --install
wsl --set-default Ubuntu-22.04

# Redémarrer
shutdown /r /t 1
```

### Docker Desktop

1. Installer [Docker Desktop](https://www.docker.com/products/docker-desktop/)
2. Activer WSL2 integration
3. Installer Ubuntu-22.04

### Installation

```bash
# Ouvrir WSL2
wsl

# Cloner et installer
git clone https://github.com/fs83500/TradePyBot.git
cd TradePyBot

# Démarrer
docker compose up -d
```

### Limitations

- WebSocket support limité (utiliser Docker Desktop récent)
- Performance inférieure à Linux natif
- Support GPU limité pour IA locale

---

## 🍎 Méthode 7: macOS

### Homebrew

```bash
# Installer Homebrew si non présent
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Installer Docker
brew install --cask docker

# Installer Node.js
brew install node@18

# Installer Python
brew install python@3.11
```

### Docker Desktop

```bash
# Ouvrir Docker Desktop
open -a Docker

# Attendre que Docker soit prêt
docker info
```

### Installation

```bash
# Cloner le repo
git clone https://github.com/fs83500/TradePyBot.git
cd TradePyBot

# Démarrer
docker compose up -d
```

### Développement local

```bash
# Backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn backend.main:app --reload

# Frontend
cd frontend
npm install
npm run dev
```

---

## 🔧 Configuration

### Variables d'environnement

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

# API Providers (optionnel)
GEMINI_API_KEY=your-key
CLAUDE_API_KEY=your-key
OPENAI_API_KEY=your-key
GROQ_API_KEY=your-key
DEEPSEEK_API_KEY=your-key
MISTRAL_API_KEY=your-key
```

### Tokens API

#### Obtenir les clés API

| Provider | URL | Type |
|----------|-----|------|
| Gemini | https://aistudio.google.com/app/apikey | OAuth |
| Claude | https://console.anthropic.com/settings/keys | API Key |
| OpenAI | https://platform.openai.com/api-keys | API Key |
| Groq | https://console.groq.com/keys | API Key |
| DeepSeek | https://platform.deepseek.com/api_keys | API Key |
| Mistral | https://console.mistral.ai/api-keys | API Key |

#### Configurer les clés

```bash
# Éditer le fichier .env
nano .env

# Ajouter vos clés API
GEMINI_API_KEY=AIzaSy...
CLAUDE_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-proj-...
```

### Sécurité

#### 1. Changer le secret key

```bash
# Générer une clé sécurisée
python3 -c "import secrets; print(secrets.token_urlsafe(32))"

# Utiliser dans .env
AUTH_SECRET_KEY=VOTRE-CLE-GÉNÉRÉE-ICI
```

#### 2. Activer HTTPS

Utiliser Let's Encrypt ou un service comme Cloudflare.

#### 3. Rate limiting (nginx)

```nginx
# Ajouter dans la configuration nginx
limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;

location /api {
    limit_req zone=api burst=20 nodelay;
    proxy_pass http://localhost:8000;
}
```

---

## ❓ FAQ

### Docker ne démarre pas

```bash
# Vérifier les logs
docker compose logs

# Vérifier les ports
lsof -i :8000  # Backend
lsof -i :3000  # Frontend

# Réinitialiser
docker compose down -v
docker compose up
```

### Erreur de port déjà utilisé

```bash
# Changer le port dans docker-compose.yml
# ou arrêter le service utilisant le port
sudo lsof -i :8000
sudo kill -9 <PID>
```

### Fichier .env non trouvé

```bash
# Copier l'exemple
cp .env.example .env

# Éditer
nano .env
```

### Frontend ne charge pas

```bash
# Vérifier le backend
curl http://localhost:8000/health

# Vérifier le frontend
curl http://localhost:3000
```

### Agent IA ne répond pas

```bash
# Vérifier les clés API
echo $GEMINI_API_KEY

# Vérifier la connexion internet
ping google.com

# Redémarrer le backend
docker compose restart backend
```

---

## 🐛 Problèmes connus

### WSL2 - WebSocket lents

**Solution:** Utiliser Docker Desktop récent (4.25+) avec WSL2 intégré.

### Raspberry Pi - OOM Killer

**Solution:** Réduire la mémoire des conteneurs ou augmenter le swap.

### Windows - Docker Desktop ne démarre pas

**Solution:** Activer la virtualisation dans le BIOS, installer WSL2.

### macOS - Port 8000 déjà utilisé

**Solution:** Changer le port dans `docker-compose.yml` ou arrêter le service.

---

## 📞 Support

### Documentation

- [GitHub Repository](https://github.com/fs83500/TradePyBot)
- [API Documentation](http://localhost:8000/docs)
- [Security Guide](docs/SECURITY.md)

### Communauté

- [GitHub Discussions](https://github.com/fs83500/TradePyBot/discussions)
- [Twitter](https://twitter.com/tradepybot)
- [Email](support@tradepybot.com)

### Support premium

Pour un support dédié, contactez l'équipe via GitHub.

---

## 📝 Notes

- Docker est la méthode recommandée pour la plupart des utilisateurs
- Pour le développement, utiliser la méthode locale (Method 2)
- Pour la production, utiliser la méthode serveur (Method 3)
- Les agents IA nécessitent des clés API pour fonctionner avec les modèles commerciaux

---

**Dernière mise à jour:** Mars 2026

**Auteur:** SYNTAX - TradePyBot Development Team
