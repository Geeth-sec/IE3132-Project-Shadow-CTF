# CyberTrace: Project Shadow
## CTF Platform & Architecture

### 1. Platform

The CTF platform uses CTFd as the central platform for:

- Participant accounts
- Challenge descriptions
- Hints
- Scoring
- Exact flag validation

### 2. Control Zone

The control plane consists of:

- Nginx
- CTFd
- MariaDB
- Redis

Nginx provides the participant-facing web entry point.

CTFd communicates with MariaDB and Redis through an internal Docker network.

MariaDB and Redis are not directly exposed to participants.

### 3. Challenge Zones

The proposed architecture separates the challenge environments from the control services.

#### File Challenge Zone

Used for:

- PS-01 – Hidden Blueprint
- PS-02 – Encrypted Research Note
- PS-04 – Recovered Evidence Drive
- PS-05 – Suspicious Network Session

These stages use prepared downloadable artefacts.

#### Web Challenge Zone

PS-03 – Compromised Developer Portal

- Flask + SQLite
- Docker container
- TCP 8083
- Resource limits
- Non-root execution
- No Docker socket
- No outbound Internet access

#### System Challenge Zone

PS-06 – Shadow Core Server

- Ubuntu Server virtual machine
- SSH
- TCP 2226
- Host-only networking
- No Internet route
- Snapshot-based reset

### 4. Current Local Implementation

The CTFd control plane has been deployed locally using Docker Compose.

Current services:

- Nginx
- CTFd
- MariaDB
- Redis

Networks:

- ctfd_default
- ctfd_internal

The ctfd_internal network is marked as internal and is used for CTFd, MariaDB and Redis communication.

### 5. Participant Access

Development access: http://localhost

The final proposed architecture uses a participant-facing HTTPS entry point.

### 6. Security Principles

The architecture follows:

- Network segmentation
- Default-deny communication between zones
- Non-root containers
- Resource limits
- No unnecessary host access
- No outbound Internet access from challenge environments
- Snapshot/recreation-based recovery
- Restricted administrative access
