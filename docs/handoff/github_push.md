# GitHub Publication — Status and Required Owner Action

**Status: BLOCKED on authentication.** Everything else is complete and committed
locally.

Verified on 2026-10-29 (Asia/Hong_Kong) in this environment:

| Check | Result |
|---|---|
| `git --version` | `2.53.0` — present |
| `git config --show-origin --get user.name` | unset **globally**; now set **repo-local** |
| `command -v gh` | **was missing**; official CLI `2.103.3` installed to `~/.local/bin/gh` |
| `gh auth status` | `You are not logged into any GitHub hosts. To log in, run: gh auth login` |
| GitHub account `Steven-ZYC` | **exists** (public API; numeric id `60809224`) |
| Target repository | **existence cannot be determined unauthenticated** — `git ls-remote` falls through to a username prompt, which GitHub also does for a private repo or a nonexistent one |
| `git push -u origin main` | `fatal: could not read Username for 'https://github.com'` |
| SSH keys | none (`~/.ssh` contains only an empty `authorized_keys`) |
| Credential helpers / `GH_TOKEN` | none |
| `sudo apt-get install` | unavailable — `sudo` requires interactive authentication |

## Local state that is ready

```text
branch      main (renamed from master)
remote      origin -> https://github.com/Steven-ZYC/INT4096-ML-Financial-Forecasting.git
identity    ZHANG Yancheng <60809224+Steven-ZYC@users.noreply.github.com>  (repo-local)
history     clean; no placeholder email remains; nothing has ever been pushed
working tree clean; all 20 run manifests resolve to an existing commit
```

The commit email is the GitHub **no-reply** form derived from the account's public
numeric id (`60809224`), not an invented address. No private email is exposed. If
you would rather use a different verified address, change it *before* the first
push — afterwards it means rewriting published history.

## One-time owner action (choose one)

### Option A — GitHub CLI device flow (recommended, no token pasting)

```bash
gh auth login          # choose: GitHub.com -> HTTPS -> login with a browser
gh auth status         # should print: Logged in to github.com as Steven-ZYC
```

`gh auth login` prints a one-time code and opens a browser. Enter the code there.
**Do not paste a password, PAT, recovery code or private key into this chat.**

Then create the private repository and push:

```bash
cd /home/steven/int4096-int

# Create ONLY if it does not exist. Private, and explicitly owned by Steven-ZYC.
gh repo view Steven-ZYC/INT4096-ML-Financial-Forecasting >/dev/null 2>&1 \
  || gh repo create Steven-ZYC/INT4096-ML-Financial-Forecasting \
       --private --source=. --remote=origin --description \
       "INT4096: reproducible model/preprocessing comparison on AAPL and BTC (coursework)"

git push -u origin main
gh repo view --web
```

If the repository already exists with a README, do **not** force push. Reconcile
instead:

```bash
git fetch origin
git rebase origin/main      # or: git merge --allow-unrelated-histories origin/main
git push -u origin main
```

### Option B — SSH

```bash
ssh-keygen -t ed25519 -C "60809224+Steven-ZYC@users.noreply.github.com"
cat ~/.ssh/id_ed25519.pub      # add this as an authentication key on GitHub
ssh -T git@github.com          # expect: Hi Steven-ZYC! You've successfully authenticated
git remote set-url origin git@github.com:Steven-ZYC/INT4096-ML-Financial-Forecasting.git
git push -u origin main
```

### Option C — a token in the environment (least preferred)

Create a **fine-grained** PAT scoped to this one repository with `Contents: write`,
then `export GH_TOKEN=<token>` in the shell only. Never commit it, never put it in
the remote URL, and revoke it after the push. The repository's `.gitignore` already
excludes `.env` and key files.

## Verification after the push

```bash
git ls-remote origin | head            # branch SHAs on the remote
git rev-parse HEAD                     # must match refs/heads/main above
gh api repos/Steven-ZYC/INT4096-ML-Financial-Forecasting \
  --jq '{private: .private, default_branch: .default_branch, size: .size}'
```

Expected: `private: true`, `default_branch: "main"`, and a HEAD SHA equal to the
local one. **A successful `git push` is not proof of visibility** — confirm the
private flag, because publishing coursework publicly is a separate decision.

## What is deliberately not in the repository

- No credentials, tokens, SSH keys, `.env` files, or student IDs.
- No official course specification PDF (not confirmed to be redistributable);
  `docs/course/README.md` records what must be verified instead.
- No member names in the PDF title block; they live in
  `docs/management/responsibilities.md` and are inserted in the Moodle copy.
- No raw provider payloads (large, regenerable, gitignored); the normalised
  snapshots and their SHA-256 manifests **are** committed because they pin every
  reported number.

## Reminder: GitHub is not the submission

The Moodle upload on **28 November 2026, 23:59 HKT** remains the submission of
record. GitHub is an additional reproducibility archive. Nobody should mark the
Moodle submission complete on the basis of a successful push.
