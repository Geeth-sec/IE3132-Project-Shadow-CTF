# PS-05 to PS-06 Connection Guide

## Environment
- Platform: UTM on macOS
- Server: Ubuntu Server 24.04 ARM64
- Client: Kali Linux
- Network: Isolated UTM Host-Only network

## PS-06 Connection
- Server IP: 10.10.4.60
- SSH Port: 2222
- Username: shadowanalyst
- Password: Supplied separately to authorised participants

## Kali Network Route
For the tested UTM lab, with Ubuntu reachable
at 192.168.128.2, run:

sudo ip route replace 10.10.4.60/32 via 192.168.128.2 dev eth0

## Connect
ssh -p 2222 shadowanalyst@10.10.4.60

## Verification
- SSH port 2222 reachable
- shadowanalyst login successful
- Ubuntu server address persists after reboot
- Root maintenance challenge tested
- Clean reset verified

## Notes
- The Kali route must be reapplied after reboot.
- DHCP addresses may vary between environments.
- Only run one copy of the server VM at a time.
- Do not include challenge flags in player instructions.
