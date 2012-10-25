# Create your views here.
from pairwork.utils.base import SiteRequestHandler
from .forms import ProfileForm, IntentInfoForm

class FHome(SiteRequestHandler):
	tpl = 'foreground/home.html'
	def GET(self):
		self.render(self.tpl, self.params)

class ModifyProfile(SiteRequestHandler):
	tpl = 'foreground/modifyprofile.html'
	def GET(self):
		form = ProfileForm()
		self.params['form'] = form
		self.render(self.tpl, self.params)

class ModifyIntentInfo(SiteRequestHandler):
	tpl = 'foreground/modifyintentinfo.html'
	def GET(self):
		form = IntentInfoForm()
		self.params['form'] = form
		self.render(self.tpl, self.params)
