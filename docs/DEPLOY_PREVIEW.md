# Deploying the pilot preview (A-53)

Hosted on Fly.io, Sydney (`syd`). One small machine (1 GB) plus a 1 GB disk for the database and uploads.
Estimated cost: about US$7–10/month for hosting (machine stops when idle), plus AI usage (about US$6 per 81-page check), capped at US$150/month (`ai.monthly_cap_usd`).

Data note: the portal and stored documents stay in Sydney; each AI check sends the TMP to the Anthropic API (outside Australia). Historical or anonymised TMPs only (A-18, A-53).

## One-time setup (Owner, on your PC, PowerShell)
1. Create a Fly.io account (fly.io) and add a payment card. **This is the spend you approved.**
2. Install the Fly CLI:
   `iwr https://fly.io/install.ps1 -useb | iex`
3. Sign in: `fly auth login`
4. In the project folder: `fly launch --no-deploy --copy-config --name tmpcheck-preview --region syd`
   (If the name is taken, choose another and update `app` in fly.toml.)
5. Create the disk: `fly volumes create tmpcheck_data --region syd --size 1`
6. Set the secrets (values never go in the repo):
   - `fly secrets set TMPCHECK_SECRET=<long random string>`
   - `fly secrets set TMPCHECK_INVITES="<INVITE-CODE>|Way to Go Traffic Management|10"`
   - `fly secrets set ANTHROPIC_API_KEY=<sk-ant-api03-...>`
   - `fly secrets set TMPCHECK_AI_PASSES=A,B,C,D`
7. Deploy: `fly deploy`
8. Open: `fly open` → the site is `https://tmpcheck-preview.fly.dev`.

## Invite Tara
Send her: `https://tmpcheck-preview.fly.dev/signup?invite=<INVITE-CODE>` (draft email: `docs/comms/EMAIL_Tara_preview_invite_DRAFT.md`).
She creates her profile (name, email, password, accreditation level, number, expiry). Her organisation gets the invite's test credits once.

## Day to day
- Logs: `fly logs`
- Update after `git pull`: `fly deploy`
- Turn the AI off: `fly secrets unset TMPCHECK_AI_PASSES`
- Withdraw an invite: change `TMPCHECK_INVITES` (existing profiles keep working).
- Stop everything: `fly scale count 0`
