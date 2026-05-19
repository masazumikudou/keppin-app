_STAFF = {
    '沖田': 'U04U91LMK3R',
    '平井': 'U04V31XF9L2',
    '田村': 'U04VD6VE8SC',
    '田中': 'U04V24ZU8TB',
    '福本': 'U087XEMUNRF',
    '柴崎': 'U04UA6WL5P1',
    '濱本': 'U06RYEJTUUE',
    '壷井': 'U082VJZU0TF',
    '鍋谷': 'U04U8U0PPBR',
    '根岸': 'U04U91KK9F1',
    '高森': 'U04UA5DFLH5',
    '浅野': 'U04UJ3A1EES',
    '高橋': 'U04RRU4670X',
    '黒崎': 'U04UGSP9WRL',
}


def load_staff_by_name() -> dict:
    return {name: {'name': name, 'slack_member_id': mid} for name, mid in _STAFF.items()}
