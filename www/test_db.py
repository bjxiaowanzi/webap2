#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 上面的文件头可以确保这些写的中文识别起来也没什么问题

from models import User, Blog, Comment

from transwarp import db

db.create_engine(user='www-data', password='www-data', database='blog')

u = User(name='Test_Name', email='test@example.com', password='1234567890', image='about:blank')
u.insert()
print 'new user id:', u.id

#u1 = User.find_first('where email=?', 'test@example.com')
#print 'find user\'s name:', u1.name
#u1.delete()

#u2 = User.find_first('where email=?', 'test@example.com')
#print 'find user:', u2

# 使用 mysql 命令直接进入mysql时，看不到schema.sql中创建的相关数据库和表
# 需要使用 mysql -u root -p 之后使用 1234 密码登录，可以看到已经创建的数据库 和 测试数据