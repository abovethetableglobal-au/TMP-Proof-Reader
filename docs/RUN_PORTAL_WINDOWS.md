# Running the TMP Check portal on Windows (from the beginning)

## One-time setup
1. **Python 3.11 or newer** — python.org → Downloads. In the installer tick **"Add python.exe to PATH"**.
2. **Git** — git-scm.com → Download for Windows (default options).
3. **Get the project** (skip if you already have the folder): open PowerShell and run
   `git clone https://github.com/abovethetableglobal-au/TMP-Proof-Reader.git`
4. **Your Anthropic API key** (for the AI checks): Start menu → "Edit environment variables for your account" → New →
   Name `ANTHROPIC_API_KEY`, Value your `sk-ant-api03-…` key → OK. Close and reopen any open windows.
5. **Operator account**: in the project folder double-click **`create_operator.bat`**; enter your name, an email not
   already used in the portal, and a password.

## Every time
1. Double-click **`start_portal.bat`** in the project folder. It updates the code, checks packages and starts the portal.
2. The browser opens **http://localhost:8000/login** after a few seconds. Sign in with your operator email.
3. **Keep the black window open** — closing it stops the portal.

## If something goes wrong
| You see | Do this |
|---|---|
| Browser: "This site can't be reached" | The black window isn't running or has stopped — double-click `start_portal.bat` and read any error |
| "address already in use" | An old portal window is still open — close it, then start again |
| Signed in but no Operator menu | You're signed in as a customer — top-right menu → Sign out → sign in with the operator email |
| Any other error | Copy the last 15 lines of the black window to Claude |
