"""Executable specs (layer 1) for Live bots one-bot v1 (REQ-A1, A2, A3 own-post, A4, A7, A8).
From docs/design/2026-10-26-live-bots.md Acceptance examples. Locked at CP-C. ADR-0010.
Run: pytest tests/acceptance --channel live  (skipped on other channels)."""
import pytest

pytestmark = pytest.mark.channels("live")


@pytest.mark.req("REQ-A1")
def test_mention_in_chosen_channel_wakes_bot_once(app):
    app.given_member_channel("town-square", members=["eddie", "rob"])
    app.given_live_bot("eddie", channels=["town-square"])
    app.post_in("town-square", "@eddie what is on deck?", as_user="rob")
    app.assert_woken_once("eddie", channel="town-square", sender="rob", message="@eddie what is on deck?")


@pytest.mark.req("REQ-A1")
def test_post_without_mention_in_chosen_channel_also_wakes_bot(app):
    app.given_member_channel("town-square", members=["eddie", "rob"])
    app.given_live_bot("eddie", channels=["town-square"])
    app.post_in("town-square", "eddie is great", as_user="rob")
    app.assert_woken_once("eddie", channel="town-square", sender="rob", message="eddie is great")


@pytest.mark.req("REQ-A1")
def test_post_in_member_channel_not_chosen_does_not_wake(app):
    app.given_member_channel("town-square", members=["eddie", "rob"])
    app.given_member_channel("off-topic", members=["eddie", "rob"])
    app.given_live_bot("eddie", channels=["town-square"])
    app.post_in("off-topic", "anyone around?", as_user="rob")
    app.assert_not_woken("eddie", message="anyone around?")


@pytest.mark.req("REQ-A2")
def test_dm_to_bot_wakes_bot_once(app):
    app.given_live_bot("eddie", channels=[])
    app.dm("eddie", "ping", as_user="ulrik")
    app.assert_woken_once("eddie", channel=None, sender="ulrik", message="ping")


@pytest.mark.req("REQ-A3")
def test_bots_own_post_never_wakes_itself(app):
    app.given_member_channel("town-square", members=["eddie", "rob"])
    app.given_live_bot("eddie", channels=["town-square"])
    app.post_in("town-square", "@eddie note to self", as_user="eddie")
    app.assert_not_woken("eddie")


@pytest.mark.req("REQ-A4")
def test_post_during_connection_drop_wakes_exactly_once_after_reconnect(app):
    app.given_member_channel("town-square", members=["eddie", "rob"])
    app.given_live_bot("eddie", channels=["town-square"])
    app.drop_connection(30)
    app.post_in("town-square", "@eddie are you there?", as_user="rob")
    app.restore_connection()
    app.assert_woken_once("eddie", channel="town-square", sender="rob", message="@eddie are you there?")


@pytest.mark.req("REQ-A7")
def test_forged_wake_is_rejected(app):
    app.given_live_bot("eddie", channels=[])
    app.send_forged_wake()
    app.assert_forged_wake_rejected()


@pytest.mark.req("REQ-A7")
def test_bot_token_never_appears_in_logs_output_or_wakes(app):
    app.given_member_channel("town-square", members=["eddie", "rob"])
    app.given_live_bot("eddie", channels=["town-square"])
    app.post_in("town-square", "hello eddie", as_user="rob")
    app.dm("eddie", "ping", as_user="ulrik")
    app.assert_woken_once("eddie", channel="town-square", sender="rob", message="hello eddie")
    app.assert_no_token_anywhere("eddie")


@pytest.mark.req("REQ-A8")
def test_failed_wake_is_retried_then_visible_to_operator(app):
    app.given_member_channel("town-square", members=["eddie", "rob"])
    app.given_live_bot("eddie", channels=["town-square"])
    app.given_wake_target_down()
    app.post_in("town-square", "@eddie status?", as_user="rob")
    app.assert_wake_retried(minimum=2)
    app.assert_failed_wake_visible(message="@eddie status?")
