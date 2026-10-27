"""Domain-specific language for the mmbridge executable specs (layer 2).

The public interface below (method names, parameters, docstrings) is locked at CP-C with the specs.
Bodies may change freely, EXCEPT assertion steps (assert_*): eng-check flags those.
The driver runs the real bridge (FastAPI app, /mcp) against a fake Mattermost (/api/v4 stub)
that records every call. How-it-works detail lives in drivers/.
"""


class Dsl:
    """Domain: Grok Bots acting in Mattermost through the bridge."""

    def __init__(self, driver):
        self._d = driver
        self._last = None

    # --- Given: the Mattermost world -------------------------------------------------
    def given_bot(self, name="eddie"):
        """A Mattermost bot account exists with a valid token; later calls use it."""
        self._d.given_bot(name)

    def given_channel(self, team="rmlab", channel="dev", members=()):
        """A channel exists in a team; listed bots/users are members."""
        self._d.given_channel(team, channel, list(members))

    def given_channel_posts(self, team="rmlab", channel="dev", count=30):
        """The channel already contains `count` posts, oldest first."""
        self._d.given_channel_posts(team, channel, count)

    def given_user(self, username="rob"):
        """A human Mattermost user exists."""
        self._d.given_user(username)

    def given_dm_post(self, author="rob", bot="eddie", message="ping"):
        """A user wrote a message to the bot in their DM."""
        self._d.given_dm_post(author, bot, message)

    def given_no_user(self, username="nobody"):
        """No Mattermost user with this username exists."""
        self._d.given_no_user(username)

    def given_no_channel(self, team="rmlab", channel="ghost"):
        """No channel with this name exists in the team (the team itself exists)."""
        self._d.given_no_channel(team, channel)

    def given_mattermost_down(self):
        """Mattermost is unreachable from the bridge."""
        self._d.given_mattermost_down()

    # --- When: the bot uses the bridge ---------------------------------------------
    def as_bot(self, name):
        """Later calls are made by this (already given) bot, with its own credential."""
        self._d.as_bot(name)

    def list_channels(self, credential="valid"):
        """The bot asks for its channels. credential: "valid" (the bot's token), "missing"
        (no Authorization header) or "invalid" (a Bearer token Mattermost rejects)."""
        self._last = self._d.call("list_channels", {}, credential=credential)

    def post(self, channel="dev", message="build is green", team="rmlab"):
        """The bot posts a message to a channel."""
        self._last = self._d.call("post_channel", {"team": team, "channel": channel, "message": message})

    def read_channel(self, channel="dev", limit=None, team="rmlab"):
        """The bot reads recent posts of a channel (limit=None: default count)."""
        args = {"team": team, "channel": channel}
        if limit is not None:
            args["limit"] = limit
        self._last = self._d.call("read_channel", args)

    def dm_send(self, username="rob", message="hello"):
        """The bot sends a DM to a user."""
        self._last = self._d.call("dm_send", {"username": username, "message": message})

    def dm_read(self, username="rob"):
        """The bot reads its DM with a user."""
        self._last = self._d.call("dm_read", {"username": username})

    # --- Then ------------------------------------------------------------------------
    def assert_refused(self):
        """The call was refused at the bridge (HTTP 401, missing/malformed credential) and Mattermost was never called."""
        assert self._last["http_status"] == 401, self._last
        assert self._d.mattermost_calls() == [], self._d.mattermost_calls()

    def assert_channels(self, expected, team="rmlab"):
        """The returned channels are exactly `expected` (names) in `team`."""
        got = sorted((c["team"], c["name"]) for c in self._last["result"]["channels"])
        assert got == sorted((team, n) for n in expected), got

    def assert_post_visible(self, channel="dev", author="eddie", message="build is green"):
        """Mattermost holds the message in the channel, authored by the bot; a post id came back."""
        assert self._last["result"].get("post_id"), self._last
        assert (author, message) in self._d.channel_posts(channel), self._d.channel_posts(channel)

    def assert_newest_posts(self, count):
        """Exactly the `count` newest seeded posts came back (same ids and text), newest first, each with author, time and text."""
        posts = self._last["result"]["posts"]
        assert len(posts) == count, len(posts)
        assert all(p.get("author") and p.get("create_at") and "message" in p for p in posts), posts
        times = [p["create_at"] for p in posts]
        assert times == sorted(times, reverse=True), times
        expected = self._d.newest_posts(count)  # [(id, message)] newest first, from the fake world
        assert [(p["id"], p["message"]) for p in posts] == expected, (posts, expected)

    def assert_default_post_count(self):
        """The default number (20) of newest posts came back."""
        self.assert_newest_posts(20)

    def assert_dm_visible(self, username="rob", bot="eddie", message="hello"):
        """The DM between bot and user holds the message from the bot."""
        assert self._last["result"].get("post_id"), self._last
        assert (bot, message) in self._d.dm_posts(bot, username), self._d.dm_posts(bot, username)

    def assert_single_dm_conversation(self, username="rob", bot="eddie"):
        """Only one direct conversation exists between bot and user."""
        assert self._d.dm_channel_count(bot, username) == 1

    def assert_dm_contains(self, author="rob", message="ping"):
        """The returned DM posts include the message from that author."""
        posts = self._last["result"]["posts"]
        assert any(p["author"] == author and p["message"] == message for p in posts), posts

    def assert_error(self, code):
        """The tool returned an error with this code and a human message."""
        err = self._last["error"]
        assert err and err["code"] == code and err["message"], self._last

    def assert_nothing_posted_or_joined(self):
        """The bridge made no post and no join call to Mattermost."""
        writes = [c for c in self._d.mattermost_calls() if c[0] == "POST" and
                  (c[1].endswith("/posts") or "/members" in c[1])]
        assert writes == [], writes

    def assert_nothing_changed_in_mattermost(self):
        """No post, channel, DM conversation or membership was created in the Mattermost world."""
        assert self._d.world_changes() == [], self._d.world_changes()

    def assert_credential_not_exposed(self):
        """The bot's token appears nowhere in the response or the bridge logs."""
        tok = self._d.current_token()
        assert tok not in repr(self._last), "token in response"
        assert tok not in self._d.bridge_logs(), "token in logs"

    # --- Live bots (REQ-A1..A8, ADR-0010): listener -> signed wake at a receiver ----------
    # Driven by the "live" channel: real container image + fake Mattermost (REST + websocket)
    # + local wake receiver that captures and HMAC-verifies every wake. Bot set up via admin CLI.
    def given_live_bot(self, name="eddie", channels=()):
        """Bot `name` is the registered live bot (via the admin CLI), listening on the chosen
        channels (names; the bot must be a member). Listener is enabled and connected."""
        self._d.given_live_bot(name, list(channels))

    def given_member_channel(self, channel="town-square", members=(), team="rmlab"):
        """A channel exists; listed bots/users are members (no choice made by this)."""
        self._d.given_channel(team, channel, list(members))

    def given_wake_target_down(self):
        """The bot's wake receiver fails every request (HTTP 503) from now on."""
        self._d.given_wake_target_down()

    def post_in(self, channel="town-square", message="hello", as_user="rob"):
        """A Mattermost user (or bot) posts in a channel; the listener sees it live."""
        self._d.post_in(channel, message, as_user)

    def dm(self, bot="eddie", message="ping", as_user="ulrik"):
        """A user sends a direct message to the bot."""
        self._d.dm(bot, message, as_user)

    def drop_connection(self, seconds=30):
        """Mattermost drops the listener's websocket and refuses reconnects for `seconds`
        (simulated); posts made meanwhile are only reachable by catch-up after reconnect."""
        self._d.drop_connection(seconds)

    def restore_connection(self):
        """Mattermost accepts connections again; the listener reconnects on its own."""
        self._d.restore_connection()

    def send_forged_wake(self):
        """Someone posts a wake to the receiver without a valid signature."""
        self._last = self._d.send_forged_wake()

    def assert_woken_once(self, bot="eddie", channel="town-square", sender="rob", message=None):
        """Exactly one correctly signed wake for this post reached the bot's receiver, naming
        channel, sender, message text and post id (within the 10 s metric)."""
        self._d.assert_woken_once(bot, channel, sender, message)

    def assert_not_woken(self, bot="eddie", message=None):
        """No wake (for this message, or at all when message is None) reached the receiver
        within the settle time."""
        self._d.assert_not_woken(bot, message)

    def assert_forged_wake_rejected(self):
        """The receiver rejected the unsigned/forged wake (signature check failed)."""
        self._d.assert_forged_wake_rejected(self._last)

    def assert_no_token_anywhere(self, bot="eddie"):
        """The bot's Mattermost token appears in no log line, admin CLI output, or wake
        payload/header captured during the scenario."""
        self._d.assert_no_token_anywhere(bot)

    def assert_wake_retried(self, minimum=2):
        """The receiver saw at least `minimum` delivery attempts for the same delivery id."""
        self._d.assert_wake_retried(minimum)

    def assert_failed_wake_visible(self, message=None):
        """After retries are exhausted the operator sees the failed wake (admin CLI `failed`)."""
        self._d.assert_failed_wake_visible(message)
