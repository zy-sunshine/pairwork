from functools import wraps
from django.utils.decorators import available_attrs
from django.contrib.auth import authenticate
from django.http import HttpResponse
import json
def factest_check_auth(retDesc='factest authenticate failed'):
	
	def decorator(view_func):
		@wraps(view_func, assigned=available_attrs(view_func))
		def _wrapped_view(request, *args, **kwargs):
			ret = {}
			username = ''
			password = ''
			if request.method == 'GET':
				username = request.GET.get('username', '')
				password = request.GET.get('password', '')
			elif request.method == 'POST':
				username = request.POST.get('username', '')
				password = request.POST.get('password', '')
			user = authenticate(username=username, password=password)
			if not user:
				ret['ret'] = "1"
				ret['retDesc'] = retDesc
				return HttpResponse(json.dumps(ret), mimetype="application/json")
			else:
				request.user = user
				return view_func(request, *args, **kwargs)
		return _wrapped_view
	return decorator
