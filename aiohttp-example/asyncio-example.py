#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 17 15:50:44 2018

@author: junjshi
"""

import time
import asyncio


## 定义一个协程
now = lambda: time.time()
async def do_some_work(x):
    print('waiting:', x)

start = now()

# 这里是一个协程对象，这个时候do_some_work函数并没有执行
coroutine = do_some_work(2)
print(coroutine)

#  创建一个事件loop
loop = asyncio.get_event_loop()

# 将协程加入到事件循环loop
loop.run_until_complete(coroutine)

print("Time:", now()-start)


## 创建一个task
async def do_some_work2(x):
    print("Do some work2:", x)
    
start = now()
coroutine = do_some_work2(2)
loop = asyncio.get_event_loop()
task = loop.create_task(coroutine)
print(task)
loop.run_until_complete(task)
print(task)
print("Time:" , now()-start)


## 绑定回调
async def do_some_work3(x):
    print("waiting:",x)
    return "Done after {}s".format(x)

def callback(future):
    print('callback:', future.result())
    
'''Don't know why it throws exception:cannot reuse already awaited coroutine
start = now()
courine = do_some_work3(2)
loop = asyncio.get_event_loop()
task = asyncio.ensure_future(coroutine)
print(task)
task.add_done_callback(callback)
print(task)
loop.run_until_complete(task)
print("Time:" , now()-start)'''

# 阻塞和await
async def do_some_work4(x):
    print("waiting:",x)
    # await 后面就是调用耗时的操作
    await asyncio.sleep(x)
    return "Done after {}s".format(x)


start = now()

coroutine = do_some_work4(2)
loop = asyncio.get_event_loop()
task = asyncio.ensure_future(coroutine)
loop.run_until_complete(task)

print("Task ret:", task.result())
print("Time:", now() - start)

#并发和并行
coroutine1 = do_some_work4(1)
coroutine2 = do_some_work4(2)
coroutine3 = do_some_work4(4)

tasks = [
    asyncio.ensure_future(coroutine1),
    asyncio.ensure_future(coroutine2),
    asyncio.ensure_future(coroutine3)
]

loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.wait(tasks))

for task in tasks:
    print("Task ret:",task.result())

print("Time:",now()-start)

# 协程嵌套

async def main():
    coroutine1 = do_some_work(1)
    coroutine2 = do_some_work(2)
    coroutine3 = do_some_work(4)
    tasks = [
        asyncio.ensure_future(coroutine1),
        asyncio.ensure_future(coroutine2),
        asyncio.ensure_future(coroutine3)
    ]

    #dones, pendings = await asyncio.wait(tasks)
    #for task in dones:
    #    print("Task ret:", task.result())
    return await asyncio.wait(tasks)
    #results = await asyncio.gather(*tasks)
    #for result in results:
    #    print("Task ret:",result)


start = now()

loop = asyncio.get_event_loop()
done, pending = loop.run_until_complete(main())
for tasks in done:
    print("Task ret:",task.result())
print("Time:", now()-start)