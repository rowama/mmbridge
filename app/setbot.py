"""Friendly owner wrapper for `python -m app.admin set-bot --name NAME` (Rob 2026-10-30; run as `bin/set-bot NAME`
in the mmbridge container terminal).

Prompts for the bot's Mattermost token (hidden, never echoed: Mattermost shows it once under Integrations > Bot
Accounts; if lost, create a new token there), the wake URL (default http://relay:8080/wake/NAME, the in-stack
relay) and the HMAC-SHA256 wake secret (Enter = generate a new one; or paste the existing one, hidden). Then runs
the real admin set-bot with token + secret on stdin and prints the matching relay env line
`RELAY_BOT_<NAME>_HMAC_SECRET=<secret>` for Coolify. The Fernet store key (MMB_STORE_KEY) is a one-time Coolify env
and is not touched here.
"""
import getpass
import io
import secrets
import sys

from app import admin, store

DEFAULT_WAKE = "http://relay:8080/wake/%s"


def relay_env_name(name: str) -> str:
    return "RELAY_BOT_%s" % name.upper().replace("-", "_")


def main(argv=None, ask=input, ask_hidden=getpass.getpass, out=None, transport=None) -> int:
    out = out or sys.stdout
    argv = sys.argv[1:] if argv is None else argv
    if len(argv) != 1 or argv[0] in ("-h", "--help"):
        print("usage: bin/set-bot NAME   (NAME: lowercase letters, digits, '-'; same name as the relay env block)",
              file=out)
        return 2
    name = argv[0]
    if not store.valid_name(name):
        print("error: invalid_argument: name must match %s" % store.NAME_RE.pattern, file=out)
        return 1
    print("Registering bot %r on mmbridge." % name, file=out)
    token = ask_hidden("Mattermost bot token for %s (hidden; shown once in Mattermost > Integrations > Bot Accounts,"
                       " if lost create a new token there): " % name).strip()
    if not token:
        print("error: invalid_argument: no token entered", file=out)
        return 1
    url = ask("Wake URL [%s]: " % (DEFAULT_WAKE % name)).strip() or DEFAULT_WAKE % name
    secret = ask_hidden("Wake secret (Enter = generate a new one; or paste the existing secret, hidden): ").strip()
    secret = secret or secrets.token_urlsafe(32)
    buf = io.StringIO()
    rc = admin.main(["set-bot", "--name", name, "--token-stdin", "--wake-secret-stdin", "--wake-url", url],
                    stdin=io.StringIO("%s\n%s\n" % (token, secret)), stdout=buf, transport=transport)
    print(buf.getvalue().rstrip(), file=out)
    if rc != 0:
        return rc
    env = relay_env_name(name)
    print("\nPut this line in the relay service env in Coolify (shown once here; same secret on both sides):",
          file=out)
    print("%s_HMAC_SECRET=%s" % (env, secret), file=out)
    print("The relay also needs %s_ROUTINE_URL and %s_ROUTINE_KEY from that bot's Grok routine; redeploy the relay"
          " after editing its env. mmbridge picks the bot up within 30 s, no redeploy." % (env, env), file=out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
