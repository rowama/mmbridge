"""Executable specs (layer 1) for increment B: Grok Bot webhook wake, round-trip reply, multi-bot
(REQ-B1..B8). From docs/design/2026-10-28-grok-webhook-multibot.md Acceptance examples. Locked at CP-C.
ADR-0016: real mmbridge + real wake relay, fake Grok routine (checks Bearer, replies via the real MCP
bridge), fake Mattermost with several bot users.
Run: pytest tests/acceptance --channel live  (skipped on other channels)."""
import pytest

pytestmark = pytest.mark.channels("live")


# --- REQ-B1: a post wakes the Grok Bot routine (B-s1) ---------------------------------------
@pytest.mark.req("REQ-B1")
def test_post_in_member_channel_starts_grok_routine_once(app):
    app.given_member_channel("town-square", members=["eddie", "rob"])
    app.register_bot("eddie", wake="grok")
    app.post_in("town-square", "what is on deck?", as_user="rob")
    app.assert_routine_started_once("eddie", channel="town-square", sender="rob", message="what is on deck?")


@pytest.mark.req("REQ-B1")
def test_dm_to_bot_starts_grok_routine_once(app):
    app.register_bot("eddie", wake="grok")
    app.dm("eddie", "ping", as_user="ulrik")
    app.assert_routine_started_once("eddie", channel=None, sender="ulrik", message="ping")


# --- REQ-B2: forged, tampered, replayed wakes never start the routine; no secrets leak ------
# Behaviour only: no additional routine run. Relay reason codes (bad_sig/stale/duplicate) are
# asserted in tests/unit/test_relay.py, not here (plan review #6).
@pytest.mark.req("REQ-B2")
def test_wake_not_produced_by_mmbridge_does_not_start_routine(app):
    app.register_bot("eddie", wake="grok")
    app.forge_wake("eddie")
    app.assert_routine_not_started("eddie")


@pytest.mark.req("REQ-B2")
def test_altered_wake_does_not_start_routine(app):
    app.given_member_channel("town-square", members=["eddie", "rob"])
    app.register_bot("eddie", wake="grok")
    app.post_in("town-square", "deploy at 5", as_user="rob")
    app.assert_routine_started_once("eddie", channel="town-square", sender="rob", message="deploy at 5")
    app.tamper_wake("eddie", message="deploy now")
    app.assert_routine_not_started("eddie", message="deploy now")


@pytest.mark.req("REQ-B2")
def test_wake_replayed_ten_minutes_later_does_not_start_routine_again(app):
    app.given_member_channel("town-square", members=["eddie", "rob"])
    app.register_bot("eddie", wake="grok")
    app.post_in("town-square", "status?", as_user="rob")
    app.assert_routine_started_once("eddie", channel="town-square", sender="rob", message="status?")
    app.replay_last_wake("eddie", after_seconds=600)
    app.assert_routine_started_once("eddie", channel="town-square", sender="rob", message="status?")


@pytest.mark.req("REQ-B2")
def test_wake_replayed_within_window_does_not_start_routine_again(app):
    app.given_member_channel("town-square", members=["eddie", "rob"])
    app.register_bot("eddie", wake="grok")
    app.post_in("town-square", "status?", as_user="rob")
    app.assert_routine_started_once("eddie", channel="town-square", sender="rob", message="status?")
    app.replay_last_wake("eddie", after_seconds=5)
    app.assert_routine_started_once("eddie", channel="town-square", sender="rob", message="status?")


@pytest.mark.req("REQ-B2")
def test_no_token_secret_or_routine_key_in_logs_output_or_wakes(app):
    app.given_member_channel("town-square", members=["eddie", "rob"])
    app.register_bot("eddie", wake="grok")
    app.post_in("town-square", "hello", as_user="rob")
    app.dm("eddie", "ping", as_user="ulrik")
    app.forge_wake("eddie")
    app.assert_routine_started_once("eddie", channel=None, sender="ulrik", message="ping")
    app.assert_no_secret_anywhere("eddie")


# --- REQ-B3: delivery failures retry, recover once, or show one failed wake ------------------
@pytest.mark.req("REQ-B3")
def test_routine_recovering_before_retries_run_out_is_started_exactly_once(app):
    app.given_member_channel("town-square", members=["eddie", "rob"])
    app.register_bot("eddie", wake="grok")
    app.grok_routine_down("eddie")
    app.post_in("town-square", "anyone there?", as_user="rob")
    app.assert_wake_retried(minimum=2)
    app.grok_routine_up("eddie")
    app.assert_routine_started_once("eddie", channel="town-square", sender="rob", message="anyone there?")


@pytest.mark.req("REQ-B3")
def test_routine_down_for_good_shows_one_failed_wake(app):
    app.given_member_channel("town-square", members=["eddie", "rob"])
    app.register_bot("eddie", wake="grok")
    app.grok_routine_down("eddie")
    app.post_in("town-square", "anyone there?", as_user="rob")
    app.assert_failed_wake_visible(message="anyone there?")
    app.assert_routine_not_started("eddie", message="anyone there?")


@pytest.mark.req("REQ-B3")
def test_relay_down_then_up_starts_routine_exactly_once(app):
    app.given_member_channel("town-square", members=["eddie", "rob"])
    app.register_bot("eddie", wake="grok")
    app.relay_down()
    app.post_in("town-square", "ping relay", as_user="rob")
    app.assert_wake_retried(minimum=2)
    app.relay_up()
    app.assert_routine_started_once("eddie", channel="town-square", sender="rob", message="ping relay")


# --- REQ-B4: switching wake target without redeploy; generic signed still works -------------
@pytest.mark.req("REQ-B4")
def test_switching_bot_from_signed_webhook_to_grok_applies_without_redeploy(app):
    app.given_member_channel("town-square", members=["eddie", "rob"])
    app.register_bot("eddie", wake="signed")
    app.post_in("town-square", "before switch", as_user="rob")
    app.assert_woken_once("eddie", channel="town-square", sender="rob", message="before switch")
    app.switch_wake_target("eddie", wake="grok")
    app.post_in("town-square", "after switch", as_user="rob")
    app.assert_routine_started_once("eddie", channel="town-square", sender="rob", message="after switch")
    app.assert_not_woken("eddie", message="after switch")


@pytest.mark.req("REQ-B4")
def test_bot_on_generic_signed_webhook_keeps_receiving_signed_wakes(app):
    app.given_member_channel("town-square", members=["eddie", "test", "rob"])
    app.register_bot("eddie", wake="grok")
    app.register_bot("test", wake="signed")
    app.post_in("town-square", "hello both", as_user="rob")
    app.assert_woken_once("test", channel="town-square", sender="rob", message="hello both")
    app.assert_routine_started_once("eddie", channel="town-square", sender="rob", message="hello both")


# --- REQ-B5: round-trip reply in channel / thread / DM, no self-wake (B-s2) -----------------
@pytest.mark.req("REQ-B5")
def test_bot_answer_appears_in_channel_and_does_not_wake_it_again(app):
    app.given_member_channel("town-square", members=["eddie", "rob"])
    app.register_bot("eddie", wake="grok")
    app.given_routine_answers("eddie", "all green")
    app.post_in("town-square", "@eddie status?", as_user="rob")
    app.assert_replied("eddie", where="town-square", text="all green")
    app.assert_routine_started_once("eddie", channel="town-square", sender="rob", message="@eddie status?")
    app.assert_routine_not_started("eddie", message="all green")


@pytest.mark.req("REQ-B5")
def test_bot_answer_to_thread_reply_lands_in_that_thread(app):
    app.given_member_channel("town-square", members=["eddie", "rob"])
    app.register_bot("eddie", wake="grok")
    app.given_routine_answers("eddie", "on it")
    app.post_in("town-square", "nightly report", as_user="eddie")
    app.reply_in_thread("town-square", to_message="nightly report", message="why red?", as_user="rob")
    app.assert_replied("eddie", where="town-square", text="on it", thread="nightly report")


@pytest.mark.req("REQ-B5")
def test_bot_answer_to_dm_appears_in_that_dm(app):
    app.register_bot("eddie", wake="grok")
    app.given_routine_answers("eddie", "hello Rob")
    app.dm("eddie", "hi", as_user="rob")
    app.assert_replied("eddie", where="dm:rob", text="hello Rob")
    app.assert_routine_not_started("eddie", message="hello Rob")


# --- REQ-B6: registry of several bots, routing by membership (B-s3) -------------------------
@pytest.mark.req("REQ-B6")
def test_post_in_channel_only_one_bot_is_in_wakes_only_that_bot(app):
    app.given_member_channel("town-square", members=["eddie", "grok", "rob"])
    app.given_member_channel("dev", members=["grok", "rob"])
    app.register_bot("eddie", wake="grok")
    app.register_bot("grok", wake="grok")
    app.post_in("dev", "build broke", as_user="rob")
    app.assert_routine_started_once("grok", channel="dev", sender="rob", message="build broke")
    app.assert_routine_not_started("eddie", message="build broke")


@pytest.mark.req("REQ-B6")
def test_post_in_shared_channel_wakes_each_bot_once(app):
    app.given_member_channel("town-square", members=["eddie", "grok", "rob"])
    app.register_bot("eddie", wake="grok")
    app.register_bot("grok", wake="grok")
    app.post_in("town-square", "standup", as_user="rob")
    app.assert_routine_started_once("eddie", channel="town-square", sender="rob", message="standup")
    app.assert_routine_started_once("grok", channel="town-square", sender="rob", message="standup")


@pytest.mark.req("REQ-B6")
def test_dm_to_one_bot_wakes_only_that_bot(app):
    app.register_bot("eddie", wake="grok")
    app.register_bot("grok", wake="grok")
    app.dm("grok", "just you", as_user="rob")
    app.assert_routine_started_once("grok", channel=None, sender="rob", message="just you")
    app.assert_routine_not_started("eddie", message="just you")


# --- REQ-B7: posts by any registered bot wake nobody ----------------------------------------
@pytest.mark.req("REQ-B7")
def test_post_by_a_registered_bot_wakes_no_bot(app):
    app.given_member_channel("town-square", members=["eddie", "grok", "rob"])
    app.register_bot("eddie", wake="grok")
    app.register_bot("grok", wake="grok")
    app.post_in("town-square", "@grok hi", as_user="eddie")
    app.assert_routine_not_started("grok", message="@grok hi")
    app.assert_routine_not_started("eddie", message="@grok hi")


# --- REQ-B8: one failing bot does not stop the others ---------------------------------------
@pytest.mark.req("REQ-B8")
def test_revoked_token_of_one_bot_leaves_other_bots_working_and_marks_it_failing(app):
    app.given_member_channel("town-square", members=["eddie", "grok", "rob"])
    app.register_bot("eddie", wake="grok")
    app.register_bot("grok", wake="grok")
    app.revoke_token("grok")
    app.post_in("town-square", "who is alive?", as_user="rob")
    app.assert_routine_started_once("eddie", channel="town-square", sender="rob", message="who is alive?")
    app.assert_bot_failing("grok")


@pytest.mark.req("REQ-B8")
def test_one_bot_routine_down_leaves_other_bot_waking_and_shows_its_failed_wake(app):
    app.given_member_channel("town-square", members=["eddie", "grok", "rob"])
    app.register_bot("eddie", wake="grok")
    app.register_bot("grok", wake="grok")
    app.grok_routine_down("grok")
    app.post_in("town-square", "who is up?", as_user="rob")
    app.assert_routine_started_once("eddie", channel="town-square", sender="rob", message="who is up?")
    app.assert_failed_wake_visible_for_bot("grok", message="who is up?")
    app.assert_routine_not_started("grok", message="who is up?")
