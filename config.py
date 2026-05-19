import os

SLACK_BOT_TOKEN  = os.environ.get('SLACK_BOT_TOKEN')
SLACK_CHANNEL_ID = os.environ.get('SLACK_CHANNEL_ID', 'C0ALR5FUN9F')
PHP_ENDPOINT     = os.environ.get('PHP_ENDPOINT')
APP_URL          = os.environ.get('APP_URL', 'http://localhost:8090')
STAFF_MASTER_PATH = os.environ.get(
    'STAFF_MASTER_PATH',
    r'C:\Users\fieldwork\Desktop\発注君CC用\担当者マスター.xlsx'
)

# 出荷時の連携先
TN_APP_URL       = os.environ.get('TN_APP_URL', '')   # TNアプリのCloud Run URL
OS2_PHP_ENDPOINT = os.environ.get(
    'OS2_PHP_ENDPOINT',
    'https://tool.field-work.co.jp/kudo_www/api/os2_orders.php'
)
