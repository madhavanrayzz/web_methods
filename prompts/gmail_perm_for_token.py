#!/usr/bin/env python3

import importlib.util
import json
import os
import subprocess
import sys
import threading
import urllib.parse
from http.server import BaseHTTPRequestHandler, HTTPServer


# ============================================================
# CONFIGURATION
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CREDENTIALS_FILE = os.path.join(BASE_DIR, "credentials.json")
TOKEN_FILE = os.path.join(BASE_DIR, "token.json")

HOST = "localhost"
PORT = 8765
REDIRECT_URI = f"http://{HOST}:{PORT}/"

SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.send",
]


# ============================================================
# DEPENDENCY INSTALLER
# ============================================================

REQUIRED_PACKAGES = {
    "google.auth": "google-auth",
    "google_auth_oauthlib": "google-auth-oauthlib",
    "googleapiclient": "google-api-python-client",
    "httplib2": "httplib2",
    "requests": "requests",
}


def module_exists(module_name):
    try:
        return importlib.util.find_spec(module_name) is not None
    except (ModuleNotFoundError, ValueError, AttributeError):
        return False


def install_missing_dependencies():
    missing = []

    for module, package in REQUIRED_PACKAGES.items():
        if not module_exists(module):
            missing.append(package)

    if not missing:
        print("[+] All required dependencies are installed.")
        return

    print()
    print("[*] Missing dependencies detected:")

    for package in missing:
        print(f"    - {package}")

    print()
    print("[*] Installing missing dependencies...")
    print()

    try:
        subprocess.check_call(
            [
                sys.executable,
                "-m",
                "pip",
                "install",
                *missing,
            ]
        )
    except subprocess.CalledProcessError:
        print()
        print("[!] Dependency installation failed.")
        print()
        print("Try running:")
        print()
        print(
            f"{sys.executable} -m pip install "
            + " ".join(missing)
        )
        sys.exit(1)

    print()
    print("[+] Dependencies installed successfully.")
    print()


install_missing_dependencies()


# ============================================================
# GOOGLE IMPORTS
# ============================================================

try:
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import Flow
except ImportError as e:
    print(f"[!] Google library import failed: {e}")
    print()
    print("Try running the script again.")
    sys.exit(1)


# ============================================================
# OAUTH CALLBACK SERVER
# ============================================================

class OAuthCallbackHandler(BaseHTTPRequestHandler):

    def do_GET(self):

        parsed = urllib.parse.urlparse(self.path)

        if parsed.path != "/":
            self.send_error(404)
            return

        params = urllib.parse.parse_qs(parsed.query)

        # Google returned an OAuth error
        if "error" in params:

            error = params["error"][0]

            self.server.oauth_error = error

            self.send_response(400)
            self.send_header("Content-Type", "text/html")
            self.end_headers()

            self.wfile.write(
                b"""
                <!DOCTYPE html>
                <html>
                <head>
                    <title>OAuth Failed</title>
                </head>
                <body>
                    <h2>Authorization failed.</h2>
                    <p>You can close this tab.</p>
                </body>
                </html>
                """
            )

            return

        # OAuth authorization code
        code = params.get("code", [None])[0]

        # OAuth state
        state = params.get("state", [None])[0]

        self.server.oauth_code = code
        self.server.oauth_state = state

        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.end_headers()

        self.wfile.write(
            b"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>OAuth Successful</title>
            </head>
            <body>
                <h2>Authorization successful!</h2>
                <p>You can close this tab.</p>
            </body>
            </html>
            """
        )

    def log_message(self, format, *args):
        # Don't print HTTP request details.
        pass


# ============================================================
# CHECK EXISTING TOKEN
# ============================================================

def check_existing_token():

    if not os.path.exists(TOKEN_FILE):
        return False

    print("[*] Existing token.json found.")

    try:

        credentials = Credentials.from_authorized_user_file(
            TOKEN_FILE,
            SCOPES,
        )

        # Already valid
        if credentials.valid:

            print("[+] Existing token is valid.")
            print(f"[+] Token file: {TOKEN_FILE}")

            return True

        # Expired access token but refresh token exists
        if credentials.expired and credentials.refresh_token:

            print("[*] Access token expired.")
            print("[*] Refreshing using stored refresh token...")

            credentials.refresh(Request())

            with open(TOKEN_FILE, "w") as f:
                f.write(credentials.to_json())

            os.chmod(TOKEN_FILE, 0o600)

            print("[+] Token refreshed successfully.")
            print(f"[+] Token file: {TOKEN_FILE}")

            return True

        print("[!] Existing token cannot be refreshed.")
        print("[*] Starting a new OAuth authorization.")

        return False

    except Exception as e:

        print(f"[!] Could not load existing token: {e}")
        print("[*] Starting a new OAuth authorization.")

        return False


# ============================================================
# MAIN OAUTH FLOW
# ============================================================

def main():

    print()
    print("=" * 70)
    print("GMAIL OAUTH TOKEN SETUP")
    print("=" * 70)
    print()

    # --------------------------------------------------------
    # Check credentials.json
    # --------------------------------------------------------

    if not os.path.exists(CREDENTIALS_FILE):

        print("[!] credentials.json was not found.")
        print()
        print("Expected location:")
        print(CREDENTIALS_FILE)
        print()

        sys.exit(1)

    print(f"[+] Credentials found:")
    print(f"    {CREDENTIALS_FILE}")
    print()

    # --------------------------------------------------------
    # Check existing token
    # --------------------------------------------------------

    if check_existing_token():

        print()
        print("[+] Nothing else is required.")
        print()

        return

    # --------------------------------------------------------
    # Create OAuth flow
    # --------------------------------------------------------

    print("[*] Creating OAuth flow...")

    try:

        flow = Flow.from_client_secrets_file(
            CREDENTIALS_FILE,
            scopes=SCOPES,
        )

    except Exception as e:

        print()
        print("[!] Could not load credentials.json")
        print(f"[!] Error: {e}")
        print()

        sys.exit(1)

    # IMPORTANT:
    # This must match the callback server below.

    flow.redirect_uri = REDIRECT_URI

    # --------------------------------------------------------
    # Generate authorization URL
    # --------------------------------------------------------

    try:

        authorization_url, state = flow.authorization_url(
            access_type="offline",
            prompt="consent",
            include_granted_scopes="true",
        )

    except Exception as e:

        print()
        print("[!] Could not generate OAuth URL.")
        print(f"[!] Error: {e}")
        print()

        sys.exit(1)

    # --------------------------------------------------------
    # Start callback server
    # --------------------------------------------------------

    try:

        server = HTTPServer(
            (HOST, PORT),
            OAuthCallbackHandler,
        )

    except OSError as e:

        print()
        print(f"[!] Could not start callback server on port {PORT}.")
        print(f"[!] Error: {e}")
        print()
        print("Check whether another application is using this port.")
        print()

        sys.exit(1)

    server.oauth_code = None
    server.oauth_state = None
    server.oauth_error = None

    # Wait for exactly one callback request.
    callback_thread = threading.Thread(
        target=server.handle_request,
        daemon=True,
    )

    callback_thread.start()

    # --------------------------------------------------------
    # Display authorization URL
    # --------------------------------------------------------

    print()
    print("=" * 70)
    print("OPEN THIS URL IN CHROME")
    print("=" * 70)
    print()
    print(authorization_url)
    print()
    print("=" * 70)
    print(f"CALLBACK: {REDIRECT_URI}")
    print("=" * 70)
    print()
    print("[*] Waiting for Google OAuth callback...")
    print()

    # --------------------------------------------------------
    # Wait for Chrome callback
    # --------------------------------------------------------

    callback_thread.join()

    server.server_close()

    # --------------------------------------------------------
    # Check OAuth errors
    # --------------------------------------------------------

    if server.oauth_error:

        print()
        print("[!] Google OAuth returned an error:")
        print(f"    {server.oauth_error}")
        print()

        sys.exit(1)

    # --------------------------------------------------------
    # Check authorization code
    # --------------------------------------------------------

    if not server.oauth_code:

        print()
        print("[!] No authorization code received.")
        print()

        sys.exit(1)

    # --------------------------------------------------------
    # Verify OAuth state
    # --------------------------------------------------------

    if server.oauth_state != state:

        print()
        print("[!] OAuth state verification failed.")
        print("[!] Refusing to exchange the authorization code.")
        print()

        sys.exit(1)

    print("[+] OAuth callback received.")
    print("[+] State verified.")
    print("[*] Exchanging authorization code...")
    print()

    # --------------------------------------------------------
    # Exchange code for tokens
    # --------------------------------------------------------

    try:

        flow.fetch_token(
            code=server.oauth_code
        )

    except Exception as e:

        print()
        print("[!] Token exchange failed.")
        print(f"[!] Error: {e}")
        print()

        sys.exit(1)

    credentials = flow.credentials

    # --------------------------------------------------------
    # Verify refresh token
    # --------------------------------------------------------

    if not credentials.refresh_token:

        print()
        print("[!] Google did not return a refresh token.")
        print("[!] The token cannot be stored for long-term reuse.")
        print()

        sys.exit(1)

    # --------------------------------------------------------
    # Save token.json
    # --------------------------------------------------------

    try:

        with open(TOKEN_FILE, "w") as f:
            f.write(credentials.to_json())

        # Owner read/write only
        os.chmod(TOKEN_FILE, 0o600)

    except Exception as e:

        print()
        print("[!] Failed to save token.json.")
        print(f"[!] Error: {e}")
        print()

        sys.exit(1)

    # --------------------------------------------------------
    # Success
    # --------------------------------------------------------

    print("=" * 70)
    print("OAUTH SUCCESSFUL")
    print("=" * 70)
    print()
    print(f"Token saved to:")
    print(TOKEN_FILE)
    print()
    print("Refresh token is stored for future authentication.")
    print("The token itself was not printed to the terminal.")
    print()
    print("=" * 70)
    print()


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()
