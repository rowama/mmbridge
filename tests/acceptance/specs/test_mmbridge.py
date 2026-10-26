"""Executable specs (layer 1) for mmbridge, from the design's Acceptance examples. Locked at CP-C."""
import pytest

pytestmark = pytest.mark.channels("mcp")


@pytest.mark.req("REQ-1")
def test_posts_appear_as_the_connecting_bot(app):
    app.given_bot("eddie")
    app.given_channel("rmlab", "dev", members=["eddie"])
    app.post("dev", "build is green")
    app.assert_post_visible("dev", author="eddie", message="build is green")


@pytest.mark.req("REQ-1")
def test_caller_without_credential_is_refused(app):
    app.given_bot("eddie")
    app.list_channels(credential="missing")
    app.assert_refused()


@pytest.mark.req("REQ-1")
def test_invalid_credential_is_rejected_and_not_exposed(app):
    app.given_bot("eddie")
    app.list_channels(credential="invalid")
    app.assert_error("unauthorized")
    app.assert_credential_not_exposed()


@pytest.mark.req("REQ-1")
@pytest.mark.req("REQ-2")
def test_each_caller_sees_only_its_own_identity(app):
    app.given_bot("eddie")
    app.given_bot("ada")
    app.given_channel("rmlab", "dev", members=["eddie"])
    app.given_channel("rmlab", "ops", members=["ada"])
    app.as_bot("eddie")
    app.list_channels()
    app.assert_channels(["dev"], team="rmlab")
    app.as_bot("ada")
    app.list_channels()
    app.assert_channels(["ops"], team="rmlab")
    app.post("ops", "ada here")
    app.assert_post_visible("ops", author="ada", message="ada here")
    app.as_bot("eddie")
    app.list_channels()
    app.assert_channels(["dev"], team="rmlab")


@pytest.mark.req("REQ-2")
def test_lists_only_joined_channels(app):
    app.given_bot("eddie")
    app.given_channel("rmlab", "town-square", members=["eddie"])
    app.given_channel("rmlab", "dev", members=["eddie"])
    app.given_channel("rmlab", "finance", members=[])
    app.list_channels()
    app.assert_channels(["town-square", "dev"], team="rmlab")


@pytest.mark.req("REQ-3")
def test_post_to_member_channel(app):
    app.given_bot("eddie")
    app.given_channel("rmlab", "dev", members=["eddie"])
    app.post("dev", "build is green")
    app.assert_post_visible("dev", author="eddie", message="build is green")


@pytest.mark.req("REQ-4")
def test_read_requested_count(app):
    app.given_bot("eddie")
    app.given_channel("rmlab", "dev", members=["eddie"])
    app.given_channel_posts("rmlab", "dev", 30)
    app.read_channel("dev", limit=5)
    app.assert_newest_posts(5)


@pytest.mark.req("REQ-4")
def test_read_default_count(app):
    app.given_bot("eddie")
    app.given_channel("rmlab", "dev", members=["eddie"])
    app.given_channel_posts("rmlab", "dev", 30)
    app.read_channel("dev")
    app.assert_default_post_count()


@pytest.mark.req("REQ-5")
def test_first_dm_opens_conversation(app):
    app.given_bot("eddie")
    app.given_user("rob")
    app.dm_send("rob", "hello")
    app.assert_dm_visible("rob", bot="eddie", message="hello")
    app.assert_single_dm_conversation("rob", bot="eddie")


@pytest.mark.req("REQ-5")
def test_second_dm_lands_in_same_conversation(app):
    app.given_bot("eddie")
    app.given_user("rob")
    app.dm_send("rob", "hello")
    app.dm_send("rob", "again")
    app.assert_dm_visible("rob", bot="eddie", message="again")
    app.assert_single_dm_conversation("rob", bot="eddie")


@pytest.mark.req("REQ-6")
def test_read_dm(app):
    app.given_bot("eddie")
    app.given_user("rob")
    app.given_dm_post(author="rob", bot="eddie", message="ping")
    app.dm_read("rob")
    app.assert_dm_contains(author="rob", message="ping")


@pytest.mark.req("REQ-7")
def test_non_member_channel_is_refused_without_join(app):
    app.given_bot("eddie")
    app.given_channel("rmlab", "finance", members=[])
    app.post("finance", "hi")
    app.assert_error("not_member")
    app.assert_nothing_posted_or_joined()


@pytest.mark.req("REQ-7")
def test_read_of_non_member_channel_is_refused(app):
    app.given_bot("eddie")
    app.given_channel("rmlab", "finance", members=[])
    app.given_channel_posts("rmlab", "finance", 3)
    app.read_channel("finance")
    app.assert_error("not_member")
    app.assert_nothing_changed_in_mattermost()


@pytest.mark.req("REQ-7")
def test_unknown_channel_is_refused(app):
    app.given_bot("eddie")
    app.given_no_channel("rmlab", "ghost")
    app.post("ghost", "hi")
    app.assert_error("unknown_channel")
    app.assert_nothing_changed_in_mattermost()
    app.read_channel("ghost")
    app.assert_error("unknown_channel")
    app.assert_nothing_changed_in_mattermost()


@pytest.mark.req("REQ-7")
def test_dm_to_unknown_user(app):
    app.given_bot("eddie")
    app.given_no_user("nobody")
    app.dm_send("nobody", "hi")
    app.assert_error("unknown_user")
    app.assert_nothing_posted_or_joined()
    app.assert_nothing_changed_in_mattermost()


@pytest.mark.req("REQ-8")
def test_mattermost_down_is_clear_and_leaks_nothing(app):
    app.given_bot("eddie")
    app.given_channel("rmlab", "dev", members=["eddie"])
    app.given_mattermost_down()
    app.post("dev", "build is green")
    app.assert_error("mattermost_unavailable")
    app.assert_credential_not_exposed()
