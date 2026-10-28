"""Local development runner. Not the production entry point.

Why this exists: the production design is a webhook (ADR-0005), but a webhook
needs a public HTTPS host, and the host checks V-2 to V-4 are still open. This
runner asks Telegram for new messages (getUpdates) so a developer can talk to a
test bot from a laptop. It uses the same router as the webhook, so behavior is
identical. Recorded as a dev-only deviation in docs/reviews/a1-design-check.md.

Run from the repo root:
    python -m src.bot.poll

getUpdates does not work while a webhook is set on the same bot. Use a test
bot from BotFather, never the shared tester bot.
"""

from __future__ import annotations

import logging
import os
import sys

from src.adapters.telegram import TelegramClient, TelegramConfigError
from src.bot.router import route_update


def load_dotenv(path: str = ".env") -> None:
    """Read KEY=value lines from .env into the environment (no extra package)."""
    if not os.path.exists(path):
        return
    with open(path, encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def main() -> int:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s %(message)s")
    log = logging.getLogger("poll")
    load_dotenv()

    try:
        client = TelegramClient()
    except TelegramConfigError as err:
        print(err, file=sys.stderr)
        return 1

    log.info("Bot started. Message your test bot in Telegram. Press Ctrl+C to stop.")
    offset = None
    try:
        while True:
            result = client.get_updates(offset)
            if not result.get("ok"):
                if result.get("error_code") == 409:
                    print("A webhook is set on this bot. Use a separate test bot.", file=sys.stderr)
                    return 1
                if result.get("error_code") == 401:
                    print("Telegram rejected the token. Check TELEGRAM_BOT_TOKEN.", file=sys.stderr)
                    return 1
                continue
            for update in result.get("result", []):
                offset = update["update_id"] + 1
                routed = route_update(update)
                if routed.chat_id is not None and routed.reply:
                    client.send_message(routed.chat_id, routed.reply)
                log.info("outcome=%s", routed.outcome)
    except KeyboardInterrupt:
        log.info("Stopped.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
