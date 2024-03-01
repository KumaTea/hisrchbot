from common.info import debug_mode


if debug_mode:
    pwd = 'D:/GitHub/hisrchbot'
else:
    pwd = '/home/kuma/bots/hisrchbot'

msg_data_dir = f'{pwd}/data/msg'

GROUP_MSG_LIMIT = 1000
TRUSTED_GROUP_MSG_LIMIT = 10000

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
unknown_message = "I can't understand your message or command. You may try /help."

USER_AGENT = (
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
    'AppleWebKit/537.36 (KHTML, like Gecko) '
    'Chrome/122.0.0.0 '
    'Safari/537.36'
)
