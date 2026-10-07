#!/bin/bash

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
CTFD_DIR="$PROJECT_ROOT/CTFd"

BACKUP_FILE="$1"

if [ -z "$BACKUP_FILE" ]; then
    echo "Usage: $0 <backup.sql>"
    exit 1
fi

if [[ "$BACKUP_FILE" != /* ]]; then
    BACKUP_FILE="$PROJECT_ROOT/$BACKUP_FILE"
fi

if [ ! -f "$BACKUP_FILE" ]; then
    echo "[ERROR] Backup file not found:"
    echo "$BACKUP_FILE"
    exit 1
fi

echo "[+] Restoring CTFd database from:"
echo "$BACKUP_FILE"

cd "$CTFD_DIR"

docker compose exec -T db \
    mariadb -u root -pctfd ctfd \
    < "$BACKUP_FILE"

echo "[+] CTFd database restore completed."
