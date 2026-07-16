#!/bin/bash
# ============================================================
# AI Universe — Server Update Script
# Yeh script SERVER pe run hoti hai (auto via deploy.bat)
# GitHub se latest code pull karta hai + services restart
# ============================================================

set -e

APP_DIR="/home/ubuntu/ai-universe-django"
cd "$APP_DIR"

echo ""
echo "======================================"
echo "  🚀 Server Update Starting..."
echo "======================================"

# 1. Latest code pull karo
echo "[1/4] GitHub se latest code pull kar raha hoon..."
git pull origin main

# 2. Dependencies update karo (agar kuch naya add hua ho)
echo "[2/4] Dependencies check kar raha hoon..."
source venv/bin/activate
pip install -r requirements.txt -q

# 3. Static files collect karo
echo "[3/4] Static files collect kar raha hoon..."
python manage.py collectstatic --noinput

# 4. Gunicorn restart karo
echo "[4/4] Gunicorn service restart kar raha hoon..."
sudo systemctl restart ai-universe

echo ""
echo "======================================"
echo "  ✅ Update Complete!"
echo "  App: http://157.151.152.144"
echo "======================================"
