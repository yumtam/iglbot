test = True

DISCORD_TOKEN_FILENAME = "tokens/discord_token.txt"
YUNITE_TOKEN_FILENAME = "tokens/yunite_token_test.txt" if test else "tokens/yunite_token.txt"
GSHEET_TOKEN_FILENAME = "tokens/brave-iterator-281404-7ac178f6299b.json"

CONTEST_NAME = "FORTNITE IGL CASH CUP"
CONTEST_CAPACITY = 64
CONTEST_FORMAT = "Tournament"
CONTEST_CHANNEL_ANNOUNCE_NAME = "1" if test else "it-chat"
CONTEST_CHANNEL_REPORT_NAME = "rep" if test else "it-chat"
CONTEST_CHANNEL_LOG_NAME = "rep" if test else "it-chat"
YUNITE_REGISTER_CHANNEL_NAME = "1" if test else "verificar"

CONTEST_TIMEOUT = 15*60

TIMEZONE = -4

GSHEET_URL = "https://docs.google.com/spreadsheets/d/1wGgqfiQT4ME0sLfnW-H5edu4v-A8J6-x4VbSQRbwNdQ/edit#gid=1457072026"
GSHEET_CONTEST_FORMAT_SHEET_NAME = "format"
GSHEET_CONTEST_WRITE_SHEET_NAME = "match"
GSHEET_CONTEST_REGISTER_SHEET_NAME = "register"
GSHEET_CONTEST_REGISTER_LOGGING_SHEET_NAME = "register_log"

ADMIN_ROLE_NAME = "admin"
PLAYER_ROLE_NAME = "player"
EMBED_COLOR = 0xf3bb76

GUILD_NAME = "bot_test" if test else "IGL CASH CUP"
GUILD_ID = 721584767409324062 if test else 717128617737453628

YUNITE_DELAY = 0.25