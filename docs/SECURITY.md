# TradePyBot Security Guide

## 🔒 Vue d'ensemble

Ce document décrit les mesures de sécurité implémentées pour protéger TradePyBot.

---

## 📊 Niveaux de Sécurité

| Niveau | Description | Implémentation |
|--------|-------------|----------------|
| **Basique** | Token authentication | Gateway token unique |
| **Intermédiaire** | Rate limiting + Fail2Ban | Limite tentatives |
| **Avancé** | 2FA + IP whitelist | Double facteur |
| **Maximum** | VPN only + Hardware key | Accès restreint |

---

## 1. Authentification par Token

### Architecture
```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Client    │────▶│   Gateway   │────▶│  TradePyBot │
│  (Browser)  │     │   Token     │     │   Backend   │
└─────────────┘     └─────────────┘     └─────────────┘
                          │
                          ▼
                    Validation Token
                    (comme OpenClaw)
```

### Configuration Backend

```python
# backend/config.py
from pydantic_settings import BaseSettings
from functools import wraps
from fastapi import HTTPException, Request
from datetime import datetime, timedelta
import secrets
import time
from collections import defaultdict
from threading import Lock

class SecurityConfig(BaseSettings):
    # Token settings
    GATEWAY_TOKEN: str = ""  # Set via env
    TOKEN_HEADER: str = "X-Gateway-Token"
    
    # Rate limiting
    RATE_LIMIT_REQUESTS: int = 100
    RATE_LIMIT_WINDOW: int = 60  # seconds
    
    # Fail2Ban
    MAX_LOGIN_ATTEMPTS: int = 3
    BAN_DURATION: int = 3600  # 1 hour
    
    # IP Whitelist
    ALLOWED_IPS: list[str] = []
    
    # 2FA
    ENABLE_2FA: bool = False
    TOTP_ISSUER: str = "TradePyBot"

# Rate Limiter
class RateLimiter:
    def __init__(self, requests: int, window: int):
        self.requests = requests
        self.window = window
        self.clients = defaultdict(list)
        self.lock = Lock()
    
    def is_allowed(self, ip: str) -> bool:
        with self.lock:
            now = time.time()
            # Clean old requests
            self.clients[ip] = [t for t in self.clients[ip] if now - t < self.window]
            
            if len(self.clients[ip]) >= self.requests:
                return False
            
            self.clients[ip].append(now)
            return True

# Login Attempt Tracker
class LoginTracker:
    def __init__(self, max_attempts: int, ban_duration: int):
        self.max_attempts = max_attempts
        self.ban_duration = ban_duration
        self.attempts = defaultdict(list)
        self.banned = {}
        self.lock = Lock()
    
    def is_banned(self, ip: str) -> bool:
        with self.lock:
            if ip in self.banned:
                if time.time() < self.banned[ip]:
                    return True
                del self.banned[ip]
            return False
    
    def record_attempt(self, ip: str, success: bool) -> bool:
        with self.lock:
            now = time.time()
            
            if success:
                self.attempts[ip] = []
                return True
            
            self.attempts[ip].append(now)
            
            # Clean old attempts
            self.attempts[ip] = [t for t in self.attempts[ip] if now - t < 3600]
            
            if len(self.attempts[ip]) >= self.max_attempts:
                self.banned[ip] = now + self.ban_duration
                return False
            
            return True
    
    def get_remaining_attempts(self, ip: str) -> int:
        with self.lock:
            return max(0, self.max_attempts - len(self.attempts[ip]))
```

---

## 2. Middleware de Sécurité

```python
# backend/api/auth.py
from fastapi import Request, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import datetime
import logging

logger = logging.getLogger("tradepybot.security")

security = HTTPBearer()
rate_limiter = RateLimiter(100, 60)
login_tracker = LoginTracker(3, 3600)

async def verify_token(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Verify gateway token with rate limiting and fail2ban."""
    
    client_ip = request.client.host
    
    # Check if IP is banned
    if login_tracker.is_banned(client_ip):
        logger.warning(f"Banned IP attempted access: {client_ip}")
        raise HTTPException(
            status_code=403,
            detail="IP temporarily banned. Try again later."
        )
    
    # Rate limiting
    if not rate_limiter.is_allowed(client_ip):
        logger.warning(f"Rate limited: {client_ip}")
        raise HTTPException(
            status_code=429,
            detail="Too many requests. Please slow down."
        )
    
    # Verify token
    token = credentials.credentials
    
    if token != config.GATEWAY_TOKEN:
        login_tracker.record_attempt(client_ip, success=False)
        remaining = login_tracker.get_remaining_attempts(client_ip)
        
        logger.error(
            f"Authentication failed for token from {client_ip} - "
            f"Remaining attempts: {remaining}"
        )
        
        raise HTTPException(
            status_code=401,
            detail=f"Invalid token. Remaining attempts: {remaining}"
        )
    
    login_tracker.record_attempt(client_ip, success=True)
    logger.info(f"Successful login from {client_ip}")
    
    return {"ip": client_ip, "authenticated": True}

# IP Whitelist Middleware
async def ip_whitelist_middleware(request: Request, call_next):
    if config.ALLOWED_IPS:
        client_ip = request.client.host
        if client_ip not in config.ALLOWED_IPS:
            logger.warning(f"Blocked non-whitelisted IP: {client_ip}")
            raise HTTPException(status_code=403, detail="Access denied")
    
    return await call_next(request)
```

---

## 3. Fail2Ban Configuration

### Installation

```bash
# Ubuntu/Debian
sudo apt install fail2ban

# Créer les configs
sudo cp security/fail2ban/jail.conf /etc/fail2ban/jail.d/tradepybot.conf
sudo cp security/fail2ban/filter.conf /etc/fail2ban/filter.d/tradepybot.conf

# Redémarrer fail2ban
sudo systemctl restart fail2ban
sudo fail2ban-client status tradepybot
```

### Logs Backend

```python
# backend/logging_config.py
import logging
from logging.handlers import RotatingFileHandler

def setup_security_logging():
    """Setup security logging for Fail2Ban."""
    
    logger = logging.getLogger("tradepybot.auth")
    logger.setLevel(logging.INFO)
    
    handler = RotatingFileHandler(
        "/var/log/tradepybot/auth.log",
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5
    )
    
    formatter = logging.Formatter(
        '%(asctime)s [%(levelname)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    return logger

# Usage in auth.py
logger = setup_security_logging()

def log_auth_event(ip: str, event: str, success: bool):
    if success:
        logger.info(f"Successful login from {ip}")
    else:
        logger.warning(f"Authentication failed for token from {ip}")
```

---

## 4. 2FA (TOTP)

### Backend

```python
# backend/api/twofa.py
import pyotp
import qrcode
from io import BytesIO
import base64

class TwoFactorAuth:
    def __init__(self, secret: str = None):
        self.secret = secret or pyotp.random_base32()
        self.totp = pyotp.TOTP(self.secret)
    
    def verify(self, code: str) -> bool:
        """Verify TOTP code (valid for 30s)."""
        return self.totp.verify(code, valid_window=1)
    
    def get_qr_code(self, email: str) -> str:
        """Generate QR code for authenticator app."""
        uri = pyotp.totp.TOTP(self.secret).provisioning_uri(
            name=email,
            issuer_name="TradePyBot"
        )
        
        img = qrcode.make(uri)
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        
        return base64.b64encode(buffer.getvalue()).decode()

# API Endpoint
@app.post("/api/auth/2fa/enable")
async def enable_2fa(user: dict = Depends(verify_token)):
    twofa = TwoFactorAuth()
    qr_code = twofa.get_qr_code(user["email"])
    
    return {
        "secret": twofa.secret,
        "qr_code": f"data:image/png;base64,{qr_code}",
        "message": "Scan with Google Authenticator or Authy"
    }

@app.post("/api/auth/2fa/verify")
async def verify_2fa(
    code: str,
    user: dict = Depends(verify_token)
):
    if not user.get("2fa_secret"):
        raise HTTPException(400, "2FA not enabled")
    
    twofa = TwoFactorAuth(user["2fa_secret"])
    
    if not twofa.verify(code):
        raise HTTPException(401, "Invalid 2FA code")
    
    return {"verified": True}
```

---

## 5. HTTPS & Certificats

### Let's Encrypt (Gratuit)

```bash
# Installation
sudo apt install certbot python3-certbot-nginx

# Générer certificat
sudo certbot --nginx -d tradepybot.example.com

# Auto-renouvellement
sudo systemctl enable certbot.timer
```

### Nginx Config

```nginx
# /etc/nginx/sites-available/tradepybot
server {
    listen 80;
    server_name tradepybot.example.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name tradepybot.example.com;

    ssl_certificate /etc/letsencrypt/live/tradepybot.example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/tradepybot.example.com/privkey.pem;

    # Security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Content-Security-Policy "default-src 'self'" always;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

---

## 6. IP Whitelist (Optionnel)

### Configuration

```python
# backend/config.py
class SecurityConfig(BaseSettings):
    # IP Whitelist (comma-separated in env)
    ALLOWED_IPS: list[str] = []
    
    @validator("ALLOWED_IPS", pre=True)
    def parse_ips(cls, v):
        if isinstance(v, str):
            return [ip.strip() for ip in v.split(",")]
        return v

# Middleware
@app.middleware("http")
async def ip_filter(request: Request, call_next):
    if config.ALLOWED_IPS:
        client_ip = request.client.host
        if client_ip not in config.ALLOWED_IPS:
            logger.warning(f"Blocked IP: {client_ip}")
            raise HTTPException(status_code=403, detail="Access denied")
    
    return await call_next(request)
```

### Environnement (.env)

```bash
# .env
ALLOWED_IPS=192.168.1.100,10.0.0.50,203.0.113.0
```

---

## 7. VPN Only (Maximum Security)

### WireGuard Setup

```bash
# Installation
sudo apt install wireguard

# Générer les clés
wg genkey | tee privatekey | wg pubkey > publickey

# Config serveur
cat > /etc/wireguard/wg0.conf << EOF
[Interface]
Address = 10.0.0.1/24
SaveConfig = true
PostUp = iptables -A FORWARD -i wg0 -j ACCEPT
PostDown = iptables -D FORWARD -i wg0 -j ACCEPT
ListenPort = 51820
PrivateKey = $(cat privatekey)

[Peer]
PublicKey = CLIENT_PUBLIC_KEY
AllowedIPs = 10.0.0.2/32
EOF

# Démarrer
sudo systemctl enable wg-quick@wg0
sudo systemctl start wg-quick@wg0
```

### Client Config

```ini
[Interface]
Address = 10.0.0.2/24
PrivateKey = CLIENT_PRIVATE_KEY
DNS = 1.1.1.1

[Peer]
PublicKey = SERVER_PUBLIC_KEY
Endpoint = tradepybot.example.com:51820
AllowedIPs = 10.0.0.0/24
PersistentKeepalive = 25
```

### TradePyBot Config (VPN Only)

```python
# backend/config.py
class SecurityConfig(BaseSettings):
    # VPN only - listen only on VPN interface
    HOST: str = "10.0.0.1"
    PORT: int = 8000
    
    # Allow only VPN subnet
    ALLOWED_IPS: list[str] = ["10.0.0.0/24"]
```

---

## 8. Audit & Monitoring

### Logging

```python
# backend/logging_config.py
import logging
import json
from datetime import datetime

class SecurityLogger:
    def __init__(self, log_file: str = "/var/log/tradepybot/audit.log"):
        self.logger = logging.getLogger("tradepybot.audit")
        handler = logging.FileHandler(log_file)
        handler.setFormatter(logging.Formatter('%(message)s'))
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)
    
    def log_event(self, event_type: str, ip: str, details: dict):
        event = {
            "timestamp": datetime.utcnow().isoformat(),
            "type": event_type,
            "ip": ip,
            **details
        }
        self.logger.info(json.dumps(event))
    
    def log_login_success(self, ip: str, user: str):
        self.log_event("LOGIN_SUCCESS", ip, {"user": user})
    
    def log_login_failed(self, ip: str, reason: str):
        self.log_event("LOGIN_FAILED", ip, {"reason": reason})
    
    def log_ip_banned(self, ip: str, duration: int):
        self.log_event("IP_BANNED", ip, {"duration": duration})
    
    def log_trade_executed(self, ip: str, trade: dict):
        self.log_event("TRADE_EXECUTED", ip, trade)
```

---

## 9. Checklist de Sécurité

| Mesure | Status | Priorité |
|--------|--------|----------|
| Token authentication | ✅ | Critique |
| Rate limiting | ✅ | Haute |
| Fail2Ban | ✅ | Haute |
| HTTPS (Let's Encrypt) | ✅ | Critique |
| Security headers | ✅ | Haute |
| 2FA (TOTP) | ⚪ Optionnel | Moyenne |
| IP Whitelist | ⚪ Optionnel | Moyenne |
| VPN only | ⚪ Optionnel | Basse |
| Audit logging | ✅ | Haute |

---

## 10. Commandes Utiles

```bash
# Vérifier status fail2ban
sudo fail2ban-client status tradepybot

# Débannir une IP
sudo fail2ban-client set tradepybot unbanip 192.168.1.100

# Voir les logs
tail -f /var/log/tradepybot/auth.log

# Vérifier les connexions actives
ss -tlnp | grep 8000

# Vérifier HTTPS
curl -I https://tradepybot.example.com
```

---

*Dernière mise à jour: 2026-03-03*