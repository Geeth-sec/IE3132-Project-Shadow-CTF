#!/bin/bash

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
CTFD_DIR="$PROJECT_ROOT/CTFd"
BACKUP_DIR="$PROJECT_ROOT/deployment/backups"

TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="$BACKUP_DIR/ctfd_backup_${TIMESTAMP}.sql"

mkdir -p "$BACKUP_DIR"

echo "[+] Creating CTFd database backup..."

cd "$CTFD_DIR"

docker compose exec -T db \
    mariadb-dump -u root -pctfd ctfd \
    > "$BACKUP_FILE"

echo "[+] Backup created:"
echo "$BACKUP_FILE"
