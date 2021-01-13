from slack import WebClient

from config import (
    SLACK_APP_TOKEN,
    SLACK_TARGET_CHANNEL_NAME,
    SLACK_USER_NAME,
    SLACK_USER_ICON_URI
)


def post_blocks(blocks: list):
    client = WebClient(token=SLACK_APP_TOKEN)
    client.chat_postMessage(
        channel=f'#{SLACK_TARGET_CHANNEL_NAME}',
        blocks=blocks,
        username=SLACK_USER_NAME,
        icon_url=SLACK_USER_ICON_URI
    )
