# Changelog
All notable changes to this project. Format: Keep a Changelog style; newest first.

## [Unreleased]
<!-- id: CHANG-20261026-s3-dm | owner_agent: unassigned | date: 2026-10-26 -->
### Added
- Bots can send direct messages to a Mattermost user by username and read that DM (dm_send, dm_read); a second DM reuses the same conversation, unknown usernames are refused, and DMs count against the 20 posts per minute limit.

<!-- id: CHANG-20261026-s2-post-read-channel | owner_agent: unassigned | date: 2026-10-26 -->
### Added
- Bots can post to and read channels they belong to (post_channel, read_channel); non-member channels are refused without joining, and posts are limited to 20 per minute per bot.

<!-- id: CHANG-20261026-s1-mcp-list-channels | owner_agent: unassigned | date: 2026-10-26 -->
### Added
- MCP endpoint at /mcp: Grok Bots connect with their own Mattermost bot token (Authorization: Bearer) and can list their channels; the header-echo placeholder is removed and unknown paths return 404.

