from common.info import debug_mode


if debug_mode:
    pwd = 'D:/GitHub/hisrchbot'
else:
    pwd = '/home/kuma/bots/hisrchbot'

msg_data_dir = f'{pwd}/data/msg'

GROUP_MSG_LIMIT = 1000
TRUSTED_GROUP_MSG_LIMIT = 10000

MAX_MSG_LEN = 200
TRUSTED_GROUP_MAX_MSG_LEN = 1000

MAX_RESULT_LEN = 16

INDEX_INTERVAL = 60 * 60  # 1 hour
STALE_CHAT_TIME = 60 * 60 * 24 * 30  # 30 days

url_regex = r'https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|' \
            r'www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|' \
            r'https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|' \
            r'www\.[a-zA-Z0-9]+\.[^\s]{2,}'

start_message = (
    'Thank you for using @hisrchbot!\n'
    'You may see commands sending "/help".'
)
help_message = (
    '/start: wake me up\n'
    '/help: display this message\n'
)

enter_group_zh = (
    '欢迎使用 @hisrchbot!\n'
    '本 bot 每小时索引一次数据，请不要着急搜索。'
    '\n'
    '会记录的消息：正常文本，媒体备注\n'
    '不记录的消息：用户的 bot 命令，代码，小作文，全域封禁及大会员消息\n'
    '无法记录的消息：bot 发言，无文字消息，非常规文本 (如投票)\n'
)

unknown_message = "I can't understand your message or command. You may try /help."

USER_AGENT = (
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
    'AppleWebKit/537.36 (KHTML, like Gecko) '
    'Chrome/122.0.0.0 '
    'Safari/537.36'
)

TWITTER_USER_AGENT = (
    # 'Twitterbot/1.0'
    'TelegramBot (like TwitterBot)'
)

valid_commands = {'/chat', '/smart'}
