#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 17 15:25:01 2018

@author: junjshi
"""

import aiohttp
import asyncio
import time
from aiohttp import web
import base64
from cryptography import fernet
from aiohttp_session import setup, get_session, session_middleware
from aiohttp_session.cookie_storage import EncryptedCookieStorage
import os


async def getRequest():
    chunk_size = 256
    async with aiohttp.ClientSession() as session:
        async with session.get('http://httpbin.org/get') as resp:
            print(resp.status)
            print(await resp.text())
        async with session.get('https://api.github.com/events', verify_ssl=False) as resp:
            while True:
                chunk = await resp.content.read(chunk_size)
                if not chunk:
                    break
                #fd.write(chunk)
                print(chunk)
                #print(await resp.content.read(10))

async def postRequest():
    async with aiohttp.ClientSession() as session:
        async with session.post('http://httpbin.org/post', data=b'data') as resp:
            print(resp.status)
            print(await resp.text())


loop = asyncio.get_event_loop()
loop.run_until_complete(getRequest())
loop.run_until_complete(postRequest())


routes = web.RouteTableDef()

@routes.get('/')
async def hello(request):
    return web.Response(text="Hello, world")

@routes.get(r'/{name:\d+}')
async def variable_handler(request):
    return web.Response(
            text='Hello,{}'.format(request.match_info['name']))

@routes.get('/json')
async def handler_json(request):
    data = {'some': 'data'}
    return web.json_response(data)

@routes.get('/session')
async def handler_session(request):
    session = await get_session(request)
    last_visit = session['last_visit'] if 'last_visit' in session else time.time()
    session['last_visit'] = last_visit
    text = 'Last visit:{}'.format(last_visit)
    return web.Response(text = text)

@routes.post('/login', name='login')
async def do_login(request):
    data = await request.post()
    login = data['login']
    password = data['password']
    print(login, ':' , password)
    return web.Response(text='logged in!')

@routes.post('/mp3')
async def store_mp3_handler(request):

    reader = await request.multipart()

    # /!\ Don't forget to validate your inputs /!\

    # reader.next() will `yield` the fields of your form

    field = await reader.next()
    assert field.name == 'name'
    name = await field.read(decode=True)

    field = await reader.next()
    assert field.name == 'mp3'
    filename = field.filename
    # You cannot rely on Content-Length if transfer is chunked.
    size = 0
    with open(os.path.join('/spool/yarrr-media/mp3/', filename), 'wb') as f:
        while True:
            chunk = await field.read_chunk()  # 8192 bytes by default.
            if not chunk:
                break
            size += len(chunk)
            f.write(chunk)

    return web.Response(text='{} sized of {} successfully stored'
                             ''.format(filename, size))


@routes.get('/ws')
async def websocket_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    
    async for msg in ws:
        if msg.type == aiohttp.WSMsgType.TEXT:
            if msg.data == 'close':
                await ws.close()
            else:
                await ws.send_str(msg.data + '/answer')
        elif msg.type == aiohttp.WSMsgType.ERROR:
            print('ws connection closed with exception %s' % ws.exception())
    print('websocket connection closed')
    return ws


@routes.get('/redirect')
async def handler_redirect(request):
    location = request.app.router['login'].url_for()
    raise web.HTTPFound(location=location)
    
    
    
async def make_app():
    app = web.Application()
    
    fernet_key = fernet.Fernet.generate_key()
    secret_key = base64.urlsafe_b64decode(fernet_key)
    setup(app, EncryptedCookieStorage(secret_key))
    
    app.add_routes(routes)
    return app


web.run_app(make_app(),port=9000)




