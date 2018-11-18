#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 17 13:08:52 2018

@author: junjshi
"""

import unittest
import orm
from models import User,Blog,Comment
import logging
logging.basicConfig(level=logging.INFO)

import asyncio

loop = asyncio.get_event_loop()


#class TestModels(unittest.TestCase):
async def test_user_insert():
    logging.info('create pool;')
    await orm.create_pool(loop, user='www-data',password='www-data',db='awesome')

    logging.info('creat new table: users')
    u = User(name='Test', email='test@example.com', passwd='1234', image='about:blank')
    await u.save()

'''if __name__ == '__main__':
    #logging.basicConfig(filename='/Users/junjshi/test.log', level=logging.INFO)
    unittest.main()'''
   


# 执行coroutine
loop.run_until_complete(test_user_insert())
#loop.close()