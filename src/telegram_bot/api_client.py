from aiohttp import ClientSession


class APIClient:
    def __init__(self, api_url: str):
        self.url = api_url

    async def get_qr_link(self, phone_number: str) -> str:
        async with ClientSession() as session:
            response = await session.post(
                f'{self.url}/login',
                data=phone_number,
            )
        return (await response.json()).get('qr_link_url')

    async def get_login_status(self, phone_number: str) -> str:
        async with ClientSession() as session:
            response = await session.get(
                f'{self.url}/check/login?phone={phone_number}',
            )
        return (await response.json()).get('status')

    async def send_message(
        self,
        phone_number: str,
        username: str,
        message: str,
    ) -> int:
        async with ClientSession() as session:
            response = await session.post(
                f'{self.url}/messages',
                json={
                    'from_phone': phone_number,
                    'username': username,
                    'message_text': message,
                },
            )
        return response.status

    async def get_messages(
        self,
        phone_number: str,
        username: str,
    ) -> dict:
        async with ClientSession() as session:
            response = await session.get(
                f'{self.url}/messages?phone={phone_number}&uname={username}',
            )
        return (await response.json()).get('messages')
