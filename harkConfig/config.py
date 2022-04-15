from harkConfig import env

ERROR = 0  # -> Show ERROR only
INFO = 1  # -> Show ERROR and INFO
DEBUG = 2  # -> Show ERROR, INFO and DEBUG
VERBOSE = 3  # -> Show ERROR, INFO, DEBUG AND VERBOSE
LOG_LEVEL = DEBUG

LATEST = 0  # 0 == LATEST
NLP_VERSION = 1

""" 
-> Global Config
"""
BOT_NAME = "HarkServer"
MASTER_PATH = env.get_env("MASTER_BOT_PATH")

# ------------------------------------------> SET CLIENT INFO <------------------------------------------------------ #

# 2. TWITTER CLIENT
twitter_consumer_key = env.get_env("TWITTER_CONSUMER_KEY")
twitter_consumer_secret = env.get_env("TWITTER_CONSUMER_SECRET")
twitter_access_token = env.get_env("TWITTER_ACCESS_TOKEN")
twitter_access_token_secret = env.get_env("TWITTER_ACCESS_TOKEN_SECRET")

# -> SMS NOTIFICATIONS <- #
# TextBelt: https://textbelt.com/ #
sms_key = "3b11437549708345091de04ca87cba6129cdfb493NIMu5rAxH3fm9Ie8EEvYqrZw"
sms_url = 'https://textbelt.com/text'
sms_number = env.get_env("CELL_NUMBER")

