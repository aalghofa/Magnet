#decorators for py to make sure that employee logged in .. where it is required to log in
from functools import wraps
from flask import session, request, redirect, url_for, abort

def login_required(f):
	@wraps(f)
	def decorated_function(*args, **kwargs):
		#if user is not logged in
		if session.get('username') is None:
			return redirect(url_for('login', next=request.url))
		return f(*args, **kwargs)
	return decorated_function

def admin_required(f):
	@wraps(f)
	def decorated_function(*args, **kwargs):
		#if user is not logged in
		if session.get('is_admin') is False:
			abort(403)
		return f(*args, **kwargs)
	return decorated_function