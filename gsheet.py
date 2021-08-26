import settings as s
import gspread_asyncio
from oauth2client.service_account import ServiceAccountCredentials

def get_creds():
    return ServiceAccountCredentials.from_json_keyfile_name(
        s.GSHEET_TOKEN_FILENAME,
        [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive",
            "https://www.googleapis.com/auth/spreadsheets",
        ],
    )

agcm = gspread_asyncio.AsyncioGspreadClientManager(get_creds)

async def get_worksheet(url, name):
    agc = await agcm.authorize()
    sh = await agc.open_by_url(url)
    ws = await sh.worksheet(name)
    return ws

