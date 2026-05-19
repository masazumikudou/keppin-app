import requests
from config import SLACK_BOT_TOKEN, SLACK_CHANNEL_ID, APP_URL


def notify(member_id: str, date_str: str, store_name: str) -> bool:
    mention = f'<@{member_id}>' if member_id else ''
    text = (
        f'{mention} {date_str} {store_name}の欠品情報を登録しました。'
        f'確認お願いします。\n→ {APP_URL}'
    )
    resp = requests.post(
        'https://slack.com/api/chat.postMessage',
        headers={'Authorization': f'Bearer {SLACK_BOT_TOKEN}'},
        json={'channel': SLACK_CHANNEL_ID, 'text': text},
        timeout=10,
    ).json()
    return resp.get('ok', False)
