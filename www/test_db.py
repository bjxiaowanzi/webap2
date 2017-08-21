#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 上面的文件头可以确保这些写的中文识别起来也没什么问题

from models import User, Blog, Comment

from transwarp import db

db.create_engine(user='www-data', password='www-data', database='blog')

u = User(name='Blues', email='blues@example.com', password='1234567890', image='about:blank')
u.insert()
print 'new user id:', u.id

blog1 = Blog(name='Blog1', summary='第一篇测试的博文标题', content='第一篇测试的博文，第一篇测试的博文，第一篇测试的博文，第一篇测试的博文，第一篇测试的博文，第一篇测试的博文，第一篇测试的博文！', user_id='00150254165747608e36aae414e40d28bef550952dbd166000', user_name='Test_Name', user_image='about:blank')
blog1.insert()
print 'new blog id:', blog1.id

blog2 = Blog(name='Blog2', summary='第二篇测试的博文标题', content='第二篇测试的博文，第二篇测试的博文，第二篇测试的博文，第二篇测试的博文，第二篇测试的博文，第二篇测试的博文，第二篇测试的博文！', user_id='00150254165747608e36aae414e40d28bef550952dbd166000', user_name='Test_Name', user_image='about:blank')
blog2.insert()
print 'new blog id:', blog2.id

blog3 = Blog(name='Blog3', summary='第三篇测试的博文标题', content='The third test blog, The third test blog, The third test blog, The third test blog, The third test blog, The third test blog！', user_id='00150254165747608e36aae414e40d28bef550952dbd166000', user_name='Test_Name', user_image='about:blank')
blog3.insert()
print 'new blog id:', blog3.id

#u1 = User.find_first('where email=?', 'test@example.com')
#print 'find user\'s name:', u1.name
#u1.delete()

#u2 = User.find_first('where email=?', 'test@example.com')
#print 'find user:', u2

# 使用 mysql 命令直接进入mysql时，看不到schema.sql中创建的相关数据库和表
# 需要使用 mysql -u root -p 之后使用 1234 密码登录，可以看到已经创建的数据库 和 测试数据