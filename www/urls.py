#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Blues'

import os, re, time, base64, hashlib, logging

from transwarp.web import get, post, ctx, view, interceptor, seeother, notfound
from models import User, Blog, Comment
from apis import api, APIError, APIValueError, APIPermissionError, APIResourceNotFoundError
from config import configs

# Helper
_RE_MD5 = re.compile(r'^[0-9a-f]{32}$')
_RE_EMAIL = re.compile(r'^[a-z0-9\.\-\_]+\@[a-z0-9\-\_]+(\.[a-z0-9\-\_]+){1,4}$')
_COOKIE_NAME = 'awesession'
_COOKIE_KEY = configs.session.secret

def parse_signed_cookie(cookie_str):
	try:
		L = cookie_str.split('-')
		if len(L) != 3:
			return None
		id, expires, md5 = L
		if int(expires) < time.time():
			return None
		user = User.get(id)
		if user is None:
			return None
		if md5 != hashlib.md5('%s-%s-%s-%s' % (id, user.password, expires, _COOKIE_KEY)).hexdigest():
			return None
		return user
	except:
		return None

def make_signed_cookie(id, password, max_age):
	expires = str(int(time.time() + max_age))
	L = [id, expires, hashlib.md5('%s-%s-%s-%s' % (id, password, expires, _COOKIE_KEY)).hexdigest()]
	return '-'.join(L)

def check_admin():
	user = ctx.request.user
	if user and user.admin:
		return
	raise APIPermissionError('No permission.')

# URL拦截器
@interceptor('/')
def user_interceptor(next):
	logging.info('Try to bind user from session cookie...')
	user = None
	cookie = ctx.request.cookies.get(_COOKIE_NAME)
	if cookie:
		logging.info('parse session cookie...')
		user = parse_signed_cookie(cookie)
		if user:
			logging.info('bind user <%s> to session...' % user.email)
	ctx.request.user = user
	return next()

@interceptor('/manage/')
def manage_interceptor(next):
	user = ctx.request.user
	if user and user.admin:
		return next()
	raise seeother('/signin')

# 注册/登录
@api
@post('/api/users')
def register_user():
	i = ctx.request.input(name='', email='', password='')
	name = i.name.strip()
	email = i.email.strip().lower()
	password = i.password

	if not name:
		raise APIValueError('name')
	if not email or not _RE_EMAIL.match(email):
		raise APIValueError('email')
	if not password or not _RE_MD5.match(password):
		raise APIValueError('password')

	user = User.find_first('where email=?', email)
	if user:
		raise APIError('register:failed', 'email', 'Email is already in use')
	user = User(name=name, email=email, password=password, image='http://www.gravatar.com/avatar/%s?d=mm&s=120' % hashlib.md5(email).hexdigest())
	user.insert()

	# cookie
	cookie = make_signed_cookie(user.id, user.password, None)
	ctx.response.set_cookie(_COOKIE_NAME, cookie)
	return user

@api
@post('/api/authenticate')
def authenticate():
	i = ctx.request.input(remember='')
	email = i.email.strip().lower()
	password = i.password
	remember = i.remember
	user = User.find_first('where email=?', email)
	if user is None:
		raise APIError('auth:failed', 'email', 'Invalid email')
	elif user.password != password:
		raise APIError('auth:failed', 'password', 'Invalid password')

	# cookie
	max_age = 604800
	cookie = make_signed_cookie(user.id, user.password, max_age)
	ctx.response.set_cookie(_COOKIE_NAME, cookie, max_age=max_age)
	user.password = '******'
	return user

@api
@get('/api/users')
def api_get_users():
	# 如果sql语句语法错误，会提示Programming Error， 比如created_at 写成 create_at就会有这个错误
	users = User.find_by('order by created_at desc')
	logging.info('users\' count: %s' % len(users))
	for u in users:
		u.password = '******'
	return dict(users=users)

# 页面
@view('blogs.html')
@get('/')
def index():
	blogs = Blog.find_all()
	return dict(blogs=blogs, user=ctx.request.user)

@view('signin.html')
@get('/signin')
def signin():
	return dict()

@get('/signout')
def signout():
	ctx.response.delete_cookie(_COOKIE_NAME)
	raise seeother('/')

@view('register.html')
@get('/register')
def register():
	return dict()