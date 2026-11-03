# Source Code

| Field | Value |
|-------|-------|
| Owner | Adiya (Architecture & Development Lead) |
| Backup | Khumoyun |
| Last updated | 2026-10-26 |

Python 3.10 or later. Layout follows [Architecture](../docs/architecture/architecture.md), Section 3.

| Folder | Layer | Rule |
|--------|-------|------|
| `src/core/` | Core: parser, lookup, day total, use cases | Imports nothing from `src/bot/`, `src/adapters/`, Flask, `sqlite3` or `urllib` |
| `src/bot/` | Interface: webhook, router, local runner | Turns Telegram updates into core calls |
| `src/adapters/` | Adapters: Telegram (and later FDC, storage) | The only code that reads secrets or calls outside services |

## Run the Bot on Your Computer

1. Create a **test** bot with @BotFather in Telegram and copy its token. Do not use the shared tester bot.
2. From the repo root:

   ```
   python -m venv .venv
   source .venv/bin/activate        # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   cp .env.example .env             # Windows: copy .env.example .env
   ```

3. Open `.env` and paste the token after `TELEGRAM_BOT_TOKEN=`. Never commit `.env`.
4. Start the bot: `python -m src.bot.poll`
5. In Telegram, send `/start` to your test bot. It replies with the welcome message. Press Ctrl+C to stop.

`poll.py` is for local development only. The production entry point is the webhook in `src/bot/web.py` (ADR-0005), which is deployed only after host checks V-2 to V-4 pass.

## Run the Tests

```
python -m unittest discover -s tests -t .
```

Tests use Python's built-in `unittest`, so they need nothing beyond `requirements.txt`.

## Change Log

| Date | Change | By |
|------|--------|----|
| 2026-10-26 | Created with the bot skeleton (#48) | Adiya |
