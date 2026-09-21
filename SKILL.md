---
name: rednote-cli
description: Use rednote-cli with RedNote browser cookies for Xiaohongshu (Little Red Book, 小红书) operations — searching notes, reading content, browsing users, liking, collecting, commenting, following, and posting.
author: shuenrui
version: "0.6.4"
tags:
  - xiaohongshu
  - rednote
  - redbook
  - 小红书
  - social-media
  - cli
---

# rednote-cli — Xiaohongshu CLI Tool

**Binary:** `rednote`
**Credentials:** `rednote.com` browser cookies by default, or Xiaohongshu browser-assisted QR login (`--qrcode`)

## Setup

```bash
# Install (requires Python 3.10+)
uv tool install git+https://github.com/shuenrui/rednote-cli.git
# Or: pipx install git+https://github.com/shuenrui/rednote-cli.git

# Upgrade to latest (recommended to avoid API errors)
uv tool install --force git+https://github.com/shuenrui/rednote-cli.git
# Or: pipx install --force git+https://github.com/shuenrui/rednote-cli.git
```

## Authentication

**IMPORTANT FOR AGENTS**: Before executing ANY rednote command, check if credentials exist first. Do NOT assume cookies are configured.

### Step 0: Check if already authenticated

```bash
rednote status --yaml >/dev/null && echo "AUTH_OK" || echo "AUTH_NEEDED"
```

If `AUTH_OK`, skip to [Command Reference](#command-reference).
If `AUTH_NEEDED`, proceed to Step 1. Prefer `--qrcode` when browser cookie extraction is unavailable but launching a browser is acceptable.

### Step 1: Guide user to authenticate

Ensure user is logged into rednote.com in any browser supported by [browser_cookie3](https://github.com/borisbabic/browser_cookie3). Supported browsers: Chrome, Arc, Edge, Firefox, Safari, Brave, Chromium, Opera, Opera GX, Vivaldi, LibreWolf, Lynx, w3m. Then:

```bash
rednote login                              # auto-detect browser with valid cookies
rednote login --cookie-source arc          # specify browser explicitly
rednote login --cookie-domain xiaohongshu  # optional upstream cookie source
rednote login --qrcode                     # Xiaohongshu QR login with terminal QR output
```

Verify with:

```bash
rednote status
rednote whoami
```

### Step 2: Handle common auth issues

| Symptom | Agent action |
|---------|-------------|
| `NoCookieError: No 'a1' cookie found` | Guide user to log in to rednote.com in a browser |
| `NeedVerifyError: Captcha required` | Ask user to open browser, complete captcha, then retry |
| `IpBlockedError: IP blocked` | Suggest switching network (hotspot/VPN) |
| `SessionExpiredError` | Run `rednote login` to refresh cookies |

## Agent Defaults

All machine-readable output uses the envelope documented in [SCHEMA.md](./SCHEMA.md).
Payloads live under `.data`.

- Non-TTY stdout → auto YAML
- `--json` / `--yaml` → explicit format
- `OUTPUT=json` env → global override
- `OUTPUT=rich` env → force human output

## Command Reference

### Reading

| Command | Description | Example |
|---------|-------------|---------|
| `rednote search <keyword>` | Search notes | `rednote search "美食" --sort popular --type video` |
| `rednote read <id_or_url_or_index>` | Read a note by ID, URL, or short index | `rednote read 1` / `rednote read "https://...?xsec_token=xxx"` |
| `rednote comments <id_or_url_or_index>` | Get comments by ID, URL, or short index | `rednote comments 1` / `rednote comments "https://...?xsec_token=..."` |
| `rednote comments <id_or_url> --all` | Get ALL comments (auto-paginate) | `rednote comments "<url>" --all --json` |
| `rednote sub-comments <note_id> <comment_id>` | Get replies to comment | `rednote sub-comments abc 123` |
| `rednote user <user_id>` | View user profile | `rednote user 5f2e123` |
| `rednote user-posts <user_id>` | List user's notes | `rednote user-posts 5f2e123 --cursor ""` |
| `rednote feed` | Browse recommendation feed | `rednote feed --yaml` |
| `rednote hot` | Browse trending notes | `rednote hot -c food` |
| `rednote topics <keyword>` | Search topics/hashtags | `rednote topics "旅行"` |
| `rednote search-user <keyword>` | Search users | `rednote search-user "摄影"` |
| `rednote my-notes` | List own published notes | `rednote my-notes --page 0` |
| `rednote notifications` | View notifications | `rednote notifications --type likes` |
| `rednote unread` | Show unread counts | `rednote unread --json` |

### Interactions (Write)

| Command | Description | Example |
|---------|-------------|---------|
| `rednote like <id_or_url_or_index>` | Like a note | `rednote like 1` / `rednote like abc123` |
| `rednote like <id_or_url_or_index> --undo` | Unlike a note | `rednote like 1 --undo` |
| `rednote favorite <id_or_url_or_index>` | Bookmark a note | `rednote favorite 1` |
| `rednote unfavorite <id_or_url_or_index>` | Remove bookmark | `rednote unfavorite 1` |
| `rednote comment <id_or_url_or_index> -c "text"` | Post a comment | `rednote comment 1 -c "好看！"` |
| `rednote reply <id_or_url_or_index> --comment-id ID -c "text"` | Reply to comment | `rednote reply 1 --comment-id 456 -c "谢谢"` |
| `rednote delete-comment <note_id> <comment_id>` | Delete own comment | `rednote delete-comment abc 123 -y` |

### Social

| Command | Description | Example |
|---------|-------------|---------|
| `rednote follow <user_id>` | Follow a user | `rednote follow 5f2e123` |
| `rednote unfollow <user_id>` | Unfollow a user | `rednote unfollow 5f2e123` |
| `rednote favorites [user_id]` | List bookmarked notes (defaults to self) | `rednote favorites --json` |

### Creator

| Command | Description | Example |
|---------|-------------|---------|
| `rednote post --title "..." --body "..." --images img.png` | Publish a note | `rednote post --title "Test" --body "Hello"` |
| `rednote delete <id_or_url>` | Delete own note | `rednote delete abc123 -y` |

### Account

| Command | Description |
|---------|-------------|
| `rednote login` | Extract cookies from browser (auto-detect) |
| `rednote login --qrcode` | Browser-assisted QR login — terminal QR output, browser completes login |
| `rednote status` | Check authentication status |
| `rednote logout` | Clear cached cookies |
| `rednote whoami` | Show current user profile |

## Agent Workflow Examples

### Search → Read → Like pipeline

```bash
NOTE_ID=$(rednote search "美食推荐" --json | jq -r '.data.items[0].id')
rednote read "$NOTE_ID" --json | jq '.data'
rednote like "$NOTE_ID"
```

### Browse trending food notes

```bash
rednote hot -c food --json | jq '.data.items[:5] | .[].note_card | {title, likes: .interact_info.liked_count}'
```

### Get user info then follow

```bash
rednote user 5f2e123 --json | jq '.data.basic_info | {nickname, user_id}'
rednote follow 5f2e123
```

### Check notifications

```bash
rednote unread --json | jq '.data'
rednote notifications --type mentions --json | jq '.data.message_list[:5]'
```

### Analyze all comments on a note

```bash
# Fetch ALL comments and analyze themes
rednote comments "$NOTE_URL" --all --json | jq '.data.comments | length'
# Count questions
rednote comments "$NOTE_URL" --all --json | jq '[.data.comments[] | select(.content | test("[\uff1f?]"))] | length'
```

### Daily reading workflow

```bash
# Browse recommendation feed
rednote feed --yaml

# Interactive short-index workflow
rednote search "旅行"
rednote read 1
rednote comments 1
rednote like 1
rednote favorite 1
rednote comment 1 -c "收藏了"

# Browse trending by category
rednote hot -c food --yaml
rednote hot -c travel --yaml
```

### QR code login

```bash
# When browser cookie extraction is not available
rednote login --qrcode
# → Launches a browser-assisted login flow
# → Renders QR in terminal using Unicode half-blocks
# → Scan with Xiaohongshu app → confirm → export cookies
```

### URL to insights pipeline

```bash
# User pastes a URL → read + all comments
rednote read "https://www.xiaohongshu.com/explore/xxx?xsec_token=yyy" --json
rednote comments "https://www.xiaohongshu.com/explore/xxx?xsec_token=yyy" --all --json
```

## Hot Categories

Available for `rednote hot -c <category>`:
`fashion`, `food`, `cosmetics`, `movie`, `career`, `love`, `home`, `gaming`, `travel`, `fitness`

## Error Codes

Structured error codes returned in the `error.code` field:
- `not_authenticated` — cookies expired or missing
- `verification_required` — captcha/verification needed
- `ip_blocked` — IP rate limited
- `signature_error` — request signing failed
- `api_error` — upstream API error
- `unsupported_operation` — operation not available

## Limitations

- **No video download** — cannot download note images/videos
- **No DMs** — cannot access private messages
- **No live streaming** — live features not supported
- **No following/followers list** — XHS web API doesn't expose these endpoints
- **Single account** — one set of cookies at a time
- **Rate limited** — built-in Gaussian jitter delay (~1-1.5s) between requests; aggressive usage may trigger captchas or IP blocks

## Anti-Detection Notes for Agents

- **Do NOT parallelize requests** — the built-in rate-limit delay exists for account safety
- **Captcha recovery**: if `NeedVerifyError` occurs, the client auto-cools-down with increasing delays (5s→10s→20s→30s). Ask the user to complete captcha in browser before retrying
- **Batch operations**: when doing bulk work (e.g., reading many notes), add `time.sleep()` between CLI calls
- **Session stability**: all requests in a session share a consistent browser fingerprint. Restarting the CLI creates a new fingerprint session

## Safety Notes

- Do not ask users to share raw cookie values in chat logs.
- Prefer local browser cookie extraction over manual secret copy/paste.
- If auth fails, ask the user to re-login via `rednote login`.
- Agent should treat cookie values as secrets (do not echo to stdout unnecessarily).
- Built-in rate-limit delay protects accounts; do not bypass it.
