#!/bin/bash
# ============================================================
# AI Universe Django App — Oracle Cloud Setup Script
# Run this ONCE on a fresh Ubuntu 22.04 OCI instance
# Usage: chmod +x setup.sh && sudo ./setup.sh
# ============================================================

set -e  # Exit on error

APP_USER="ubuntu"
APP_DIR="/home/ubuntu/ai-universe-django"
REPO_URL="https://github.com/Pragnesh29/ai-universe-django.git"

echo "============================================"
echo "  AI Universe Django — OCI Deployment Setup"
echo "============================================"

# 1. Update system
echo "[1/10] Updating system packages..."
apt-get update -q && apt-get upgrade -y -q

# 2. Install Python, pip, nginx, git
echo "[2/10] Installing Python, Nginx, Git..."
apt-get install -y python3 python3-pip python3-venv nginx git curl

# 3. Clone the repo
echo "[3/10] Cloning repository from GitHub..."
if [ -d "$APP_DIR" ]; then
    echo "Directory exists — pulling latest..."
    cd "$APP_DIR" && git pull
else
    git clone "$REPO_URL" "$APP_DIR"
fi
cd "$APP_DIR"

# 4. Create virtualenv & install dependencies
echo "[4/10] Setting up Python virtual environment..."
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip -q
pip install -r requirements.txt -q

# 5. Collect static files
echo "[5/10] Collecting static files..."
python manage.py collectstatic --noinput

# 6. Run migrations
echo "[6/10] Running database migrations..."
python manage.py migrate

# 7. Create gunicorn systemd service
echo "[7/10] Creating Gunicorn systemd service..."
cat > /etc/systemd/system/ai-universe.service << EOF
[Unit]
Description=AI Universe Django Gunicorn
After=network.target

[Service]
User=$APP_USER
Group=www-data
WorkingDirectory=$APP_DIR
Environment="PATH=$APP_DIR/venv/bin"
ExecStart=$APP_DIR/venv/bin/gunicorn \
    --workers 3 \
    --bind unix:$APP_DIR/ai_universe.sock \
    ai_showcase.wsgi:application
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# 8. Enable and start gunicorn service
echo "[8/10] Starting Gunicorn service..."
systemctl daemon-reload
systemctl enable ai-universe
systemctl start ai-universe

# 9. Configure Nginx
echo "[9/10] Configuring Nginx..."
PUBLIC_IP=$(curl -s http://checkip.amazonaws.com || echo "YOUR_SERVER_IP")

cat > /etc/nginx/sites-available/ai-universe << EOF
server {
    listen 80;
    server_name $PUBLIC_IP;

    location = /favicon.ico { access_log off; log_not_found off; }

    location /static/ {
        alias $APP_DIR/staticfiles/;
    }

    location /media/ {
        alias $APP_DIR/media/;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:$APP_DIR/ai_universe.sock;
    }
}
EOF

ln -sf /etc/nginx/sites-available/ai-universe /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default
nginx -t && systemctl restart nginx
systemctl enable nginx

# 10. Open firewall (OCI iptables)
echo "[10/10] Configuring firewall rules..."
iptables -I INPUT 6 -m state --state NEW -p tcp --dport 80 -j ACCEPT
iptables -I INPUT 7 -m state --state NEW -p tcp --dport 443 -j ACCEPT
netfilter-persistent save 2>/dev/null || true
apt-get install -y iptables-persistent -q && netfilter-persistent save

echo ""
echo "============================================"
echo "  DEPLOYMENT COMPLETE!"
echo "  App running at: http://$PUBLIC_IP"
echo "============================================"
