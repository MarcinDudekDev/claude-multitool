#!/bin/sh
# ============================================================================
# WordPress on Mikrus Frog — One-Click Installer
# ============================================================================
# Optimized for 256MB RAM / 3GB disk Alpine Linux LXC containers
#
# Usage:
#   1. scp this file to your Frog VPS:
#      scp -P YOUR_SSH_PORT frog-wordpress.sh frog@frogXX.mikr.us:~/
#   2. SSH in and run:
#      chmod +x frog-wordpress.sh && sudo ./frog-wordpress.sh
#
# What it installs:
#   - Nginx (1 worker, low memory)
#   - PHP 8.3 FPM (2 static workers, OPcache)
#   - Redis 8.x (16MB cap, object cache)
#   - WordPress (latest) with WP-CLI
#   - Redis Object Cache plugin
#
# Requirements:
#   - Mikrus Frog VPS (Alpine Linux)
#   - Run as root (sudo)
#   - MySQL credentials in /root/mysql.txt (auto-provisioned by Mikrus)
# ============================================================================

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

log()   { printf "${GREEN}[+]${NC} %s\n" "$1"; }
warn()  { printf "${YELLOW}[!]${NC} %s\n" "$1"; }
error() { printf "${RED}[✗]${NC} %s\n" "$1"; exit 1; }
info()  { printf "${CYAN}[i]${NC} %s\n" "$1"; }

# ============================================================================
# Pre-flight checks
# ============================================================================

if [ "$(id -u)" -ne 0 ]; then
    error "Must run as root. Use: sudo ./frog-wordpress.sh"
fi

if ! grep -q "Alpine" /etc/os-release 2>/dev/null; then
    error "This script is designed for Alpine Linux (Mikrus Frog)"
fi

# ============================================================================
# Auto-detect VPS identity
# ============================================================================

HOSTNAME=$(hostname)
# Hostname format: f3494.mikr.us → VPS_ID=3494, SUFFIX=494
VPS_ID=$(echo "$HOSTNAME" | sed 's/\..*//; s/^f//')
PORT_SUFFIX=$(echo "$VPS_ID" | sed 's/^[0-9]*//' | tail -c 4)
# Fallback: use last 3 digits
if [ -z "$PORT_SUFFIX" ]; then
    PORT_SUFFIX=$(echo "$VPS_ID" | grep -o '...$')
fi

# Detect which frog server we're on from /etc/resolv.conf or hostname
FROG_SERVER=$(echo "$HOSTNAME" | sed 's/^f[0-9]*//' | sed 's/\.mikr\.us//')
if [ -z "$FROG_SERVER" ]; then
    # Try to get from SSH connection
    FROG_SERVER=$(who -m 2>/dev/null | grep -o 'frog[0-9]*' | head -1)
fi

# Port for HTTP (first of the three assigned ports: 20xxx)
WEB_PORT="20${PORT_SUFFIX}"

info "VPS ID: f${VPS_ID}"
info "HTTP port: ${WEB_PORT}"

# ============================================================================
# Read MySQL credentials
# ============================================================================

MYSQL_FILE="/root/mysql.txt"
if [ ! -f "$MYSQL_FILE" ]; then
    error "MySQL credentials not found at $MYSQL_FILE"
fi

DB_HOST=$(grep "Serwer:" "$MYSQL_FILE" | awk '{print $2}')
DB_USER=$(grep "dbuser:" "$MYSQL_FILE" | awk '{print $2}')
DB_PASS=$(grep "dbpass:" "$MYSQL_FILE" | awk '{print $2}')
DB_NAME=$(grep "dbname:" "$MYSQL_FILE" | awk '{print $2}')

if [ -z "$DB_HOST" ] || [ -z "$DB_USER" ] || [ -z "$DB_PASS" ] || [ -z "$DB_NAME" ]; then
    error "Could not parse MySQL credentials from $MYSQL_FILE"
fi

log "MySQL: ${DB_USER}@${DB_HOST}/${DB_NAME}"

# ============================================================================
# User configuration
# ============================================================================

printf "\n${CYAN}=== WordPress Configuration ===${NC}\n\n"

# Site title
printf "Site title [Frog WP]: "
read SITE_TITLE
SITE_TITLE="${SITE_TITLE:-Frog WP}"

# Admin user
printf "Admin username [admin]: "
read ADMIN_USER
ADMIN_USER="${ADMIN_USER:-admin}"

# Admin password
printf "Admin password [auto-generate]: "
read ADMIN_PASS
if [ -z "$ADMIN_PASS" ]; then
    ADMIN_PASS=$(head -c 32 /dev/urandom | base64 | tr -dc 'a-zA-Z0-9!@#' | head -c 16)
    info "Generated password: ${ADMIN_PASS}"
fi

# Admin email
printf "Admin email: "
read ADMIN_EMAIL
while [ -z "$ADMIN_EMAIL" ]; do
    printf "Admin email (required): "
    read ADMIN_EMAIL
done

# Detect site URL
# Ask user which frog server they're on if we couldn't detect it
if [ -z "$FROG_SERVER" ]; then
    printf "Which frog server? (e.g., frog01, frog03): "
    read FROG_SERVER_INPUT
    FROG_SERVER_NAME="${FROG_SERVER_INPUT}"
else
    FROG_SERVER_NAME="frog${FROG_SERVER}"
fi

# If still empty, ask directly
if [ -z "$FROG_SERVER_NAME" ] || [ "$FROG_SERVER_NAME" = "frog" ]; then
    printf "Enter your frog server name (e.g., frog03): "
    read FROG_SERVER_NAME
fi

SITE_URL="https://${FROG_SERVER_NAME}-${WEB_PORT}.wykr.es"

printf "\nSite URL will be: ${CYAN}${SITE_URL}${NC}\n"
printf "Custom domain instead? (leave empty for wykr.es): "
read CUSTOM_DOMAIN
if [ -n "$CUSTOM_DOMAIN" ]; then
    SITE_URL="https://${CUSTOM_DOMAIN}"
fi

printf "\n${YELLOW}Installing WordPress at ${SITE_URL}${NC}\n"
printf "Press Enter to continue or Ctrl+C to abort..."
read _CONFIRM

# ============================================================================
# Phase 1: System packages
# ============================================================================

log "Updating package index..."
apk update -q

log "Installing Nginx, PHP 8.3, Redis, and tools..."
apk add -q \
    nginx \
    php83 php83-fpm \
    php83-mysqli php83-curl php83-gd php83-xml php83-mbstring \
    php83-zip php83-json php83-opcache php83-session php83-fileinfo \
    php83-dom php83-tokenizer php83-ctype php83-iconv php83-openssl \
    php83-phar php83-simplexml php83-xmlreader php83-xmlwriter \
    php83-intl php83-exif php83-pecl-imagick php83-pecl-redis \
    php83-sodium php83-bcmath \
    redis \
    imagemagick \
    mysql-client \
    curl

# Create php symlink
ln -sf /usr/bin/php83 /usr/bin/php 2>/dev/null || true

log "Packages installed"

# ============================================================================
# Phase 2: PHP-FPM configuration
# ============================================================================

log "Configuring PHP-FPM (2 workers, OPcache)..."

cat > /etc/php83/php-fpm.d/www.conf << 'EOF'
[www]
user = nginx
group = nginx
listen = /run/php-fpm.sock
listen.owner = nginx
listen.group = nginx
listen.mode = 0660

; Static pool — predictable memory usage
pm = static
pm.max_children = 2
pm.max_requests = 200

; Slow log
slowlog = /var/log/php83/slow.log
request_slowlog_timeout = 10s
EOF

cat > /etc/php83/conf.d/99-wordpress.ini << 'EOF'
; Memory
memory_limit = 128M
upload_max_filesize = 16M
post_max_size = 16M
max_execution_time = 60
max_input_vars = 3000

; OPcache — critical for performance
opcache.enable = 1
opcache.memory_consumption = 32
opcache.interned_strings_buffer = 4
opcache.max_accelerated_files = 4000
opcache.revalidate_freq = 60
opcache.fast_shutdown = 1
opcache.enable_file_override = 1

; Security
expose_php = Off
EOF

mkdir -p /var/log/php83
chown nginx:nginx /var/log/php83

# ============================================================================
# Phase 3: Redis configuration
# ============================================================================

log "Configuring Redis (16MB cap, no persistence)..."

cat > /etc/redis.conf << 'EOF'
bind 127.0.0.1
port 6379
daemonize yes
pidfile /run/redis/redis.pid
dir /var/lib/redis

# Memory cap
maxmemory 16mb
maxmemory-policy allkeys-lru

# No persistence — pure object cache
save ""
appendonly no
rdbcompression no

# Low resource usage
maxclients 50
timeout 300
tcp-keepalive 60

# Logging
loglevel warning
logfile /var/log/redis/redis.log
EOF

mkdir -p /run/redis /var/log/redis /var/lib/redis
chown redis:redis /run/redis /var/log/redis /var/lib/redis

# ============================================================================
# Phase 4: Nginx configuration
# ============================================================================

log "Configuring Nginx on port ${WEB_PORT}..."

cat > /etc/nginx/nginx.conf << 'EOF'
user nginx;
worker_processes 1;
pid /run/nginx/nginx.pid;
error_log /var/log/nginx/error.log warn;

events {
    worker_connections 128;
    multi_accept on;
}

http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 30;
    types_hash_max_size 2048;

    access_log /var/log/nginx/access.log;

    include /etc/nginx/http.d/*.conf;
}
EOF

cat > /etc/nginx/http.d/wordpress.conf << NGINXEOF
server {
    listen ${WEB_PORT};
    listen [::]:${WEB_PORT};
    server_name _;

    root /var/www/wordpress;
    index index.php index.html;

    # Security headers
    add_header X-Frame-Options SAMEORIGIN;
    add_header X-Content-Type-Options nosniff;

    # Gzip
    gzip on;
    gzip_types text/css application/javascript application/json text/xml application/xml text/plain;
    gzip_min_length 256;

    # Max upload
    client_max_body_size 16M;

    # Block xmlrpc
    location = /xmlrpc.php { deny all; }

    # Block dotfiles
    location ~ /\\. { deny all; }

    location / {
        try_files \$uri \$uri/ /index.php?\$args;
    }

    location ~ \\.php\$ {
        fastcgi_pass unix:/run/php-fpm.sock;
        fastcgi_index index.php;
        fastcgi_param SCRIPT_FILENAME \$document_root\$fastcgi_script_name;
        include fastcgi_params;
        fastcgi_param PATH_INFO \$fastcgi_path_info;
        fastcgi_read_timeout 60s;
        fastcgi_buffer_size 16k;
        fastcgi_buffers 4 16k;
    }

    # Static file caching
    location ~* \\.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)\$ {
        expires 30d;
        add_header Cache-Control "public, immutable";
        access_log off;
    }

    # Deny sensitive files
    location ~* (wp-config\\.php|readme\\.html|license\\.txt)\$ {
        deny all;
    }
}
NGINXEOF

rm -f /etc/nginx/http.d/default.conf
mkdir -p /run/nginx

# ============================================================================
# Phase 5: WordPress installation
# ============================================================================

log "Downloading WordPress..."
cd /tmp
curl -sL https://wordpress.org/latest.tar.gz -o wordpress.tar.gz
tar xzf wordpress.tar.gz
rm wordpress.tar.gz

rm -rf /var/www/wordpress 2>/dev/null
mv /tmp/wordpress /var/www/wordpress

log "Fetching security salts..."
SALTS=$(curl -sL https://api.wordpress.org/secret-key/1.1/salt/)

log "Writing wp-config.php..."
cat > /var/www/wordpress/wp-config.php << WPEOF
<?php
/** Database */
define( 'DB_NAME',     '${DB_NAME}' );
define( 'DB_USER',     '${DB_USER}' );
define( 'DB_PASSWORD', '${DB_PASS}' );
define( 'DB_HOST',     '${DB_HOST}' );
define( 'DB_CHARSET',  'utf8mb4' );
define( 'DB_COLLATE',  '' );

/** Security Salts */
${SALTS}

\$table_prefix = 'wp_';

define( 'WP_DEBUG', false );

/** Performance — optimized for 256MB */
define( 'WP_MEMORY_LIMIT',     '128M' );
define( 'WP_MAX_MEMORY_LIMIT', '128M' );
define( 'WP_POST_REVISIONS',   3 );
define( 'AUTOSAVE_INTERVAL',   300 );
define( 'EMPTY_TRASH_DAYS',    7 );
define( 'DISABLE_WP_CRON',     true );

/** Site URL */
define( 'WP_HOME',    '${SITE_URL}' );
define( 'WP_SITEURL', '${SITE_URL}' );

/** HTTPS — wykr.es proxy handles SSL termination */
define( 'FORCE_SSL_ADMIN', true );
if ( isset( \$_SERVER['HTTP_X_FORWARDED_PROTO'] ) && \$_SERVER['HTTP_X_FORWARDED_PROTO'] === 'https' ) {
    \$_SERVER['HTTPS'] = 'on';
}

/** Redis Object Cache */
define( 'WP_REDIS_HOST',         '127.0.0.1' );
define( 'WP_REDIS_PORT',         6379 );
define( 'WP_REDIS_TIMEOUT',      1 );
define( 'WP_REDIS_READ_TIMEOUT', 1 );
define( 'WP_REDIS_DATABASE',     0 );
define( 'WP_REDIS_CLIENT',       'phpredis' );

if ( ! defined( 'ABSPATH' ) ) {
    define( 'ABSPATH', __DIR__ . '/' );
}

require_once ABSPATH . 'wp-settings.php';
WPEOF

chown -R nginx:nginx /var/www/wordpress
chmod 640 /var/www/wordpress/wp-config.php

# Ensure wp-content is fully writable (uploads, upgrades, plugin installs)
mkdir -p /var/www/wordpress/wp-content/uploads
mkdir -p /var/www/wordpress/wp-content/upgrade
chown -R nginx:nginx /var/www/wordpress/wp-content
chmod -R 775 /var/www/wordpress/wp-content

# ============================================================================
# Phase 6: Install WP-CLI
# ============================================================================

log "Installing WP-CLI..."
curl -sL https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/wp-cli.phar -o /usr/local/bin/wp
chmod +x /usr/local/bin/wp

# ============================================================================
# Phase 7: Start services
# ============================================================================

log "Starting services..."

# Stop any existing instances
killall nginx php-fpm83 redis-server 2>/dev/null || true
sleep 1

mkdir -p /run/php-fpm /run/redis /run/nginx

redis-server /etc/redis.conf
php-fpm83
nginx

# Wait for services
sleep 2

# Verify services are running
FAIL=0
if ! pgrep -x nginx > /dev/null; then
    error "Nginx failed to start"
    FAIL=1
fi
if ! pgrep -f php-fpm83 > /dev/null; then
    error "PHP-FPM failed to start"
    FAIL=1
fi
if ! redis-cli ping 2>/dev/null | grep -q PONG; then
    error "Redis failed to start"
    FAIL=1
fi

if [ "$FAIL" -eq 1 ]; then
    error "One or more services failed to start"
fi

log "All services running"

# ============================================================================
# Phase 8: WordPress setup via WP-CLI
# ============================================================================

log "Running WordPress installer..."
cd /var/www/wordpress

wp core install \
    --url="${SITE_URL}" \
    --title="${SITE_TITLE}" \
    --admin_user="${ADMIN_USER}" \
    --admin_password="${ADMIN_PASS}" \
    --admin_email="${ADMIN_EMAIL}" \
    --skip-email \
    --allow-root

log "Installing Redis Object Cache plugin..."
wp plugin install redis-cache --activate --allow-root
wp redis enable --allow-root

log "Cleaning up defaults..."
# Remove inactive themes
for theme in twentytwentyfour twentytwentythree; do
    wp theme delete "$theme" --allow-root 2>/dev/null || true
done

# Disable pingbacks
wp option update default_pingback_flag 0 --allow-root
wp option update default_ping_status closed --allow-root
wp option update default_comment_status closed --allow-root

# Set clean permalinks
wp rewrite structure '/%postname%/' --allow-root
wp rewrite flush --allow-root

# Delete default content
wp post delete 1 --force --allow-root 2>/dev/null || true
wp post delete 2 --force --allow-root 2>/dev/null || true
wp post delete 3 --force --allow-root 2>/dev/null || true

# Set timezone
wp option update timezone_string "Europe/Warsaw" --allow-root

# ============================================================================
# Phase 9: Enable auto-start on boot
# ============================================================================

log "Enabling auto-start..."
rc-update add nginx default 2>/dev/null || true
rc-update add php-fpm83 default 2>/dev/null || true
rc-update add redis default 2>/dev/null || true

# System cron for WP-Cron (every 15 min)
echo "*/15 * * * * cd /var/www/wordpress && /usr/bin/php83 wp-cron.php > /dev/null 2>&1" | crontab -
rc-update add crond default 2>/dev/null || true
crond 2>/dev/null || true

# ============================================================================
# Phase 10: Verification
# ============================================================================

log "Verifying installation..."

HTTP_CODE=$(curl -so /dev/null -w '%{http_code}' "http://127.0.0.1:${WEB_PORT}/" 2>/dev/null)
if [ "$HTTP_CODE" = "200" ] || [ "$HTTP_CODE" = "301" ] || [ "$HTTP_CODE" = "302" ]; then
    log "WordPress responding (HTTP ${HTTP_CODE})"
else
    warn "WordPress returned HTTP ${HTTP_CODE} — may need external access to verify"
fi

REDIS_STATUS=$(cd /var/www/wordpress && wp redis status --allow-root 2>&1 | grep "Status:" | awk '{print $2}')
if [ "$REDIS_STATUS" = "Connected" ]; then
    log "Redis Object Cache: Connected"
else
    warn "Redis Object Cache: ${REDIS_STATUS:-unknown}"
fi

# ============================================================================
# Summary
# ============================================================================

WP_VERSION=$(cd /var/www/wordpress && wp core version --allow-root 2>/dev/null)
REDIS_VERSION=$(redis-cli info server 2>/dev/null | grep redis_version | cut -d: -f2 | tr -d '\r')
PHP_VERSION=$(php83 -v 2>/dev/null | head -1 | awk '{print $2}')
RAM_USED=$(free -m | awk '/Mem:/{print $3}')
RAM_TOTAL=$(free -m | awk '/Mem:/{print $2}')
DISK_USED=$(df -h / | awk 'NR==2{print $3}')
DISK_AVAIL=$(df -h / | awk 'NR==2{print $4}')

printf "\n"
printf "${GREEN}============================================================${NC}\n"
printf "${GREEN}  WordPress installed successfully!${NC}\n"
printf "${GREEN}============================================================${NC}\n"
printf "\n"
printf "  ${CYAN}Site URL:${NC}    %s\n" "${SITE_URL}"
printf "  ${CYAN}Admin:${NC}       %s/wp-admin/\n" "${SITE_URL}"
printf "  ${CYAN}Username:${NC}    %s\n" "${ADMIN_USER}"
printf "  ${CYAN}Password:${NC}    %s\n" "${ADMIN_PASS}"
printf "\n"
printf "  ${CYAN}WordPress:${NC}   %s\n" "${WP_VERSION}"
printf "  ${CYAN}PHP:${NC}         %s\n" "${PHP_VERSION}"
printf "  ${CYAN}Redis:${NC}       %s (16MB cap)\n" "${REDIS_VERSION}"
printf "  ${CYAN}RAM:${NC}         %sMB / %sMB\n" "${RAM_USED}" "${RAM_TOTAL}"
printf "  ${CYAN}Disk:${NC}        %s used, %s free\n" "${DISK_USED}" "${DISK_AVAIL}"
printf "\n"
printf "  ${YELLOW}Optimizations:${NC}\n"
printf "    - OPcache: 32MB, 4000 files\n"
printf "    - PHP-FPM: 2 static workers\n"
printf "    - Redis: object cache, allkeys-lru\n"
printf "    - Nginx: gzip, static caching, xmlrpc blocked\n"
printf "    - WP-Cron: system cron (every 15min)\n"
printf "    - Revisions: max 3, trash: 7 days\n"
printf "\n"
printf "${GREEN}============================================================${NC}\n"
