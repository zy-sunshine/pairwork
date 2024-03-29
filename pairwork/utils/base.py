import os, logging
from django.http import HttpResponse, HttpRequest, HttpResponseNotAllowed
from django.template import RequestContext, loader
from django.conf import settings
from django import shortcuts
from django.utils.encoding import iri_to_uri
from django.contrib import auth
from django.contrib.auth.views import login, logout
from django.core import urlresolvers

from django.template import TemplateDoesNotExist

from django.core.urlresolvers import reverse

def get_absolute_path(request, relative_path = ''):
    relative_path = not relative_path and request.get_full_path() or relative_path
    if hasattr(request, 'build_absolute_uri') and callable(getattr(request, 'build_absolute_uri')):
        return request.build_absolute_uri(relative_path)
    else:
        # For django 0.96 there have no build_absolute_uri method
        #http_base = request.META['HTTP_REFERER']
        http_base = 'http://%s' % request.META['HTTP_HOST']
        http_base = http_base[-1] == '/' and http_base[:-1] or http_base
        return '%s%s' % (http_base, relative_path)

#From http://djangosnippets.org/snippets/2041/
class CallableViewClass(type):
    def __new__(cls, name, bases, dct):
        if 'HEAD' not in dct and 'GET' in dct:
            # XXX: this function could possibly be moved out
            # to the global namespace to save memory.
            def HEAD(self, request, *args, **kwargs):
                response = self.get(request, *args, **kwargs)
                response.content = u''
                return response
            dct['HEAD'] = HEAD

        dct['permitted_methods'] = []
        for method in ('GET', 'POST', 'PUT', 'DELETE', 'HEAD', 'OPTIONS', 'CONNECT', 'TRACE'):
            if hasattr(dct.get(method, None), '__call__'):
                dct['permitted_methods'].append(method)

        return type.__new__(cls, name, bases, dct)

    def __call__(self, *args, **kwargs):
        if args and isinstance(args[0], HttpRequest):
            instance = super(CallableViewClass, self).__call__()
            return instance.__call__(*args, **kwargs)
        else:
            instance = super(CallableViewClass, self).__call__(*args, **kwargs)
            return instance

class TemplateView(object):
    __metaclass__ = CallableViewClass

    def __call__(self, request, *args, **kwargs):
        if request.method in self.permitted_methods:
            handler = getattr(self, request.method)
            # XXX: Could possibly check if 'before' returns a response
            # and return that instead.
            self.before(request, args, kwargs)
            if hasattr(self, 'initialize'):
                self.initialize()
            handler(*args, **kwargs)
            if hasattr(self, 'after'):
                self.after()
            return self.response

        return HttpResponseNotAllowed(self.permitted_methods)

    def before(self, request, args, kwargs):
        """Override this method to add common functionality to all HTTP method handlers.

        args and kwargs are passed as regular arguments so you can add/remove arguments:
            def before(self, request, args, kwargs):
                kwargs['article'] = get_object_or_404(Article, id=kwargs.pop('article_id')
            def GET(self, request, article): # <== 'article' instead of 'article_id'
                ...
            def post(delf, request, article): # <== 'article' instead of 'article_id'
                ...
        """
        self.request = request
        self.response = HttpResponse()
        self.response.headers = Setter(self.response)
        self.response.out = Writer(self.response)
        self.request.uri = get_absolute_path(request)
        self.request.str_cookies = request.COOKIES
        self.request.remote_addr = request.META['REMOTE_ADDR']
        self.request.get_all = lambda x: request.REQUEST.getlist(x)
        try:
            self.referer = self.request.META['HTTP_REFERER']
        except:
            self.referer = None
    def after(self):
        pass
    def initialize(self):
        pass
        
class Setter(object):
    def __init__(self, response):
        self.response = response
    def __getitem__(self, header):
        self.response[header]
    def __delitem__(self, header):
        del self.response[header]
    def __setitem__(self, header, value):
        self.response[header] = value
    def add_header(self, header, value):
        self.response[header] = value

class Writer(object):
    def __init__(self, response):
        self.response = response
    def write(self, data):
        self.response.write(data)

class SiteRequestHandler(TemplateView):
    def __init__(self):
        self.template_vals = {}
        self.params = {}
        ## Don not define self.app_context there, it will override in sub class when use in render* method
    def initialize(self):
        TemplateView.initialize(self)
        ## some for authorize
        #self.login_user = users.get_current_user()
        ### TODO
        #  self.login_user = auth.authenticate(username='john', password='secret')
        #  self.is_login = (self.login_user is not None)
        #self.is_login = False
        ### TODO
        #   self.loginurl=reverse(login)#users.create_login_url(self.request.path)
        #   self.logouturl=reverse(logout)#users.create_logout_url(self.request.path)
        #self.is_admin = users.is_current_user_admin()
        #self.is_admin = False # TODO: make it valid
        # three status: admin author login
        #if self.is_admin:
        #    self.auth = 'admin'
        #    self.author=User.all().filter('email =',self.login_user.email()).get()
        #    if not self.author:
        #        # init author database
        #        self.author=User(dispname=self.login_user.nickname(),email=self.login_user.email())
        #        self.author.isadmin=True
        #        self.author.user=self.login_user
        #        self.author.put()
        #elif self.is_login:
        #    self.author=User.all().filter('email =',self.login_user.email()).get()
        #    if self.author:
        #        self.auth='author'
        #    else:
        #        self.auth = 'login'
        #else:
        #    self.auth = 'guest'

        

    ### TODO: check code position
    def error(self, message='an error occured', returl=None, errorcode=None):
        if not errorcode:
            self.render('message.html', {'error': message, 'returl': returl})
            return
        if errorcode == 404:
            message = 'Sorry, we were not able to find the requested page.  We have logged this error and will look into it.'
        elif errorcode == 403:
            message = 'Sorry, that page is reserved for administrators.  '
        elif errorcode == 500:
            message = "Sorry, the server encountered an error.  We have logged this error and will look into it."
        #self.template_vals.update( {'errorcode':errorcode,'message':message})

        # TODO:zy
        #if errorcode>0:
            #self.response.set_status(errorcode)


        #errorfile=getattr(self.blog.theme,'error'+str(errorcode))
        #logging.debug(errorfile)
##        if not errorfile:
##            errorfile=self.blog.theme.error
        errorfile='error'+str(errorcode)+".html"
        #try:
        #    content=micolog_template.render(self.blog.theme,errorfile, self.template_vals)
        #except TemplateDoesNotExist:
        #    try:
        #        content=micolog_template.render(self.blog.theme,"error.html", self.template_vals)
        #    except TemplateDoesNotExist:
        #        content=micolog_template.render(self.blog.default_theme,"error.html", self.template_vals)
        #    except:
        #        content=message
        #except:
        #    content=message
        #self.response.out.write(content)
        return self.render(errorfile, {'errorcode':errorcode,'message':message})

    def message(self, msg, returl=None, title='Infomation'):
        return self.render('message.html',{'info':msg, 'title':title, 'returl':returl})
    def warning(self, msg, returl=None, title='Warning'):
        return self.render('message.html', {'warning': msg, 'title': title, 'returl': returl})
    def info(self, msg):
        return self.render('message.html', {'info': msg})
    def success(self, msg):
        return self.render('message.html', {'success': msg})
    def render(self, template_file, params={}, mimetype=None, status=None,
            content_type=None):
        tpl = loader.get_template(template_file)
        self.renderImpl(tpl, params, mimetype, status, content_type)

    def renderEx(self, template, params={}, mimetype=None, status=None,
            content_type=None):
        self.renderImpl(template, params, mimetype, status, content_type)

    def renderImpl(self, template, params={}, mimetype=None, status=None,
            content_type=None):
        """
        Helper method to render the appropriate template
        """
        params.update(self.template_vals)
        c = RequestContext(self.request, params)
        self.response.write(template.render(c))
        if mimetype:
            content_type = mimetype
        if content_type:
            self.response['Content-Type'] = content_type
        #response = HttpResponse(template.render(c), **kargs)

    def attachment(self, filename='attachment.csv', mimetype='text/csv'):
        del self.response
        self.response = HttpResponse(mimetype=mimetype)
        self.response['Content-Disposition'] = 'attachment; filename=%s' % filename 
        
    def param(self, name, default=''):
        method = self.request.method == 'GET' and 'GET' or 'POST'
        method_obj = getattr(self.request, method)
        return method_obj.get(name, default)

    def paramstr(self, name, default=''):
        return self.param(name, default)
    
    def paramint(self, name, default=0):
        value = self.param(name)
        try:
           return int(value)
        except:
           return default

    def parambool(self, name, default=False):
        value = self.param(name)
        try:
           return value=='on'
        except:
           return default
           
    def paramfloat(self, name, default=0.00):
        value = self.param(name)
        try:
           return float(value)
        except:
           return default
           
    def paramlist(self, name, **kw):
        method = getattr(self.request, self.request.method)
        method2 = getattr(self.request, self.request.method == 'GET' and 'POST' or 'GET')
        ret = method.getlist(name)
        if not ret:
            ret = method2.getlist(name, **kw)
        return ret and ret or ''
        
    def write(self, s):
        self.response.out.write(s)

    def chk_login(self, redirect_url='/'):
        if self.is_login:
            return True
        else:
            self.redirect(redirect_url)
            return False

    def chk_admin(self, redirect_url='/'):
        if self.is_admin:
            return True
        else:
            self.redirect(redirect_url)
            return False
            
    def redirect(self, to, *args, **kwargs):
        if kwargs.pop('permanent', False):
            self.response.status_code = 301
        else:
            self.response.status_code = 302
        # If it's a model, use get_absolute_url()
        iri = to
        if hasattr(to, 'get_absolute_url'):
            iri = to.get_absolute_url()
        else:
            # Next try a reverse URL resolution.
            try:
                iri = urlresolvers.reverse(to, args=args, kwargs=kwargs)
            except urlresolvers.NoReverseMatch:
                # If this is a callable, re-raise.
                if callable(to):
                    raise
                # If this doesn't "feel" like a URL, re-raise.
                if '/' not in to and '.' not in to:
                    raise
        self.response['Location'] = iri_to_uri(iri)
        #return shortcuts.redirect(uri)
