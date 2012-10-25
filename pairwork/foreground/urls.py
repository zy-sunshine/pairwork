from django.conf.urls import patterns, include, url

urlpatterns = patterns('pairwork.foreground.views',
	url(r'^$', 'FHome', name='FHome'),

	# modify
	url(r'^modifyprofile/$', 'ModifyProfile', name="ModifyProfile"),
	url(r'^modifyintentinfo/$', 'ModifyIntentInfo', name="ModifyIntentInfo"),
)