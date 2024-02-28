import aiohttp
import os
from aiohttp import web

PROXY_URL = 'https://api.openai.com/v1/'
TOKEN = os.getenv("OPENAI_API_KEY")

async def handle_request(request):
    async with aiohttp.ClientSession() as session:
        headers = {'Authorization':  f'Bearer {TOKEN}'}
        try:
            async with session.request(
                    request.method,
                    PROXY_URL + request.path_qs,
                    headers=headers,
                    data=await request.read()) as response:
                response_data = await response.read()
                return aiohttp.web.Response(
                    body=response_data,
                    status=response.status,
                    headers=dict(response.headers))
        except Exception as exc:
            return aiohttp.web.Response(
                    body=str(exc),
                    status=502,
                    headers=dict(response.headers))
            


app = aiohttp.web.Application()
app.router.add_route('*', '/{path:.*}', handle_request)

web.run_app(app)