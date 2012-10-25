# Create your views here.
from pairwork.utils.base import SiteRequestHandler

class BHome(SiteRequestHandler):
    tpl = 'background/home.html'
    def GET(self):
        self.render(self.tpl, self.params)
