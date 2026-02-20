---
name: frog
description: Mikrus Frog free VPS management - Alpine Linux 256MB server with WordPress, Redis, and optimized stacks. Use when working with Frog servers, deploying apps on frogXX.mikr.us, or managing the free-tier Mikrus VPS.
domain: hosting
type: workflow
frequency: specialized
commands: []
tools: []
---

# Mikrus Frog VPS

Free-tier Alpine Linux LXC container (256MB RAM, 3GB disk) from Mikr.us. Perfect for lightweight WordPress sites, small APIs, static sites, and learning projects.

## Quick Reference

### Connection
```bash
# SSH (login as frog user, NOT root)
ssh frog@frogXX.mikr.us -p 10NNN

# Get root
sudo su
# OR prefix commands with:
echo "PASSWORD" | sudo -S <command>
```

### Identity & Ports
```
Hostname format:  f{VPS_ID}.mikr.us     (e.g., f3494.mikr.us)
Server:           frog{NN}.mikr.us       (e.g., frog03.mikr.us)
SSH port:         10000 + last 3 digits  (e.g., 10494)
HTTP port:        20000 + last 3 digits  (e.g., 20494)
Extra ports:      30NNN, 40NNN           (TCP/UDP)
```

### Web Access (wykr.es)
```
URL format: https://frogNN-PORT.wykr.es
Example:    https://frog03-20494.wykr.es

- Auto HTTPS via Cloudflare (Let's Encrypt)
- App must serve HTTP internally (NOT HTTPS)
- Only works for web traffic (not SSH/FTP)
```

### MySQL (Shared)
```bash
# Credentials stored at:
sudo cat /root/mysql.txt

# Connect (MUST use --skip-ssl on Frog):
mariadb -h 192.168.1.1 -u f{ID} -p{PASS} --skip-ssl db_f{ID}

# Capacity: ~200MB
# Version: MariaDB 10.5.x (shared, not upgradeable)
# PHPMyAdmin: https://frogNN.mikr.us/pma/
```

## Specs & Limits

| Resource | Value |
|----------|-------|
| RAM | 256MB (no swap) |
| Disk | 3GB |
| CPU | Shared |
| Network | 1Gbps shared, dedicated IPv6, shared IPv4 |
| OS | Alpine Linux (cannot change) |
| MySQL | Shared, ~200MB |
| Cost | Free (5 PLN one-time verification) |
| Limit | 1 server per user |

### What You CANNOT Do
- Install custom kernels or mount devices
- Add SWAP memory
- Run gaming/voice servers
- Port scan (instant permanent ban)
- Change the OS
- Access port 22 (not allocated)

### Allowed Outbound Ports
80, 443, 3306, 53, 20, 21, 22, 110, 143, 465, 1883, 7844, 51820, 27018

## Alpine Linux Essentials

**CRITICAL**: This is Alpine, NOT Debian/Ubuntu. Use `apk`, not `apt`.

### Package Management
```bash
apk update                    # Update package index (do first!)
apk upgrade                   # Upgrade all packages
apk add <package>             # Install package
apk del <package>             # Remove package
apk search <name>             # Search packages
apk search -v <name>          # Search with descriptions
```

### Service Management (OpenRC)
```bash
rc-update add <service> default   # Enable auto-start
rc-update del <service>           # Disable auto-start
rc-update                         # List auto-start services
rc-service <service> start        # Start service
rc-service <service> stop         # Stop service
rc-service <service> restart      # Restart service
```

### Diagnostics
```bash
df -h /                       # Disk usage
free -m                       # RAM usage
htop                          # Process monitor (q to quit)
ps auxf                       # Full process list
kill -9 <PID>                 # Kill process
cat /var/log/messages         # System log
ls /var/log/                  # App-specific logs
```

### BusyBox Gotchas
Alpine uses BusyBox which has limited versions of common tools:
- **No `grep -P`** (no Perl regex) — use `grep -E` or `sed`/`awk`
- **No `sed -i` with `\a`** (append) — use `cat > file << EOF` instead
- **No `ss` command** — use `netstat` if installed
- **No `systemctl`** — use `rc-service` and `rc-update`

## Built-in Scripts
```bash
sudo su
ls /root/scripts/

# Available installers:
/root/scripts/install_LAMP.sh          # Apache + PHP + MySQL client
/root/scripts/install_docker.sh        # Docker
/root/scripts/install_lighttpd_PHP.sh  # Lighttpd + PHP
/root/scripts/install_nginx_PHP.sh     # Nginx + PHP
```

## WordPress on Frog (Optimized Stack)

### One-Click Install Script
```bash
# Upload script:
scp -P SSH_PORT frog-wordpress.sh frog@frogXX.mikr.us:~/

# Run on server:
chmod +x frog-wordpress.sh
sudo ./frog-wordpress.sh
```

Script location: `~/.claude/main/frog-wordpress.sh`

### Stack Architecture
```
┌─────────────────────────────────┐
│  Cloudflare (HTTPS termination) │
│  frogNN-PORT.wykr.es            │
└──────────┬──────────────────────┘
           │ HTTP
┌──────────▼──────────────────────┐
│  Nginx (1 worker, port 20NNN)  │
│  gzip, static cache, xmlrpc ✗  │
└──────────┬──────────────────────┘
           │ unix socket
┌──────────▼──────────────────────┐
│  PHP 8.3 FPM (2 static workers)│
│  OPcache 32MB, 128M mem limit  │
└──────────┬───────────┬──────────┘
           │           │
┌──────────▼─────┐ ┌───▼──────────┐
│ Shared MySQL   │ │ Redis 8.x    │
│ 192.168.1.1    │ │ 16MB cap     │
│ MariaDB 10.5   │ │ object cache │
└────────────────┘ └──────────────┘
```

### Resource Footprint
| Component | RAM Usage |
|-----------|-----------|
| Nginx master + 1 worker | ~3MB |
| PHP-FPM master + 2 workers | ~25MB |
| Redis | ~1MB (grows to 16MB cap) |
| WordPress page load | ~15-20MB per request |
| **Total idle** | **~47MB / 256MB** |

### Key Configurations

**PHP-FPM** (`/etc/php83/php-fpm.d/www.conf`):
- `pm = static` with `pm.max_children = 2`
- `pm.max_requests = 200` (prevent memory leaks)
- Socket: `/run/php-fpm.sock` owned by nginx

**OPcache** (`/etc/php83/conf.d/99-wordpress.ini`):
- 32MB memory, 4000 files cached
- 60s revalidation (reduces disk I/O)
- `memory_limit = 128M`, `upload_max_filesize = 16M`

**Redis** (`/etc/redis.conf`):
- `maxmemory 16mb` with `allkeys-lru` eviction
- No persistence (pure object cache)
- `maxclients 50`, `timeout 300`

**Nginx**:
- 1 worker, 128 connections
- gzip on, static files cached 30 days
- xmlrpc.php blocked, dotfiles blocked
- `client_max_body_size 16M`

**WordPress** (`wp-config.php`):
- `DISABLE_WP_CRON = true` (system cron every 15min)
- `WP_POST_REVISIONS = 3`
- `FORCE_SSL_ADMIN = true` with X-Forwarded-Proto detection
- Redis Object Cache via PhpRedis native extension

### PHP Extensions Installed
Core WP: `mysqli`, `curl`, `gd`, `xml`, `mbstring`, `zip`, `session`, `fileinfo`, `dom`, `openssl`
Performance: `opcache`, `redis` (pecl-redis)
Extras: `intl`, `exif`, `imagick`, `sodium`, `bcmath`

### Permissions
```bash
# Full wp-content must be writable for uploads/plugins/themes:
chown -R nginx:nginx /var/www/wordpress/wp-content
chmod -R 775 /var/www/wordpress/wp-content

# wp-config.php should be restricted:
chmod 640 /var/www/wordpress/wp-config.php
```

### WP-CLI Usage
```bash
# Must use --allow-root when running as root
cd /var/www/wordpress

wp plugin install <slug> --activate --allow-root
wp theme install <slug> --activate --allow-root
wp plugin update --all --allow-root
wp core update --allow-root
wp cache flush --allow-root
wp redis status --allow-root
```

## Other App Ideas for Frog

### Static Sites
```bash
apk add nginx
# Drop HTML files in /var/www/html
# Nginx on port 20NNN → frogNN-PORT.wykr.es
```

### Go/Rust APIs
Small compiled binaries are ideal for 256MB — no runtime overhead.

### Python/FastAPI (Minimal)
```bash
apk add python3 py3-pip
pip install fastapi uvicorn
# Run on port 20NNN with --workers 1
```

### Reverse Proxy
Use Nginx to proxy to any app on localhost:
```nginx
location / {
    proxy_set_header Host $host;
    proxy_set_header X-Forwarded-For $remote_addr;
    proxy_pass http://127.0.0.1:3000;
}
```

## Troubleshooting

### "The uploaded file could not be moved"
```bash
sudo chown -R nginx:nginx /var/www/wordpress/wp-content
sudo chmod -R 775 /var/www/wordpress/wp-content
```

### "Could not create directory" (plugin/theme install)
Same fix — wp-content/upgrade/ needs nginx ownership.

### MySQL SSL error
```bash
# Frog's shared MySQL doesn't support SSL
# Use --skip-ssl flag:
mariadb -h 192.168.1.1 -u USER -pPASS --skip-ssl DB_NAME
```

### Services not running after reboot
```bash
rc-update add nginx default
rc-update add php-fpm83 default
rc-update add redis default
rc-update add crond default
```

### OOM kills (out of memory)
```bash
# Check what's eating RAM:
ps aux --sort=-%mem | head -10

# Reduce PHP-FPM workers to 1:
# Edit /etc/php83/php-fpm.d/www.conf → pm.max_children = 1

# Lower Redis cap:
# Edit /etc/redis.conf → maxmemory 8mb
```

### BusyBox sed multi-line insert fails
```bash
# DON'T use sed -i with \a or multi-line inserts
# DO use heredoc:
cat > /path/to/file << 'EOF'
content here
EOF
```

## Site Health Notes

After WordPress install, Site Health shows 4 warnings. 3 are fixable:

| Warning | Fix |
|---------|-----|
| Inactive themes | Delete with `wp theme delete` |
| Missing modules | Install php83-intl, php83-exif, php83-pecl-imagick |
| Page cache | Install Redis Object Cache plugin |
| **Outdated SQL** | **Cannot fix** — shared MariaDB 10.5, Mikrus controls it |
