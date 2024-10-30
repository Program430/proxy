from aiohttp import web
import json
import asyncio
import aiohttp

#Useless asyncio =)
async def request_to_aim_server(url, headers, json):
     async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=json) as response:
            print("Status:", response.status)
            result = await response.json()
            return result


async def handle_post(request):
    try:
        data = await request.json()
    except Exception as e:
        return web.Response(status=400)

    task = asyncio.create_task(request_to_aim_server(data['url'], data['headers'], data['data']))
    result = await task

    return web.json_response(result)


app = web.Application()
app.router.add_post('/proxy', handle_post)

if __name__ == '__main__':
    web.run_app(app, host='127.0.0.1', port=5000)
