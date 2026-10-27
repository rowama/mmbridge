"""Live-bots protocol driver (layer 3, ADR-0010). STUB until slices 3-5 build it.

Target: start the real container image (temp /data, MMB_STORE_KEY, LIVE_BOTS_ENABLED=true,
MATTERMOST_URL -> fake MM with REST + websocket, wake_url -> local HMAC-verifying receiver),
configure the bot with the real admin CLI. Drivers are not locked; edit freely.
"""


class LiveDriver:
    def __getattr__(self, name):
        def _stub(*a, **k):
            raise NotImplementedError("live driver step %r not built yet (slices 3-5)" % name)
        return _stub

    def close(self):
        pass
