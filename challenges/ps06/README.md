
cat > README.md << 'README_EOF'
# PS-06 — Shadow Core Server (Linux Privilege Escalation)

**Domain:** Linux / System Security
**Difficulty:** Hard
**Author:** Zoysa E.R.L (Member 3)

## Scenario

The Shadow Core server is the final stop in the Project Shadow investigation.
Participants connect as a synthetic investigator account (shadowanalyst)
and must identify and exploit a misconfigured privileged maintenance
workflow to recover the final case file and flag.

## Vulnerability

- /opt/shadow/maintenance/backup.sh is owned by root:shadowmaint
  with mode 775 - readable, writable and executable by the shadowmaint
  group.
- The investigator account shadowanalyst belongs to shadowmaint,
  so it can edit the script's contents, even though it cannot
  change the file's ownership or permission bits (those require root).
- Root's crontab executes this script every minute:
  * * * * * /opt/shadow/maintenance/backup.sh
- Any participant who overwrites the script's contents gets that
  payload executed as root on the next cron tick - a classic
  group-writable, root-run cron job privilege escalation.

## Environment

- Ubuntu Server 24.04 LTS, host-only network (no internet access,
  verified with ping 8.8.8.8 failing).
- Low-privileged account: shadowanalyst (groups: shadowanalyst,
  shadowmaint).
- Root-protected flag file: /opt/shadow/private/final_case.txt
  (mode 600, owned by root:root).
- Drop location for exfiltrated data: /var/tmp/shadow-drop/.

## Solve path

1. SSH in as shadowanalyst.
2. Enumerate /opt/shadow/maintenance/backup.sh - notice it's
   group-writable and that shadowanalyst is in the owning group.
3. Overwrite the script to copy the protected flag file into a
   world-readable location:
   cp /opt/shadow/private/final_case.txt /var/tmp/shadow-drop/final_case.txt
   chmod 644 /var/tmp/shadow-drop/final_case.txt
4. Wait up to 60 seconds for root's cron job to execute the modified
   script.
5. Read the leaked file:
   cat /var/tmp/shadow-drop/final_case.txt
6. The file contains the six-event incident timeline and the final
   flag in the form CyberTrace{Final_<token>}.

## Solver script

ps06_solver.py automates the full solve path over SSH using
paramiko:

pip install paramiko --break-system-packages
python3 ps06_solver.py --host <shadow-core-ip> --user shadowanalyst

It connects, enumerates the script, overwrites it, waits for cron,
reads back the flag, prints it, and restores the original harmless
script content so the box is left in a clean, re-solvable state.

## Reset and recovery

A clean baseline clone of the VM is kept separately (not committed -
disk images are excluded via .gitignore). To reset between attempts:

1. Power off the working VM.
2. Discard it and re-clone from the clean baseline image.
3. Boot the fresh clone - backup.sh is back to its harmless
   content and /var/tmp/shadow-drop/ is empty.

This was tested end-to-end: dirtied then reset via clone then
re-exploited successfully, confirming the reset mechanism works.

## Security controls

- VM has no internet route (host-only network only).
- shadowanalyst cannot reach CTFd administration, the database, or
  other participants.
- Only the intended group-write misconfiguration is exploitable;
  no other services are exposed.
README_EOF

