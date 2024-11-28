from requests import get


async def check_bot_token(token) -> list:
    response = get(f'https://api.telegram.org/bot{token}/getMe')

    if response.status_code == 200:
        return [True,response.json()['result']['first_name']]
    else:
        return [False,False]